import pandas as pd 
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns
from scipy.stats import pearsonr
import matplotlib.ticker as ticker
import warnings
import baostock as bs
warnings.filterwarnings("ignore")
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
 
def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''.join(["\033[31m%s\033[0m"%'   '] * int(percent * total_length)) + ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
    print(bar, end='', flush=True)
    
    
class analyze_daily_factor:
    def __init__(self,factor,price,quantiles=5,periods=[1],neutralize=0,demeaned=False,show_IC_line=True,show_IC_heat=True,show_test_line=True,show_test_heat=True):
        factor.replace(np.inf,np.nan,inplace=True)
        factor.index=pd.to_datetime(factor.index)
        price.index=pd.to_datetime(price.index)
        self.factor=factor
        self.price=price
        self.quantiles=quantiles
        self.periods=periods
        self.neutralize=neutralize
        self.demeaned=demeaned 
        self.return_rate=[]
        self.factors=[]
        self.show_IC_line=show_IC_line
        self.show_IC_heat=show_IC_heat
        self.show_test_line=show_test_line
        self.show_test_heat=show_test_heat
        
        for i in range(len(periods)):
            time_gap=periods[i]
            return_rate_now=(price/price.shift(time_gap)-1).shift(-time_gap)
            return_rate_now.replace(np.inf, np.nan,inplace=True)
            return_rate_now=return_rate_now[:-time_gap]
            self.factors.append(factor[:-time_gap])
            self.return_rate.append(return_rate_now)
        
        if neutralize!=0:
            for i in range(len(periods)):
                time_gap=periods[i]
                lg = bs.login()  
                start_date=str(factor.index[0])[:10]
                end_date=str(factor.index[len(factor)-1])[:10]
                rs = bs.query_history_k_data_plus(neutralize,
                    "date,close",
                    start_date=start_date, end_date=end_date, frequency="d")
                data_list = []
                while (rs.error_code == '0') & rs.next():
                    data_list.append(rs.get_row_data())
                result = pd.DataFrame(data_list, columns=rs.fields)
                result.set_index('date',inplace=True)
                result.index=pd.to_datetime(result.index)
                result=result.astype(float)
                result=(result/result.shift(time_gap)-1).shift(-time_gap)
                result.replace(np.inf, np.nan,inplace=True)
                result.rename(columns={'close':'return_rate'},inplace=True)
                result=result[:-time_gap]
                self.return_rate[i]=self.return_rate[i].sub(result['return_rate'],axis=0)
                bs.logout()  
        
        if demeaned==True:
            for i in range(len(periods)):
                self.return_rate[i]=self.return_rate[i].sub(self.return_rate[i].mean(axis=1),axis=0)
                
                
    def strategy_information(self,rate,final_rate,time_gap):
        maxDrawdown=0
        years=(len(final_rate)+time_gap)/252
        annual_return=final_rate[len(final_rate)-1]**(1/years)-1
        Abs_return=final_rate[len(final_rate)-1]-1
        sr = np.mean(rate)/np.std(rate) * np.sqrt(252)
        for i in range(len(final_rate)-1):
            for j in range(i+1,len(final_rate)-1):
                if(final_rate[j]<final_rate[i]):
                    maxDrawdown=max((final_rate[i]-final_rate[j])/final_rate[i],maxDrawdown)
        victory_times=0
        for i in range(0,len(rate)):
            if rate[i]>0:
                victory_times+=1
        return annual_return,Abs_return,sr,maxDrawdown,victory_times/len(rate)


    def factor_statistic(self,percentiles=[0.2,0.4,0.6,0.8]):
        pd.set_option('display.max_columns', None)
        total=[]
        for i in range(self.quantiles):
            total.append([])
        for i in range(len(self.factor)):
            now_row=sorted(list(self.factor.iloc[i]))
            for j in range(self.quantiles):
                total[j]+=now_row[int(j*len(now_row)/self.quantiles):int((j+1)*len(now_row)/self.quantiles)]
        df=pd.DataFrame()
        for i in range(self.quantiles):
            df['第'+str(i+1)+'分组']=total[i]
        print(df.describe(percentiles=percentiles).T)
        
    def set_picture(self):
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(prop={'size':20})
    
    def group_picture(self,time_gap,factor):
        sns.set(palette="muted", color_codes=True)
        years=int(str(factor.index[len(factor)-1])[:4])-int(str(factor.index[0])[:4])+1
        months=[]
        for i in range(0,years):
            months.append([])
            for j in range(0,12):
                months[i].append(0)
                
        if self.show_test_line==True:       
            fig, ax = plt.subplots(figsize=(30,20))         
            for i in range(0,self.quantiles):
                ax.plot(factor.index.strftime('%Y-%m-%d'), self.group_total_return[i], label="The "+str(i+1)+'the group')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/8))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Return Rate",fontsize=20)
            self.set_picture()           
            plt.title(str(time_gap)+'day: Accumulated Return',fontdict={'size': 20})  
            plt.show()
            
            
            fig, ax = plt.subplots(figsize=(30,20))         
            for i in range(0,self.quantiles):
                ax.plot(factor.index.strftime('%Y-%m-%d'), self.group_compound_return[i], label="The "+str(i+1)+'the group')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/8))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Retun Rate",fontsize=20)
            self.set_picture()           
            plt.title(str(time_gap)+'day: Compounded Return',fontdict={'size': 24})  
            plt.show()
            
       
        ylist=[factor.index[0].year]
        current_year=factor.index[0].year
        for j in range(1,len(self.group_total_return[0])):
                if current_year!=factor.index[j].year:
                    ylist.append(factor.index[j].year)
                    current_year=factor.index[j].year
                    
        if self.show_test_heat==True:
            for i in range(0,self.quantiles):
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=1
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(self.group_total_return[i])):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=self.group_total_return[i][j]-current_rate
                        current_rate=self.group_total_return[i][j]
                        current_time=factor.index[j]
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(time_gap)+'days: the Accumulated Return of the '+str(i+1)+'th group',fontdict={'size': 24})
                plt.show()
                    
            for i in range(0,self.quantiles):
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=1
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(self.group_total_return[i])):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=(self.group_compound_return[i][j]-current_rate)/current_rate
                        current_rate=self.group_compound_return[i][j]
                        current_time=factor.index[j]
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(time_gap)+'days: the Compouned Return of the '+str(i+1)+'th group',fontdict={'size': 24})
                plt.show()
                
    def buy_and_sell(self,total_list,buy,sell,time_gap,factor):
        new_total=[]
        for i in range(len(total_list[0])):
            now=0
            for j in buy:
                now+=total_list[j][i]/(len(buy)+len(sell))
            for j in sell:
                now-=total_list[j][i]/(len(buy)+len(sell))
            new_total.append(now)
        rate=[]
        basic=1
        base=1
        for j in range(0,len(new_total)):
            if (j+1)%time_gap==0:
                base=basic
            basic+=new_total[j]*base
            rate.append(basic)
        self.group_compound_return=rate
        df=pd.DataFrame(columns=['策略收益率详情'],index=['年化复利收益','绝对复利收益','夏普比率','最大回撤','胜率'])
        annual_return,Abs_return,sr,maxDrawdown,victory_rate=self.strategy_information(new_total,rate,time_gap)
        df['策略收益率详情'][0]=annual_return
        df['策略收益率详情'][1]=Abs_return
        df['策略收益率详情'][2]=sr
        df['策略收益率详情'][3]=maxDrawdown
        df['策略收益率详情'][4]=victory_rate
        print()
        print(df.T)
        if self.show_test_line==True:
            fig, ax = plt.subplots(figsize=(30,20))         
            ax.plot(factor.index.strftime('%Y-%m-%d'), self.group_compound_return, label="复利累计收益率")
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/8))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Return Rate",fontsize=20)
            self.set_picture()           
            text=str(time_gap)+'days: The Compouned Return of buying '
            for i in buy:
                text+='the '+str(i+1)+'th group, '
            text+='and selling '
            for i in sell:
                text+='the '+str(i+1)+'th group, '
            plt.title(text,fontdict={'size': 24})  
            plt.show()
            
            
    def back_test(self,buy=[5],sell=[1]):
        buy[0]=min(self.quantiles,buy[0])
        for i in range(len(buy)):
            buy[i]-=1
        for i in range(len(sell)):
            sell[i]-=1
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            return_rate_now=self.return_rate[k]
            factor=self.factors[k]
            total_list=[]
            return_rate_now=return_rate_now/time_gap
            for i in range(self.quantiles):
                total_list.append([])
            for i in range(0,len(factor)):
                process_bar(float(i)/float(len(factor)), start_str='', end_str='100%', total_length=0)
                x=pd.DataFrame(index=list(factor.columns))
                x['factor']=factor.iloc[i]
                x['return_rate']=return_rate_now.iloc[i]
                x=x.T
                x.dropna(axis=1,inplace=True)
                x=x.sort_values(by='factor', axis=1)
                now_return=list(x.loc['return_rate'])
                for j in range(self.quantiles):
                    today_thisquantile=now_return[int(j*len(now_return)/self.quantiles):int((j+1)*len(now_return)/self.quantiles)]
                    total_list[j].append(np.mean(today_thisquantile))
        
            self.daily_rate=total_list
            rate=[]
            for i in range(self.quantiles):
                basic=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    basic+=total_list[i][j]
                    rate[i].append(basic)
            self.group_total_return=rate
            name_group=[]
            for i in range(self.quantiles):
                name_group.append(str(i+1)+'分位')
            df=pd.DataFrame(columns=name_group,index=['平均每日收益率','累计收益率','复利累计收益率','每日收益率标准差','年化复利收益','夏普比率','最大回撤','胜率'])
            for i in range(self.quantiles):
                df[str(i+1)+'分位'][0]=np.mean(total_list[i])/time_gap
            for i in range(self.quantiles):
                df[str(i+1)+'分位'][1]=np.sum(total_list[i])
            rate=[]
            for i in range(self.quantiles):
                basic=1
                base=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    if (j+1)%time_gap==0:
                        base=basic
                    basic+=total_list[i][j]*base
                    rate[i].append(basic)
                df[str(i+1)+'分位'][2]=rate[i][len(total_list[i])-1]-1
            self.group_compound_return=rate
            for i in range(self.quantiles):
                df[str(i+1)+'分位'][3]=np.std(total_list[i])
            for i in range(self.quantiles):
                annual_return,Abs_return,sr,maxDrawdown,victory_rate=self.strategy_information(total_list[i],rate[i],time_gap)
                df[str(i+1)+'分位'][4]=annual_return
                df[str(i+1)+'分位'][5]=sr
                df[str(i+1)+'分位'][6]=maxDrawdown
                df[str(i+1)+'分位'][7]=victory_rate
            print()
            print(df.T)
            self.group_picture(time_gap,factor)
            self.buy_and_sell(total_list,buy,sell,time_gap,factor)
    
    def IC_value(self,gap=10):
        sns.set(palette="muted", color_codes=True)
        names=[]
        for i in self.periods:
            names.append('period_'+str(i))

        day_IC=pd.DataFrame(index=names)
        IC_mean=[]
        IC_std=[]
        NormalIR=[]
        PIC=[]
        skIC=[]
        kurIC=[]
        
        day_Rank=pd.DataFrame(index=names)
        Rank_mean=[]
        Rank_std=[]
        NormalRank=[]
        PRank=[]
        skRank=[]
        kurRank=[]
        for i in range(len(self.periods)):
            factor=self.factors[i]
            return_rate_now=self.return_rate[i]
            RankIC=[]
            IC=[]
            P_IC_value=[]
            P_RankIC_value=[]
            for j in range(0,len(factor)):
                df=pd.DataFrame(index=list(factor.columns))
                df['factor']=factor.iloc[j]
                df['return_rate']=return_rate_now.iloc[j]
                df.dropna(inplace=True)
                x = df['factor']
                y = df['return_rate']
                RankIC.append(st.spearmanr(x,y)[0])
                IC.append(pearsonr(x,y)[0])
                P_IC_value.append(pearsonr(x,y)[1])
                P_RankIC_value.append(st.spearmanr(x,y)[1])
                
            
            IC_mean.append(np.mean(IC))
            IC_std.append(np.std(IC))
            NormalIR.append(np.mean(IC)/np.std(IC))
            PIC.append(np.mean(P_IC_value))
            skIC.append(pd.Series(IC).skew())
            kurIC.append(pd.Series(IC).kurtosis())
            
            Rank_mean.append(np.mean(RankIC))
            Rank_std.append(np.std(RankIC))
            NormalRank.append(np.mean(RankIC)/np.std(RankIC))
            PRank.append(np.mean(P_RankIC_value))
            skRank.append(pd.Series(RankIC).skew())
            kurRank.append(pd.Series(RankIC).kurtosis())
            if self.show_IC_line==True:
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(factor.index, IC, label='IC Value',alpha=0.3)
                ax.plot(factor.index, pd.Series(IC).rolling(gap).mean(), label='The Mean Value of IC: rolling windows length is '+str(gap),color='darkgreen')
                ax.legend(loc='best')
                plt.xlabel("Time",fontsize=24)
                plt.ylabel("IC Value",fontsize=24)
                plt.ylim(-0.5, 0.5)   
                plt.yticks([-0.5,-0.25,0, 0.25, 0.5])  
                self.set_picture()
                plt.title('The Line of IC Value: '+str(self.periods[i])+'days',fontdict={'size': 20})
                plt.show()
            
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(factor.index, RankIC, label='RankIC Value',alpha=0.3)
                ax.plot(factor.index, pd.Series(RankIC).rolling(gap).mean(), label='The Mean Value of RankIC: rolling windows length is '+str(gap),color='darkgreen')
                ax.legend(loc='best')
                plt.xlabel("Time",fontsize=24)
                plt.ylabel("Rank IC Value",fontsize=24)
                plt.ylim(-0.5, 0.5)   
                plt.yticks([-0.5,-0.25,0, 0.25, 0.5])
                self.set_picture()
                plt.title('The Line of Rank IC Value: '+str(self.periods[i])+'days',fontdict={'size': 20})
                plt.show()
            
            if self.show_IC_heat==True:
                years=int(str(factor.index[len(factor)-1])[:4])-int(str(factor.index[0])[:4])+1
                months=[]
                for ii in range(0,years):
                    months.append([])
                    for j in range(0,12):
                        months[ii].append(0)
                ylist=[factor.index[0].year]
                current_year=factor.index[0].year
                for j in range(1,len(IC)):
                        if current_year!=factor.index[j].year:
                            ylist.append(factor.index[j].year)
                            current_year=factor.index[j].year
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=[IC[0]]
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(IC)):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=np.mean(current_rate)
                        current_rate=[IC[j]]
                        current_time=factor.index[j]
                    else:
                        current_rate.append(IC[j])
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(self.periods[i])+'days: IC Mean Value ',fontdict={'size': 24})
                plt.show()
                
                
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=[RankIC[0]]
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(IC)):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=np.mean(current_rate)
                        current_rate=[RankIC[j]]
                        current_time=factor.index[j]
                    else:
                        current_rate.append(RankIC[j])
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(self.periods[i])+'days: Rank IC Mean Value ',fontdict={'size': 24})
                plt.show()
            
            
        day_IC['IC Mean']=IC_mean 
        day_IC['IC Std.']=IC_std
        day_IC['IR']=NormalIR
        day_IC['p-value']=PIC
        day_IC['IC Skew']=skIC
        day_IC['IC Kurtosis']=kurIC
        print(day_IC.T)
        day_Rank['Rank IC Mean']=Rank_mean 
        day_Rank['Rank IC Std.']=Rank_std
        day_Rank['Rank IR']=NormalRank
        day_Rank['Rank p-value']=PRank
        day_Rank['IC Skew']=skRank
        day_Rank['Rank IC Kurtosis']=kurRank
        print()
        print(day_Rank.T)
    
    
    def exchange_rate(self):
        names=[]
        for i in self.periods:
            names.append('period_'+str(i))
        exchange_df=pd.DataFrame(columns=names)
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            return_rate_now=self.return_rate[k]
            factor=self.factors[k]
            exchange_list=[]
            return_rate_now=return_rate_now/time_gap
            for i in range(self.quantiles):
                exchange_list.append([])
            for d in range(time_gap):
                for i in range(d,len(factor),time_gap):
                    x=pd.DataFrame(index=list(factor.columns))
                    x['factor']=factor.iloc[i]
                    x['return_rate']=return_rate_now.iloc[i]
                    x=x.T
                    x.dropna(axis=1,inplace=True)
                    x=x.sort_values(by='factor', axis=1)
                    now_names=list(x.columns)
                    new_names=[]
                    for j in range(self.quantiles):
                        new_names.append(now_names[int(j*len(now_names)/self.quantiles):int((j+1)*len(now_names)/self.quantiles)])
                    if i>=time_gap:
                        for j in range(self.quantiles):
                            new_one=0
                            for name in old_names[j]:
                                if name not in new_names[j]:
                                    new_one+=1
                            exchange_list[j].append(new_one/len(new_names[j]))
                    old_names=new_names
            summary=[]
            for i in range(self.quantiles):
                summary.append(np.mean(exchange_list[i]))
            exchange_df.iloc[:,k]=summary  
        names=[]
        for i in range(self.quantiles):
            names.append('Quantile '+str(i+1)+' Mean Turnover')
        exchange_df['Quantile Turnover']=names 
        exchange_df.set_index('Quantile Turnover',inplace=True)
        print(exchange_df)
                
        
    def self_corr(self):
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            factor=self.factors[k]
            corr_list=[]
            for i in range(time_gap,len(factor)):
                try:
                    new_df=factor.iloc[[i,i-time_gap],:]
                    new_df.dropna(axis=1,inplace=True)
                    corr=np.corrcoef(new_df.iloc[0],new_df.iloc[1])
                    corr_list.append(corr)
                except:
                    continue
            print('因子滞后'+str(time_gap)+'天的自相关性系数为:',end=' ')
            print(np.mean(corr_list).round(4))
            
    
    def get_all(self,percentiles=[0.2,0.4,0.6,0.8],buy=[5],sell=[1],gap=10):
        self.factor_statistic(percentiles)
        self.IC_value(gap)
        self.back_test(buy=buy,sell=sell)
        self.exchange_rate()
        self.self_corr()
        pd.set_option('display.max_columns', 5)
        


class analyze_minute_factor:
    def __init__(self,factor,price,minute,quantiles=5,periods=[240],demeaned=False,trade_day=[],trade_time=[],show_IC_line=True,show_IC_heat=True,show_test_line=True):
        factor.replace(np.inf,np.nan,inplace=True)
        factor.index=pd.to_datetime(factor.index)
        price.index=pd.to_datetime(price.index)
        self.factor=factor
        self.price=price
        self.quantiles=quantiles
        self.periods=periods
        self.demeaned=demeaned 
        self.return_rate=[]
        self.factors=[]
        self.minute=minute
        self.trade_day=trade_day
        self.trade_time=trade_time
        self.show_IC_line=show_IC_line
        self.show_IC_heat=show_IC_heat
        self.show_test_line=show_test_line

        if len(trade_day)!=0 and len(trade_time)!=0:
            periods=[]
            self.type='time'
            for i in range(len(trade_day)):
                all_trade_days=list(set(list(factor.index.date.astype(str))))
                all_trade_days.sort()
                return_rate_now=pd.DataFrame()
                for j in range(len(factor)):
                    try:
                        new_time=all_trade_days[all_trade_days.index(factor.index.values[j].astype(str)[:10])+trade_day[i]]+" "+trade_time[i]
                        new_time=pd.to_datetime(new_time)
                        new_dataframe=pd.DataFrame(price.loc[new_time]/price.iloc[j]-1).T
                        if j==0:
                            for k in range(len(factor)):
                                if price.index.values[k]==new_time:
                                    time_gap=k-j
                                    periods.append(time_gap)
                                    break 
                        new_dataframe.index=[factor.index.values[j]]
                        return_rate_now=pd.concat([return_rate_now,new_dataframe])
                    except:
                        break
                self.return_rate.append(return_rate_now)
                self.factors.append(factor[:-time_gap])
            self.periods=periods
        
        else:
            self.type='K'
            for i in range(len(periods)):
                time_gap=periods[i]
                return_rate_now=(price/price.shift(time_gap)-1).shift(-time_gap)
                return_rate_now.replace(np.inf, np.nan,inplace=True)
                return_rate_now=return_rate_now[:-time_gap]
                self.factors.append(factor[:-time_gap])
                self.return_rate.append(return_rate_now)
        
        if demeaned==True:
            for i in range(len(periods)):
                self.return_rate[i]=self.return_rate[i].sub(self.return_rate[i].mean(axis=1),axis=0)
                
                
    def strategy_information(self,rate,final_rate,time_gap):
        maxDrawdown=0
        years=(len(final_rate)+time_gap)/(240/self.minute)/252
        annual_return=final_rate[len(final_rate)-1]**(1/years)-1
        Abs_return=final_rate[len(final_rate)-1]-1
        sr = np.mean(rate)/np.std(rate) * np.sqrt(252)
        for i in range(len(final_rate)-1):
            for j in range(i+1,len(final_rate)-1):
                if(final_rate[j]<final_rate[i]):
                    maxDrawdown=max((final_rate[i]-final_rate[j])/final_rate[i],maxDrawdown)
        victory_times=0
        for i in range(0,len(rate)):
            if rate[i]>0:
                victory_times+=1
        return annual_return,Abs_return,sr,maxDrawdown,victory_times/len(rate)


    def factor_statistic(self,percentiles=[0.2,0.4,0.6,0.8]):
        pd.set_option('display.max_columns', None)
        total=[]
        for i in range(self.quantiles):
            total.append([])
        for i in range(len(self.factor)):
            now_row=sorted(list(self.factor.iloc[i]))
            for j in range(self.quantiles):
                total[j]+=now_row[int(j*len(now_row)/self.quantiles):int((j+1)*len(now_row)/self.quantiles)]
        df=pd.DataFrame()
        for i in range(self.quantiles):
            df['第'+str(i+1)+'分位']=total[i]
        print(df.describe(percentiles=percentiles).T)
        
    def set_picture(self):
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(prop={'size':20})
    
    def group_picture(self,time_gap,factor,day):
        sns.set(palette="muted", color_codes=True)
        years=int(str(factor.index[len(factor)-1])[:4])-int(str(factor.index[0])[:4])+1
        months=[]
        for i in range(0,years):
            months.append([])
            for j in range(0,12):
                months[i].append(0)
                
        if self.show_test_line==True:       
            fig, ax = plt.subplots(figsize=(30,20))         
            for i in range(0,self.quantiles):
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), self.group_total_return[i], label="The "+str(i+1)+'the group')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/6))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Return Rate",fontsize=20)
            self.set_picture()     
            if self.type=='K':
                plt.title(str(time_gap)+' K Line: Accumulated Return Rate',fontdict={'size': 24})  
            else:
                plt.title('After '+str(self.trade_day[day])+'days at '+self.trade_time[day]+': Accumulated Return Rate',fontdict={'size': 20})
            plt.show()
            
            
            fig, ax = plt.subplots(figsize=(30,20))         
            for i in range(0,self.quantiles):
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), self.group_compound_return[i], label="The "+str(i+1)+'the group')
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/6))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Return Rate",fontsize=20)
            self.set_picture()   
            if self.type=='K':        
                plt.title(str(time_gap)+' K Line: Compounded Return Rate',fontdict={'size': 24})
            else:
                plt.title('After '+str(self.trade_day[day])+'days at '+self.trade_time[day]+': Compounded Return Rate',fontdict={'size': 24})
            plt.show()
        
                
    def buy_and_sell(self,total_list,buy,sell,time_gap,factor,day):
        new_total=[]
        for i in range(len(total_list[0])):
            now=0
            for j in buy:
                now+=total_list[j][i]/(len(buy)+len(sell))
            for j in sell:
                now-=total_list[j][i]/(len(buy)+len(sell))
            new_total.append(now)
        rate=[]
        basic=1
        base=1
        for j in range(0,len(new_total)):
            if (j+1)%time_gap==0:
                base=basic
            basic+=new_total[j]*base
            rate.append(basic)
        self.group_compound_return=rate
        df=pd.DataFrame(columns=['策略收益率详情'],index=['年化复利收益','绝对复利收益','夏普比率','最大回撤','胜率'])
        annual_return,Abs_return,sr,maxDrawdown,victory_rate=self.strategy_information(new_total,rate,time_gap)
        df['策略收益率详情'][0]=annual_return
        df['策略收益率详情'][1]=Abs_return
        df['策略收益率详情'][2]=sr
        df['策略收益率详情'][3]=maxDrawdown
        df['策略收益率详情'][4]=victory_rate
        print()
        print(df.T)
        if self.show_test_line==True:
            fig, ax = plt.subplots(figsize=(30,20))         
            ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), self.group_compound_return, label="复利累计收益率")
            ax.legend(loc='best')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(factor)/6))
            plt.xlabel("Time",fontsize=20)
            plt.ylabel("Return Rate",fontsize=20)
            self.set_picture()   
            if self.type=='K':        
                text='The Compounded Return of ' +str(time_gap)+'K Line: buy '
            else:
                text='After '+str(self.trade_day[day])+'days at '+self.trade_time[day]+': buy '
            for i in buy:
                text+='the '+str(i+1)+'the group,'
            text+='and sell '
            for i in sell:
                text+='the '+str(i+1)+'the group,'
            plt.title(text,fontdict={'size': 24})  
            plt.show()
        
            
    def back_test(self,buy=[5],sell=[1]):
        buy[0]=min(self.quantiles,5)
        for i in range(len(buy)):
            buy[i]-=1
        for i in range(len(sell)):
            sell[i]-=1
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            return_rate_now=self.return_rate[k]
            factor=self.factors[k]
            total_list=[]
            return_rate_now=return_rate_now/time_gap
            for i in range(self.quantiles):
                total_list.append([])
            for i in range(0,len(factor)):
                process_bar(float(i)/float(len(factor)), start_str='', end_str='100%', total_length=0)
                x=pd.DataFrame(index=list(factor.columns))
                x['factor']=factor.iloc[i]
                x['return_rate']=return_rate_now.iloc[i]
                x=x.T
                x.dropna(axis=1,inplace=True)
                x=x.sort_values(by='factor', axis=1)
                now_return=list(x.loc['return_rate'])
                for j in range(self.quantiles):
                    today_thisquantile=now_return[int(j*len(now_return)/self.quantiles):int((j+1)*len(now_return)/self.quantiles)]
                    total_list[j].append(np.mean(today_thisquantile))
        
            self.daily_rate=total_list
            rate=[]
            for i in range(self.quantiles):
                basic=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    basic+=total_list[i][j]
                    rate[i].append(basic)
            self.group_total_return=rate
            name_group=[]
            for i in range(self.quantiles):
                name_group.append(str(i+1)+'分位')
            df=pd.DataFrame(columns=name_group,index=['累计收益率','复利累计收益率','年化复利收益','夏普比率','最大回撤','胜率'])
            for i in range(self.quantiles):
                df[str(i+1)+'分位'][0]=np.sum(total_list[i])
            rate=[]
            for i in range(self.quantiles):
                basic=1
                base=1
                rate.append([])
                for j in range(0,len(total_list[i])):
                    if (j+1)%time_gap==0:
                        base=basic
                    basic+=total_list[i][j]*base
                    rate[i].append(basic)
                df[str(i+1)+'分位'][1]=rate[i][len(total_list[i])-1]-1
            self.group_compound_return=rate
            for i in range(self.quantiles):
                annual_return,Abs_return,sr,maxDrawdown,victory_rate=self.strategy_information(total_list[i],rate[i],time_gap)
                df[str(i+1)+'分位'][2]=annual_return
                df[str(i+1)+'分位'][3]=sr
                df[str(i+1)+'分位'][4]=maxDrawdown
                df[str(i+1)+'分位'][5]=victory_rate
            print()
            print(df.T)
            day=k
            self.group_picture(time_gap,factor,day)
            self.buy_and_sell(total_list,buy,sell,time_gap,factor,day)
    
    def IC_value(self,gap=10):
        sns.set(palette="muted", color_codes=True)
        names=[]
        for i in self.periods:
            names.append('period_'+str(i))

        day_IC=pd.DataFrame(index=names)
        IC_mean=[]
        IC_std=[]
        NormalIR=[]
        PIC=[]
        skIC=[]
        kurIC=[]
        
        day_Rank=pd.DataFrame(index=names)
        Rank_mean=[]
        Rank_std=[]
        NormalRank=[]
        PRank=[]
        skRank=[]
        kurRank=[]
        for i in range(len(self.periods)):
            factor=self.factors[i]
            return_rate_now=self.return_rate[i]
            RankIC=[]
            IC=[]
            P_IC_value=[]
            P_RankIC_value=[]
            for j in range(0,len(factor)):
                df=pd.DataFrame(index=list(factor.columns))
                df['factor']=factor.iloc[j]
                df['return_rate']=return_rate_now.iloc[j]
                df.dropna(inplace=True)
                x = df['factor']
                y = df['return_rate']
                RankIC.append(st.spearmanr(x,y)[0])
                IC.append(pearsonr(x,y)[0])
                P_IC_value.append(pearsonr(x,y)[1])
                P_RankIC_value.append(st.spearmanr(x,y)[1])
                
            
            IC_mean.append(np.mean(IC))
            IC_std.append(np.std(IC))
            NormalIR.append(np.mean(IC)/np.std(IC))
            PIC.append(np.mean(P_IC_value))
            skIC.append(pd.Series(IC).skew())
            kurIC.append(pd.Series(IC).kurtosis())
            
            Rank_mean.append(np.mean(RankIC))
            Rank_std.append(np.std(RankIC))
            NormalRank.append(np.mean(RankIC)/np.std(RankIC))
            PRank.append(np.mean(P_RankIC_value))
            skRank.append(pd.Series(RankIC).skew())
            kurRank.append(pd.Series(RankIC).kurtosis())
            
            
            if self.show_IC_line==True:
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), IC, label='IC Value',alpha=0.3)
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), pd.Series(IC).rolling(gap).mean(), label='The Mean Value of IC: rolling windows length is'+str(gap),color='darkgreen')
                ax.legend(loc='best')
                plt.xlabel("Time",fontsize=20)
                plt.ylabel("IC Value",fontsize=20)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.ylim(-0.5, 0.5)   
                plt.yticks([-0.5,-0.25,0, 0.25, 0.5])
                self.set_picture()
                if self.type=='K':
                    plt.title(str(self.periods[i])+'K Line: IC Value',fontdict={'size': 20})
                else:
                    plt.title('After '+str(self.trade_day[i])+'days at '+self.trade_time[i]+': IC Value',fontdict={'size': 20})
                plt.show()
                
                fig, ax = plt.subplots(figsize=(24,10))
                plt.ylim(-1.25, 1.25)
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), RankIC, label='RankIC Value',alpha=0.3)
                ax.plot(factor.index.strftime('%Y-%m-%d %H:%M:%S'), pd.Series(RankIC).rolling(gap).mean(), label='The Mean Value of Rank IC: rolling windows length is'+str(gap),color='darkgreen')
                ax.legend(loc='best')
                plt.xlabel("Time",fontsize=20)
                plt.ylabel("IC Value",fontsize=20)
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=len(self.factor)/6))
                plt.ylim(-0.5, 0.5)   
                plt.yticks([-0.5,-0.25,0, 0.25, 0.5])
                self.set_picture()
                if self.type=='K':
                    plt.title(str(self.periods[i])+'K Line: Rank IC Value',fontdict={'size': 20})
                else:
                    plt.title('After '+str(self.trade_day[i])+'days at '+self.trade_time[i]+': Rank IC Value',fontdict={'size': 20})
                plt.show()
            
            
            if self.show_IC_heat==True:
                years=int(str(factor.index[len(factor)-1])[:4])-int(str(factor.index[0])[:4])+1
                months=[]
                for ii in range(0,years):
                    months.append([])
                    for j in range(0,12):
                        months[ii].append(0)
                ylist=[factor.index[0].year]
                current_year=factor.index[0].year
                for j in range(1,len(IC)):
                        if current_year!=factor.index[j].year:
                            ylist.append(factor.index[j].year)
                            current_year=factor.index[j].year
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=[IC[0]]
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(IC)):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=np.mean(current_rate)
                        current_rate=[IC[j]]
                        current_time=factor.index[j]
                    else:
                        current_rate.append(IC[j])
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(self.periods[i])+'days: IC Mean Value ',fontdict={'size': 24})
                plt.show()
                
                
                fig, ax = plt.subplots(figsize=(30,20))
                current_rate=[RankIC[0]]
                current_time=factor.index[0]
                current_year=factor.index[0]
                for j in range(0,years):
                    for k in range(0,12):
                        months[j][k]=0
                for j in range(1,len(IC)):
                    if current_time.month!=self.factor.index[j].month:
                        years=int(str(factor.index[j-1])[:4])-int(str(factor.index[0])[:4])
                        months[years][current_time.month-1]=np.mean(current_rate)
                        current_rate=[RankIC[j]]
                        current_time=factor.index[j]
                    else:
                        current_rate.append(RankIC[j])
                xlist=['1','2','3','4','5','6','7','8','9','10','11','12']
                months=np.array(months)
                ax=sns.heatmap(months,mask=months==0,xticklabels=xlist,yticklabels=ylist,cmap='RdYlGn_r',annot=True,annot_kws={"fontsize":20})
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                cbar = ax.collections[0].colorbar
                cbar.ax.tick_params(labelsize=20)
                ax.set_title(str(self.periods[i])+'days: Rank IC Mean Value ',fontdict={'size': 24})
                plt.show()
                
    
        day_IC['IC Mean']=IC_mean 
        day_IC['IC Std.']=IC_std
        day_IC['IR']=NormalIR
        day_IC['p-value']=PIC
        day_IC['IC Skew']=skIC
        day_IC['IC Kurtosis']=kurIC
        print(day_IC.T)
        day_Rank['Rank IC Mean']=Rank_mean 
        day_Rank['Rank IC Std.']=Rank_std
        day_Rank['Rank IR']=NormalRank
        day_Rank['Rank p-value']=PRank
        day_Rank['IC Skew']=skRank
        day_Rank['Rank IC Kurtosis']=kurRank
        print()
        print(day_Rank.T)
        
    
    
    def exchange_rate(self):
        names=[]
        for i in self.periods:
            names.append('period_'+str(i))
        exchange_df=pd.DataFrame(columns=names)
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            return_rate_now=self.return_rate[k]
            factor=self.factors[k]
            exchange_list=[]
            return_rate_now=return_rate_now/time_gap
            for i in range(self.quantiles):
                exchange_list.append([])
            for d in range(time_gap):
                for i in range(d,len(factor),time_gap):
                    x=pd.DataFrame(index=list(factor.columns))
                    x['factor']=factor.iloc[i]
                    x['return_rate']=return_rate_now.iloc[i]
                    x=x.T
                    x.dropna(axis=1,inplace=True)
                    x=x.sort_values(by='factor', axis=1)
                    now_names=list(x.columns)
                    new_names=[]
                    for j in range(self.quantiles):
                        new_names.append(now_names[int(j*len(now_names)/self.quantiles):int((j+1)*len(now_names)/self.quantiles)])
                    if i>=time_gap:
                        for j in range(self.quantiles):
                            new_one=0
                            for name in old_names[j]:
                                if name not in new_names[j]:
                                    new_one+=1
                            exchange_list[j].append(new_one/len(new_names[j]))
                    old_names=new_names
            summary=[]
            for i in range(self.quantiles):
                summary.append(np.mean(exchange_list[i]))
            exchange_df.iloc[:,k]=summary  
        names=[]
        for i in range(self.quantiles):
            names.append('Quantile '+str(i+1)+' Mean Turnover')
        exchange_df['Quantile Turnover']=names 
        exchange_df.set_index('Quantile Turnover',inplace=True)
        print(exchange_df)
                
        
    def self_corr(self):
        for k in range(len(self.periods)):
            time_gap=self.periods[k]
            factor=self.factors[k]
            corr_list=[]
            for i in range(time_gap,len(factor)):
                try:
                    new_df=factor.iloc[[i,i-time_gap],:]
                    new_df.dropna(axis=1,inplace=True)
                    corr=np.corrcoef(new_df.iloc[0],new_df.iloc[1])
                    corr_list.append(corr)
                except:
                    continue
            if self.type=='K':
                print('因子滞后'+str(time_gap)+'根K线的自相关性系数为:',end=' ')
            else:
                print('因子滞后'+str(self.trade_day[k])+'天在时刻'+self.trade_time[k]+'的自相关性系数为:',end=' ')
            print(np.mean(corr_list).round(4))
            
    
    def get_all(self,percentiles=[0.2,0.4,0.6,0.8],buy=[5],sell=[1],gap=10):
        self.factor_statistic(percentiles)
        self.IC_value(gap)
        self.back_test(buy,sell)
        self.exchange_rate()
        self.self_corr()
        pd.set_option('display.max_columns', 5)
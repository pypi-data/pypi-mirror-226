"""
Correlator Class performs the main functions.
Find the correlation between input data_x and ideal data_y
"""
import numpy as np
import pandas as pd
import wbgapi as wb
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats


from ..macroIndicator import *
from ..utils import *


class Correlator:
    
    # create one correlator object for each set of input data x
    def __init__(self, data_x=None, date=None, start_date=None, end_date=None):
        
        # check if input data x has only one colomn, raise error if not valid
        data_x= np.array(data_x)
        if data_x.all()==None or data_x.ndim == 1!= 1:
            raise ValueError(f"input data x isn't in a valid format. Please refer to 'link' to get the correct format")
        self.data_x = data_x

        if len(data_x)!= len(date):
            raise ValueError(f"Date doesn't match with data x. Make sure they have the same number of values")

        # set correct date format and range
        if not start_date:
            start_date= date[0]
        
        if not end_date:
            end_date= date[-1]

        self.date = utils.toDateTime(date)

        self.df_x= pd.DataFrame(data=self.data_x, index=self.date)

        self.x_freq_index=utils.infer_frequency(self.df_x.index)
        
        normalized_x=utils.normalize_df(self.df_x.copy(True))
        
        # total x: dictionary{ style: respective dataset}
        self.total={}
        self.total['normalized']=normalized_x


        
     

    def get_data_y_WorldBank(self, indicator:str, country):
        country_ABW=wb.economy.coder(country)
        region_input=[]
        region_input.append(country_ABW)
        data= wb.data.DataFrame(indicator,economy=region_input,time=range(self.date[0].year,self.date[-1].year ))
        df=utils.format_data_WorldBank(data, indicator)
        return df
    
    def get_data_y_YahooFinance(self, ticker:str, start_date, end_date):
        data=yf.download(ticker, start=start_date, end=end_date)
        df= pd.DataFrame(data=data['Close'], index=data.index)
        return df

    def graph_data(self, indicator:str, country='USA'):
        # normalized_x= self.total['normalized']
        data_y= self.get_data_web(indicator, country=country)
        # normalized_y= utils.normalize_df(data_y)
        data_x=self.df_x.values
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Datetime')
        ax1.set_ylabel('input', color=color)  # we already handled the x-label with ax1
        ax1.plot(self.df_x.index,data_x, color=color)
        ax1.tick_params(axis='y',labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel(data_y.columns[0], color=color)  # we already handled the x-label with ax1
        ax2.plot(data_y.index, data_y[data_y.columns[0]], color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
        return

    def sample_data(self, df_og: pd.DataFrame, crr_freq, target_freq):
        df=[]
        if crr_freq >=target_freq: # only standarlize df 
            df= df_og.resample(crr_freq).mean()
        else: # downcale current df into larger time frequency
            df= df_og.resample(target_freq).mean()
        limit= max(3, len(df.index)//10)
        df= df.ffill(limit=limit).bfill(limit=limit)
        return df
    
    def get_data_web(self, y_name:str, country='USA'):
        # retrive data from internet
        y_name_uniform=utils.filter_string(y_name)
        src= macroIndicator.mi_dict[y_name_uniform]
        provider= src[1]
        if provider==0:
            df_y= self.get_data_y_YahooFinance(src[0], self.date[0], self.date[-1])
            df_y.columns=[y_name]
            return df_y
        elif provider==1:
            df_y= self.get_data_y_WorldBank(src[0], country)
            df_y.columns=[y_name]
            return df_y 
        

    def get_df_y(self, y_name:str, country='USA'):
        # retrive data from internet
        data_y= self.get_data_web(y_name, country)
        # standardize data
        dfy_freq_index= utils.infer_frequency(data_y.index)
        df_y= self.sample_data(data_y, crr_freq=utils.datetime_freqs[dfy_freq_index], target_freq= utils.datetime_freqs[self.x_freq_index])
        df_y= df_y.loc[(df_y.index >= self.df_x.index[0]) & (df_y.index <= self.df_x.index[-1])]
        return [dfy_freq_index, df_y]
    
    # not accesible by user
    def get_Correlation_system(self, y_name, country='USA'):
        # get standardized df for x and y under same time scale
        y_res_arr=self.get_df_y(y_name,country)
        y_freq_index=y_res_arr[0]
        df_y= y_res_arr[1]
        df_y= df_y.dropna()
        if(len(df_y)<=0):
            return [0,0]
        if y_freq_index not in self.total: # frequency is the same
            self.total[y_freq_index]=self.sample_data(self.df_x, crr_freq=utils.datetime_freqs[self.x_freq_index], target_freq= utils.datetime_freqs[y_freq_index])
        df_x= self.total[y_freq_index].copy(deep=True)
        df_x= df_x.loc[df_y.index]
        # calculate x and y correlation
        res = stats.pearsonr(df_x[df_x.columns[0]], df_y[df_y.columns[0]])
        if np.isnan(res[0]):
            return [0,0]
        return res
        
    #accesible by user
    def get_Correlation(self, y_name, country='USA', graph=True):
        # get standardized df for x and y under same time scale
        y_res_arr=self.get_df_y(y_name,country)
        y_freq_index=y_res_arr[0]
        df_y= y_res_arr[1]
        df_y= df_y.dropna()
        if(len(df_y)<=0):
            print(f'the {y_name} indicator is not valid for this specific country or the date-range' )
            return 
        if y_freq_index not in self.total: # frequency is the same
            self.total[y_freq_index]=self.sample_data(self.df_x, crr_freq=utils.datetime_freqs[self.x_freq_index], target_freq= utils.datetime_freqs[y_freq_index])
        df_x= self.total[y_freq_index].copy(deep=True)
        df_x= df_x.loc[df_y.index]
        # calculate x and y correlation
        res = stats.pearsonr(df_x[df_x.columns[0]], df_y[df_y.columns[0]])
        if np.isnan(res[0]):
            print(f'there is not enough data to produce a valid correlation between the input data and {y_name} correlator' )
            return 
        
        print(f'{y_name}: Pearson coefficient of {res[0]} with p-value of {res[1]}.')
        if graph:
            self.graph_data(y_name, country=country)
        return res
        

    #accesible by user
    def analyze_Correlation(self, category='population', country='USA', top_num=3):
        category_name=utils.filter_string(category)
        res={}
        for indicator in macroIndicator.categories[category_name]:
            res[macroIndicator.mi_dict[indicator][-1]]=self.get_Correlation_system(indicator,country=country)

        high= sorted(res, key=lambda dict_key: abs(res[dict_key][0]), reverse=True)[:top_num]
        # Finding 3 highest values
        high_crrs={}
        for h in high:
            high_crrs[h]=res[h]
        
        response=f'The {h} most correlated macro-indicators with the input data: '
        for indicator, statistics in high_crrs.items():
            response+= '\n'
            response+= f'{indicator}: Pearson coefficient of {statistics[0]} with p-value of {statistics[1]}.'
        
        print(response)
        self.graph_data(high[0], country=country)
        return
    
    
        


    



    




     


        

    
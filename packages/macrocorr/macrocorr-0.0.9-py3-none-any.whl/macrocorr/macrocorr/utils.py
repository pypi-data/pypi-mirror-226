import numpy as np
import pandas as pd
import re

class utils:
    def filter_string(s:str):
        s=s.replace("_", " ")
        s=s.replace(" ", "")
        newS= s.lower()
        return newS
    
    datetime_freqs=['D','W','M','Q','Y']
    def infer_frequency(date: pd.DatetimeIndex):
        front=(date[1]-date[0]).days
        mid=(date[(len(date)//2)]-date[(len(date)//2-1)]).days
        last=(date[-1]-date[-2]).days
        gap=(front+mid+last)//3
        if gap <=3:
            return 0
        elif gap<=10:
            return 1
        elif gap<=35:
            return 2
        elif gap<=120:
            return 3
        elif gap<=400:
            return 4
        else:
            raise ValueError(f"datetime frequency is invalid: "+ str(gap))

    
    def toDateTime(datedata):
        try:
            date=pd.to_datetime(datedata,  format='mixed')
            input_frequency= pd.infer_freq(date)
            date.freq= input_frequency
            return date
        except:
            date=[]
            for i in datedata:
                s=re.sub("[^0123456789\.:']","",i)
                date.append(s)
            date=pd.to_datetime(date, format='mixed')
            input_frequency= pd.infer_freq(date)
            date.freq= input_frequency
            return date
    
    def standardize_datetime(df: pd.DataFrame, freq: str):
        df.resample(rule=freq)
        return df

    
    def format_data_WorldBank(data, indicator):
        value= data.to_numpy()
        d= {'values':value[0][1:] }
        date=utils.toDateTime(data.columns[1:])
        df=pd.DataFrame(data=d, index=date)
        return df
    
    def check_non_stationarity(adf_result):
        critical_value= adf_result[0]
        p_value= adf_result[1]
        if p_value <=0.2:
            return False
        at_10= adf_result[4]['10%']
        at_5= adf_result[4]['5%']
        at_1= adf_result[4]['1%']
        if  critical_value< max(at_10,at_5,at_1):
            return False
        else:
            return True

    def stationary_df(df: pd.DataFrame):
        return df
        
    
    def normalize_df(df: pd.DataFrame):
        for col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.interpolate(axis=1, limit_direction='forward')
        for c in df.columns:
            data=df.loc[df.first_valid_index():,c]
            base=data[df.first_valid_index()]
            ans=[]
            for d in data.values:
                v= abs(d-base)/base
                ans.append(v)
            df.loc[df.first_valid_index():,c]=ans
        return df

        



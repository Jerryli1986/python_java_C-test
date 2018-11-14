#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Jerry
"""

# question 5

import pandas as pd
from datetime import datetime



def date_format_convert(str):
  '''judge the date type'''
  try:
    # original date format is "06-Jun-16"
    datetime.strptime(str, "%d-%b-%y")
    return datetime.strptime(str, "%d-%b-%y").date()
  except:
      try:
        # original date format is "07-06-16"
        datetime.strptime(str, "%d-%m-%y")  
        return datetime.strptime(str, "%d-%m-%y").date()
      except ValueError:
        print("date format is invalid and not be converted")

def date_uniform(df,date_column_name):
    datelist=[]
    for date in df[date_column_name] :
        datelist.append(date_format_convert(date))
    df["Date"]=datelist
    return df

# =============================================================================
 
class Timeseries(object):
    def __init__(self, Dates, Prices):
        self.Dates=Dates
        self.Prices = Prices
#     # method
    def subtimeseries(self,Beg,End):
         output=[]
         index=(self.Dates>=Beg)&(self.Dates<=End)
         output=pd.DataFrame(list(self.Prices.loc[index]),columns=["Prices"],index=self.Dates.loc[index])
         print(output)
         return output
    def AnnualizedReturn(self,Beg,End):
        # calculate day return and then annualized
        # using first method in class
        subdata=Timeseries.subtimeseries(self,Beg,End)
        initial_price=subdata.values[0][0]
        r_days=0
        for line in subdata.values[1:] :
            r=line[0]/initial_price-1
            initial_price=line[0]
            r_days=(1+r)*(1+r_days)-1
        n=len(subdata[1:])
        AnnualizedReturn=round(((r_days+1)**(365.0/n)-1)*100,2)
        print('Annualized Return: {0}%'.format(AnnualizedReturn))
        return AnnualizedReturn
        
# =============================================================================

# the main
if __name__=="__main__":
   # please change the file address
  file=r'/Users/jerry/Documents/GitHub/python_java_C-test/Time Series.csv'
  
  # parameters
  Begin_day='2017-08-01'
  End_day='2018-03-01'
  
  ######################################
  Beg=datetime.strptime(Begin_day,"%Y-%m-%d").date()
  End=datetime.strptime(End_day,"%Y-%m-%d").date()
  
  df = pd.read_csv(file,  header=[0])
  # convert all date to standard date form and increase a column for date
  df=date_uniform(df,'Unnamed: 0')
  # two time series price data
  SP500_df=pd.DataFrame(df,columns=['Date','S&P 500 Price'])
  DAX_df=pd.DataFrame(df,columns=['Date','DAX Price'])
  
  # for example play with SP500
  data=SP500_df
  
  if Beg<data.Date[0] or End>data.Date.iloc[-1]:
     print("Please select right date within the period of records!!!")
  else :
     # play with class methods
     TS_obj=Timeseries(data.iloc[:,0],data.iloc[:,1])
     TS_obj.subtimeseries(Beg,End)
     TS_obj.AnnualizedReturn(Beg,End)
  
  


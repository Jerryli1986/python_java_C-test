#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
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
    
def YTD(df):
    YTD_return=0
    # use last row to get current year
    current_year=df.index[-1].year
    index=datetime(current_year,1,1).date()
    column_name=df.columns.values[0]
    # the price of first day in current year
    Price_Begin=df[column_name][index]
    # the price of last record in current year
    Price_End=df.values[-1][0]
    YTD_return=round((Price_End/Price_Begin-1)*100,2)
    print ('YTD return of {0} : {1}%'.format(column_name,YTD_return))
def Total_Net_return(df) :
    column_name=df.columns.values[0]
    # the price of first record in whole time series
    Price_Begin=df.values[0][0]
    # the price of last record in whole time series
    Price_End=df.values[-1][0]
    TNR_return=round((Price_End/Price_Begin-1)*100,2)
    print ('Total Net Return of {0} : {1}%'.format(column_name,TNR_return))
def Compounded_Annually(df):
    Begin_year=df.index[0].year
    End_year=df.index[-1].year
    column_name=df.columns.values[0]
    annual_return_list=[]
    comp_annually=0
    for year in range(Begin_year,End_year+1):
        beg_index=max(datetime(year,1,1).date(),df.index[0])
        end_index=min(datetime(year,12,31).date(),df.index[-1])
        r=df[column_name][end_index]/df[column_name][beg_index]-1
        annual_return_list.append(r)
        comp_annually=(1+r)*(1+comp_annually)-1
    comp_annually=round(comp_annually,2)*100
    print ('Compounded_Annually of {0} : {1}%'.format(column_name,comp_annually))
def Max_Drawdown(df):
    column_name=df.columns.values[0]
    maximums = np.maximum.accumulate(df[column_name])
    drawdowns = 1 - df[column_name] / maximums
    #plt.plot(df[column_name])
    #plt.show()
    max_drawdown=round(np.max(drawdowns)*100,2)
    print ('Max Drawdown of {0} : {1}%'.format(column_name,max_drawdown))

def last_day_of_month(year,month):
    last_days = [31, 30, 29, 28, 27]
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date()
    return None

def monthly_return(df):
    Begin_year=df.index[0].year
    End_year=df.index[-1].year
    column_name=df.columns.values[0]
    month_return_list=[]
    for year in range(Begin_year,End_year+1):
        beg_index=max(datetime(year,1,1).date(),df.index[0])
        end_index=min(datetime(year,12,31).date(),df.index[-1])
        df_year=df[column_name][beg_index:end_index]
        Begin_month=df_year.index[0].month
        End_month=df_year.index[-1].month 
        for month in range(Begin_month,End_month+1) :
          last_day=last_day_of_month(year,month)
          beg_month_index=max(datetime(year,month,1).date(),df_year.index[0])
          end_month_index=min(last_day,df_year.index[-1])
          df_month=df_year[beg_month_index:end_month_index]
          r=df_month[-1]/df_month[0]-1
          month_return_list.append(r)
    return  month_return_list 

def monthlized_return(array):
    r=0
    for i in range(len(array)):
       r=(1+array[i])*(r+1)-1
    return (r+1)**(1.0/len(array))-1
      
def Annualized_Sharpe_Ratio(df):
    column_name=df.columns.values[0]
    month_return_list= monthly_return(df)
    monthlized_r=monthlized_return(month_return_list)
    std=np.std(month_return_list)
    # assume rf=0
    # use month sharpe to calculate year sharpe by multiplying sqrt(12)
    rf=0.0
    month_Sharpe_ratio=(monthlized_r-rf)/std
    Annualized_Sharpe_Ratio=round((12)**(1.0/2)*(month_Sharpe_ratio),2)
    print ('Annualized Sharpe Ratio of {0} : {1}'.format(column_name,Annualized_Sharpe_Ratio))
    
def Sortino_Ratio(df) :
    column_name=df.columns.values[0]
    month_return_list=np.array(monthly_return(df))
    #Define the minimum acceptable monthly return (MAR)=0.0
    mar=0.0
    monthlized_r=monthlized_return(month_return_list)
    month_return_list[month_return_list>mar]=0
    std=np.std(month_return_list)
    month_Sortino_ratio=round((monthlized_r-mar)/std,2)
    print ('Monthly Sortino Ratio of {0} : {1}'.format(column_name,month_Sortino_ratio))
def Omega_Ratio(df):
    # assume the same probability for each monthly return
    # assume the mar=0.0
    mar=0.0
    column_name=df.columns.values[0]
    month_return_list=np.array(monthly_return(df))
    month_upside=month_return_list[month_return_list>=mar]-mar
    month_downside=mar-month_return_list[month_return_list<mar]
    OmegaRatio=round(sum(month_upside)/sum(month_downside),2)
    print ('Omega Ratio of {0} : {1}'.format(column_name,OmegaRatio))
    
def Annual_Volatility(df):
    column_name=df.columns.values[0]
    month_return_list= monthly_return(df)
    year_std=round(np.std(month_return_list)*(12)**(1.0/2),2)
    print ('Annual Volatility of {0} : {1}'.format(column_name,year_std))
def Downside_Deviation(df):
    column_name=df.columns.values[0]
    month_return_list=np.array(monthly_return(df))
    #Define the minimum acceptable monthly return (MAR)=0.0
    mar=0.0
    month_return_list[month_return_list>mar]=0
    month_down_std=round(np.std(month_return_list),2)
    print ('Monthly Downside Deviation of {0} : {1}'.format(column_name,month_down_std))
def Positive_Period(df) :
    column_name=df.columns.values[0]
    # assume price in the day before first day is the same with the first day
    initial=df.values[0][0]
    positive_day,negative_day=0,0
    for index in list(df.index) :
        lastday_price=initial
        key=df[column_name][index]/lastday_price-1
        if key>0 :
            positive_day=positive_day+1
        else :
            negative_day=negative_day+1
        initial=df[column_name][index]
    postive_period_=round(positive_day/(positive_day+negative_day)*100,2)  
    print ('% Postive period of {0} : {1}%'.format(column_name,postive_period_))    
def Average_Gain_Lost(df):
    column_name=df.columns.values[0]
    month_return_list=np.array(monthly_return(df))
    month_gain=month_return_list[month_return_list>0]
    month_lost=month_return_list[month_return_list<0]
    Average_gain=round(sum(month_gain)/len(month_gain)*100,2)
    Average_lost=round(sum(month_lost)/len(month_lost)*100,2)
    print ('Average Gain of {0} : {1}%'.format(column_name,Average_gain))
    print ('Average Lost of {0} : {1}%'.format(column_name,Average_lost))    
def Skewness(df):
    column_name=df.columns.values[0]
    month_return_list=np.array(monthly_return(df))
    month_mean=np.mean(month_return_list)
    std=np.std(month_return_list)
    sum_3=sum((month_return_list-month_mean)**3)
    skewness=round(sum_3/(len(month_return_list)*std**3),2)
    print ('Skewness of {0} : {1}'.format(column_name,skewness))

def Correlation(df1,df2):
    column_name1=df1.columns.values[0]
    column_name2=df2.columns.values[0]
    mean1 = df1.mean()[0] 
    mean2 = df2.mean()[0]
    std1 = df1.std()[0]
    std2 = df2.std()[0]

    # corr = ((data1-mean1)*(data2-mean2)).mean()/(std1*std2)
    corr = round(((df1.values*df2.values).mean()-mean1*mean2)/(std1*std2),2)
    print ('Correlation of {0} and {1}: {2}'.format(column_name1,column_name2,corr))
def Beta(df1,df2) :
    # assum df1 as a stock and df2 as market index
    column_name1=df1.columns.values[0]
    column_name2=df2.columns.values[0]
    y=np.array(monthly_return(df1))
    X=np.array(monthly_return(df2))
    
    X = sm.add_constant(X) #  add an intercept 
    # linear regression
    model = sm.OLS(y, X).fit()
    Beta_=round(model.params[1],2)
    print ('Beta of {0} related to market index {1} is: {2}'.format(column_name1,column_name2,Beta_))

def plot_series(df1,df2):
    column_name1=df1.columns.values[0]
    column_name2=df2.columns.values[0]
    return_df1=np.array(monthly_return(df1))
    return_df2=np.array(monthly_return(df2))
    periods=len(pd.date_range(df1.index[0],df1.index[-1],freq='M'))+1
    index=pd.date_range(df1.index[0],periods=periods,freq='M')
    fig=plt.figure(figsize=(8, 4))
    ax = plt.gca()
    years = plt.matplotlib.dates.YearLocator()
    months = plt.matplotlib.dates.MonthLocator()
    yearsFmt = plt.matplotlib.dates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_ylabel("Monthly Return")
    title="Monthly return of {0} and {1}".format(column_name1,column_name2)
    plt.suptitle(title)
    ax.plot(index,return_df1,label=column_name1)
    ax.plot(index,return_df2,label=column_name2)
    plt.legend((column_name1, column_name2),
    loc='upper right')
    plt.show()
    fig.savefig('question1_plot.png')
def all_functions(df) :
    YTD(df)
    Total_Net_return(df)
    Compounded_Annually(df)
    Max_Drawdown(df)
    Annualized_Sharpe_Ratio(df)
    Sortino_Ratio(df) 
    Omega_Ratio(df)
    Annual_Volatility(df)
    Positive_Period(df)
    Average_Gain_Lost(df)
    Skewness(df)
    print('--------------------------------')
    
 
if __name__=="__main__":
    # Please change the file address only
    df = pd.read_csv("/Users/jerry/Documents/GitHub/python_java_C-test/Time Series.csv",  header=[0])
    
    #####################################################
    # convert all date to standard date form and increase a column for date
    df=date_uniform(df,'Unnamed: 0')
    # two time series price data and date will be index
    SP500_df=pd.DataFrame(df,columns=['Date','S&P 500 Price'])
    SP500_df.set_index('Date', inplace=True)
    DAX_df=pd.DataFrame(df,columns=['Date','DAX Price'])
    DAX_df.set_index('Date', inplace=True)
    # all calculation
    for df_i in list([SP500_df,DAX_df]) :
       all_functions(df_i)
    Correlation(SP500_df,DAX_df)
    Beta(SP500_df,DAX_df) 
    plot_series(SP500_df,DAX_df)
    
    
    
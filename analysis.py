# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 14:33:38 2021

@author: eberly
"""
#
# DIB Financial Analysis
#

# Date: 6.14.2021
# Data Source: SEC Filings & Yahoo Finance Premier .csv reports
# .csv reports downloaded on 6.13.2021

import pandas as pd
import numpy as np

# Companies of interest
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

#%%

# import pickle file
measures=pd.read_pickle("measures_qtrly.pkl.zip")
stock_info=pd.read_pickle("stock_info.pkl.zip")

#%%

# Create ROE and ROA Variables
measures["ROA"] = measures["NetIncome"]/measures["TotalAssets"]
measures["ROE"] = measures["NetIncome"]/measures["StockholdersEquity"]

#%%
#
# isolate time frames
#

financials_10yr = measures.query("date > '2010-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
financials_5yr = measures.query("date > '2016-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
financials_3yr = measures.query("date > '2018-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
financials_1yr = measures.query("date > '2020-01-29 00:00:00' and date < '2021-06-11 00:00:00'")

stocks_10yr = stock_info.query("Date > '2010-01-29 00:00:00' and Date < '2021-06-11 00:00:00'")
stocks_5yr = stock_info.query("Date > '2016-01-29 00:00:00' and Date < '2021-06-11 00:00:00'")
stocks_3yr = stock_info.query("Date > '2018-01-29 00:00:00' and Date < '2021-06-11 00:00:00'")
stocks_1yr = stock_info.query("Date > '2020-01-29 00:00:00' and Date < '2021-06-11 00:00:00'")

#%%

##
## Accounts Payable Turnover Ratios
##

# To help w/calculations... created smaller dataframe to drop NaN
 
AP = financials_10yr[['CostOfRevenue','AccountsPayable']]
print ( AP )

# Keep only records with data
AP = AP.dropna()
print( AP )

#
# Calculate Ratios with 'for' loop
#

# Used loop because I couldn't figure out how to do it with groupby()


apt = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = AP.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
   
    # reset index because of trouble doing .diff() calc w/ 'date' in the index
    temp = temp.reset_index()
    temp['days'] = temp['date'].diff()
        # convert nanoseconds to days
    temp['days'] = temp['days'].astype('timedelta64[D]')
  
    ## Accounts Payable Turnover Ratio

    # calculate average for AccountsPayable (column #3) 
        # current & previous row is window=2  
    temp['APT_period_ave'] =  temp.iloc[:,3].rolling(window=2).mean()

    #  calculate ratio
    temp['APT'] = temp['CostOfRevenue'] / temp['APT_period_ave']

    # reset index to date
    temp = temp.set_index('date')
  
    ## Accounts Payable Turnover Ratio DAYS
 
    temp['APT_days'] = temp['days'] / temp['APT'] 

    apt = apt.append( temp )
    
print ( apt )

#%%

##
## Import & format R&D data
##

data_type = {'filing': str, 'ticker':str}
RD_data = pd.read_csv('R&D_data.csv', dtype = data_type)

#  Format data types
RD_data.dtypes
RD_data['Date'] = pd.to_datetime(RD_data['Date'])   # keep only the date, remove hr/min/sec
RD_data['Date'] = RD_data['Date'].dt.date   # keep only the date, remove hr/min/sec
RD_data.dtypes

#%%

##
## Stock - Normalize Stock prices & calculate ROI 
##

#%%

#
#  Stock Calcs - 10 YR 
#

# Normalize stock price plus ROI
stock_info_10yr = pd.DataFrame()

# To collect final ROI
finalROIs = pd.DataFrame()
    # My vision for 'finalROIs' is:
            #           10yrROI     10yrROI_including Dividends .... 5yrROI
            # Ticker
            # LMT
            # BA
            # ...
            # GE
print('If you purchased 1 stock in 2/2011 & sold it in 6/2021.')

for ticker in companies:
  
    tick = ticker
    temp = stocks_10yr.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # sort data  
    temp = temp.sort_index( ascending= False )
    # select last row
    start_date = temp.iloc[-1]
    # normalize stock based on start date
    temp['norm_close'] = temp['Close']/start_date['Close']

    # calculate ROI with $100 dollar investment
    temp['ROI'] = 100* (( temp['Close'] - start_date['Close'] ) / start_date['Close'] )
    
    stock_info_10yr = stock_info_10yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    total_ROI = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    
    print('Stock:',tick,
          '| ROI:', round(end_date['ROI']),
          '%| ROI plus dividends', round(total_ROI),"%")
    #finalROI_10yr = finalROI_10yr.append( total_ROI )
    
#print( stock_info_10yr )

#%%
#
#  Stock Calcs - 5 YR 
#

# Normalize stock price plus ROI
stock_info_5yr = pd.DataFrame()

print('If you purchased 1 stock in 2/2016 & sold it in 6/2021.')

for ticker in companies:
  
    tick = ticker
    temp = stocks_5yr.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # sort data  
    temp = temp.sort_index( ascending= False )
    # select last row
    start_date = temp.iloc[-1]
    # normalize stock based on start date
    temp['norm_close'] = temp['Close']/start_date['Close']

    # calculate ROI with $100 dollar investment
    temp['ROI'] = 100* (( temp['Close'] - start_date['Close'] ) / start_date['Close'] )
    
    stock_info_5yr = stock_info_5yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    total_ROI = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    
    print('Stock:',tick,
          '| ROI:', round(end_date['ROI']),
          '%| ROI plus dividends', round(total_ROI),"%")

#print( stock_info_5yr )

#%%
#
#  Stock Calcs - 3 YR 
#

# Normalize stock price plus ROI
stock_info_3yr = pd.DataFrame()

print('If you purchased 1 stock in 2/2018 & sold it in 6/2021.')

for ticker in companies:
  
    tick = ticker
    temp = stocks_3yr.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # sort data  
    temp = temp.sort_index( ascending= False )
    # select last row
    start_date = temp.iloc[-1]
    # normalize stock based on start date
    temp['norm_close'] = temp['Close']/start_date['Close']

    # calculate ROI with $100 dollar investment
    temp['ROI'] = 100* (( temp['Close'] - start_date['Close'] ) / start_date['Close'] )
    
    stock_info_3yr = stock_info_3yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    total_ROI = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    
    print('Stock:',tick,
          '| ROI:', round(end_date['ROI']),
          '%| ROI plus dividends', round(total_ROI),"%")

#print( stock_info_5yr )

#%%
#
#  Stock Calcs - 1 YR 
#

# Normalize stock price plus ROI
stock_info_1yr = pd.DataFrame()

print('If you purchased 1 stock in 2/2020 & sold it in 6/2021.')

for ticker in companies:
  
    tick = ticker
    temp = stocks_1yr.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # sort data  
    temp = temp.sort_index( ascending= False )
    # select last row
    start_date = temp.iloc[-1]
    # normalize stock based on start date
    temp['norm_close'] = temp['Close']/start_date['Close']

    # calculate ROI with $100 dollar investment
    temp['ROI'] = 100* (( temp['Close'] - start_date['Close'] ) / start_date['Close'] )
    
    stock_info_1yr = stock_info_1yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    total_ROI = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    
    print('Stock:',tick,
          '| ROI:', round(end_date['ROI']),
          '%| ROI plus dividends', round(total_ROI),"%")

#print( stock_info_5yr )


#%%

#
# ROA & ROE
#

#%%

#
# 10 yr
#

norm = financials_10yr[['ROA','ROE']]

# Keep only records with data
norm = norm.dropna()

# Normalize ROA and ROE based on first quarter 
norm_fin_10yr = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = norm.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # normalize 
    temp1 = temp.xs('2011-03-31 00:00:00')
    temp['norm_ROA'] = temp['ROA']/temp1['ROA']
    temp['norm_ROE'] = temp['ROE']/temp1['ROE']
    
    norm_fin_10yr = norm_fin_10yr.append( temp )
    
print ( norm_fin_10yr )


#%%

#
# 5 yr
#

norm = financials_5yr[['ROA','ROE']]

# Keep only records with data
norm = norm.dropna()

# Normalize ROA and ROE based on first quarter
norm_fin_5yr = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = norm.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # normalize 
    temp1 = temp.xs('2016-03-31 00:00:00')
    temp['norm_ROA'] = temp['ROA']/temp1['ROA']
    temp['norm_ROE'] = temp['ROE']/temp1['ROE']
    
    
    norm_fin_5yr = norm_fin_5yr.append( temp )
    
print ( norm_fin_5yr )

#%%
#
# 10 yr
#

norm = financials_3yr[['ROA','ROE']]

# Keep only records with data
norm = norm.dropna()

# Normalize ROA and ROE based on first quarter
norm_fin_3yr = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = norm.query("ticker == @tick")
    temp = temp.copy()  # .copy() needed fix Pandas Error when calculating
    
    # normalize 
    temp1 = temp.xs('2018-03-31 00:00:00')
    temp['norm_ROA'] = temp['ROA']/temp1['ROA']
    temp['norm_ROE'] = temp['ROE']/temp1['ROE']
    
    norm_fin_3yr = norm_fin_3yr.append( temp )
    
print ( norm_fin_3yr )
#%%
#
# 10 yr
#

norm = financials_1yr[['ROA','ROE']]

# Keep only records with data
norm = norm.dropna()

# Normalize ROA and ROE based on first quarter
norm_fin_1yr = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = norm.query("ticker == @tick")
    temp = temp.copy()
    
    # normalize 
    temp1 = temp.xs('2020-03-31 00:00:00')
    temp['norm_ROA'] = temp['ROA']/temp1['ROA']
    temp['norm_ROE'] = temp['ROE']/temp1['ROE']
    
    norm_fin_1yr = norm_fin_1yr.append( temp )
    
print ( norm_fin_1yr )
#%%
#Pickle dfs for plotting in another file

norm_fin_1yr.to_pickle("norm_fin_1yr.pkl")
norm_fin_3yr.to_pickle("norm_fin_3yr.pkl")
norm_fin_5yr.to_pickle("norm_fin_5yr.pkl")
norm_fin_10yr.to_pickle("norm_fin_10yr.pkl")

financials_1yr.to_pickle("financials_1yr.pkl")
financials_3yr.to_pickle("financials_3yr.pkl")
financials_5yr.to_pickle("financials_5yr.pkl")
financials_10yr.to_pickle("financials_10yr.pkl")

stock_info_1yr.to_pickle("stocks_1yr.pkl")
stock_info_3yr.to_pickle("stocks_3yr.pkl")
stock_info_5yr.to_pickle("stocks_5yr.pkl")
stock_info_10yr.to_pickle("stocks_10yr.pkl")

apt.to_pickle('apt.pkl')

RD_data.to_pickle('RD_data.pkl')

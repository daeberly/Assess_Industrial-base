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

# Run this file after '1_inputs.py' & before '3_plots.py'

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

start_time = datetime.datetime.now()

# Companies of interest
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

#%%

# import pickle files

measures = pd.read_pickle("clean_data/measures_qtrly.pkl.zip")
stock_info = pd.read_pickle("clean_data/stock_info.pkl.zip")
monthly = pd.read_pickle("clean_data/measures_monthly.pkl.zip")

# import, set data types & export Research & Development data
data_type = {'filing': str, 'ticker':str}
rd_data = pd.read_csv('clean_data/R&D_data.csv', dtype = data_type, parse_dates=(['Date']))
rd_data.to_pickle( 'clean_data/R&D_data.pkl' )
rd_data.dtypes

#%%

# Create ROE and ROA Variables
measures["ROA"] = measures["NetIncome"]/measures["TotalAssets"]
measures["ROE"] = measures["NetIncome"]/measures["StockholdersEquity"]

#%%
#
# Isolate timeframes
#

# Timeframes

# Created with TODAY = 2021-6-14 00:00:00

# End Date
    # set to 6/14 so results don't change as we write the report
today = pd.to_datetime('2021-06-14 00:00:00')

    # future analysis use the next line...
#today = datetime.datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0) 

# Start Date per timeframe
one_year = datetime.datetime.today() + relativedelta(years=-1)
one_year = one_year.replace(hour=0, minute=0, second=0, microsecond=0) 

three_year = datetime.datetime.today() + relativedelta(years=-3)
three_year = three_year.replace(hour=0, minute=0, second=0, microsecond=0) 

five_year = datetime.datetime.today() + relativedelta(years=-5)
five_year = five_year.replace(hour=0, minute=0, second=0, microsecond=0) 

ten_year = datetime.datetime.today() + relativedelta(years=-10)
ten_year = ten_year.replace(hour=0, minute=0, second=0, microsecond=0) 

#
# Create timeframes from files
#
financials_10yr = measures.query("date > '2011-01-31 00:00:00' and date < @today ")
financials_5yr = measures.query("date > '2016-01-31 00:00:00' and date < @today ")
financials_3yr = measures.query("date > '2018-01-31 00:00:00' and date < @today ")
financials_1yr = measures.query("date > '2020-01-31 00:00:00' and date < @today ")

stocks_10yr = stock_info.query("Date > @ten_year and Date < @today " )
stocks_5yr = stock_info.query( "Date > @five_year and Date < @today " )
stocks_3yr = stock_info.query( "Date > @three_year and Date < @today "  )
stocks_1yr = stock_info.query( "Date > @one_year and Date < @today " )

monthly_10yr = monthly.query( "date > @ten_year and date < @today ")
monthly_5yr = monthly.query( "date > @five_year and date < @today ")
monthly_3yr = monthly.query( "date > @three_year and date < @today ")
monthly_1yr = monthly.query( "date > @one_year and date < @today " )

#%%

##
## Accounts Payable Turnover Ratios
##

# To help w/calculations... created smaller dataframe to drop NaN
 
AP = financials_10yr[['CostOfRevenue','AccountsPayable']]
#print ( AP )

# Keep only records with data
AP = AP.dropna()
#print( AP )

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
    temp['days'] = -1* temp['date'].diff()
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
    
#print ( apt )
apt.to_pickle('clean_data/apt.pkl')


    
#%%

################
## Stock & ROIs - Normalize Stock prices & calculate ROI 
################


# collect ROIs for all timeframes
all_ROIs = pd.DataFrame( companies, columns= ['ticker'] )

####
#
#  Stock & ROI Calcs - 10 YR 
#

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX', 'SPX']

#print('If you purchased 1 stock in 2/2011 & sold it in 6/2021.')


# Normalize stock price plus ROI
stock_info_10yr = pd.DataFrame()

# To collect ROIs
roi = []
roi_div = []
roi_diff= []

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
    
    # append new dataframe
    stock_info_10yr = stock_info_10yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    temp_roi_div = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    temp_roi = end_date['ROI']
    
    # difference between ROI w/ & w/o dividends
    diff =  (temp_roi_div-temp_roi)

    # add ROIs to list
    roi.append( temp_roi )
    roi_div.append( temp_roi_div )
    roi_diff.append( diff )

# Create ROI dictionaries

dic_roi = dict(zip(companies,roi))
dic_roi_div = dict(zip(companies,roi_div))
dic_roi_diff = dict(zip(companies, roi_diff ))

# Add dictionaries to dataframe

all_ROIs['roi_10yr'] = all_ROIs['ticker'].map( dic_roi )
all_ROIs['roi_div_10yr'] = all_ROIs['ticker'].map( dic_roi_div )
all_ROIs['roi_%diff_10yr'] = all_ROIs['ticker'].map( dic_roi_diff )

#%%

####
#
#  Stock & ROI Calcs - 5 YR 
#

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX', 'SPX']

#print('If you purchased 1 stock in 2/2016 & sold it in 6/2021.')

# Normalize stock price plus ROI
stock_info_5yr = pd.DataFrame()

# To collect ROIs
roi = []
roi_div = []
roi_diff = []

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
    temp_roi_div = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    temp_roi = end_date['ROI']

    # difference between ROI w/ & w/o dividends
    diff =  (temp_roi_div-temp_roi)
    
    # add ROIs to list
    roi.append( temp_roi )
    roi_div.append( temp_roi_div )
    roi_diff.append( diff )

# Create ROI dictionaries

dic_roi = dict(zip(companies,roi))
dic_roi_div = dict(zip(companies,roi_div))
dic_roi_diff = dict(zip(companies, roi_diff ))

# Add dictionaries to dataframe

all_ROIs['roi_5yr'] = all_ROIs['ticker'].map( dic_roi )
all_ROIs['roi_div_5yr'] = all_ROIs['ticker'].map( dic_roi_div )
all_ROIs['roi_%diff_5yr'] = all_ROIs['ticker'].map( dic_roi_diff )

#%%

####
#
#  Stock & ROI Calcs - 3 YR 
#

# 'SPX' removed because data stops at 2018. No 2019 or 2020 data.
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

#print('If you purchased 1 stock in 2/2016 & sold it in 6/2021.')

# Normalize stock price plus ROI
stock_info_3yr = pd.DataFrame()

# To collect ROIs
roi = []
roi_div = []
roi_diff = []

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
    temp_roi_div = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    temp_roi = end_date['ROI']

    # difference between ROI w/ & w/o dividends
    diff =  (temp_roi_div-temp_roi)
    
    # add ROIs to list
    roi.append( temp_roi )
    roi_div.append( temp_roi_div )
    roi_diff.append( diff )

# Create ROI dictionaries

dic_roi = dict(zip(companies,roi))
dic_roi_div = dict(zip(companies,roi_div))
dic_roi_diff = dict(zip(companies, roi_diff ))

# Add dictionaries to dataframe

all_ROIs['roi_3yr'] = all_ROIs['ticker'].map( dic_roi )
all_ROIs['roi_div_3yr'] = all_ROIs['ticker'].map( dic_roi_div )
all_ROIs['roi_%diff_3yr'] = all_ROIs['ticker'].map( dic_roi_diff )


#%%


####
#
#  Stock & ROI Calcs - 1 YR 
#

# 'SPX' removed because data stops at 2018. No 2019 or 2020 data.
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

#print('If you purchased 1 stock in 2/2020 & sold it in 6/2021.')

# Normalize stock price plus ROI
stock_info_1yr = pd.DataFrame()

# To collect ROIs
roi = []
roi_div = []
roi_diff = []

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
    
    stock_info_1yr = stock_info_1yr.append( temp )
    
    # total ROI plus dividends
    end_date = temp.iloc[0]
    temp_roi_div = 100* (( end_date['Close'] - start_date['Close'] + temp['Dividends'].sum()) / start_date['Close'] )
    temp_roi = end_date['ROI']

    # difference between ROI w/ & w/o dividends
    diff =  (temp_roi_div-temp_roi)
    
    # add ROIs to list
    roi.append( temp_roi )
    roi_div.append( temp_roi_div )
    roi_diff.append( diff )

# Create ROI dictionaries

dic_roi = dict(zip(companies,roi))
dic_roi_div = dict(zip(companies,roi_div))
dic_roi_diff = dict(zip(companies, roi_diff ))

# Add dictionaries to dataframe

all_ROIs['roi_1yr'] = all_ROIs['ticker'].map( dic_roi )
all_ROIs['roi_div_1yr'] = all_ROIs['ticker'].map( dic_roi_div )
all_ROIs['roi_%diff_1yr'] = all_ROIs['ticker'].map( dic_roi_diff )

#%%
####
#
# Export files
#


all_ROIs = all_ROIs.set_index('ticker')
all_ROIs.to_pickle('clean_data/ROI_table.pkl')

stock_info_1yr.to_pickle("clean_data/stocks_1yr.pkl")
stock_info_3yr.to_pickle("clean_data/stocks_3yr.pkl")
stock_info_5yr.to_pickle("clean_data/stocks_5yr.pkl")
stock_info_10yr.to_pickle("clean_data/stocks_10yr.pkl")

#%%

#
# ROA & ROE
#

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

#
# 10 yr
#

norm = financials_10yr[['ROA','ROE']]

financials_10yr.dtypes
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
    
#print ( norm_fin_10yr )


#%%

#
# 5 yr
#
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    
#print ( norm_fin_5yr )

#%%
#
# 3 yr
#
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    
#print ( norm_fin_3yr )

#%%
#
# 1 yr
#
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

norm = financials_1yr[['ROA','ROE']]

# Keep only records with data
norm = norm.dropna()

# Normalize ROA and ROE based on first quarter
norm_fin_1yr = pd.DataFrame()

for ticker in companies:
  
    tick = ticker
    temp = norm.query("ticker == @tick")
    temp = temp.copy()
    temp = temp.sort_index( ascending= False )

    # normalize 
    temp1 = temp.xs('2020-03-31 00:00:00')
    temp['norm_ROA'] = temp['ROA']/temp1['ROA']
    temp['norm_ROE'] = temp['ROE']/temp1['ROE']
    
    norm_fin_1yr = norm_fin_1yr.append( temp )
    
#print ( norm_fin_1yr )

#%%

#
# Pickle dfs for plotting in another file
#

# Normalized Financials
norm_fin_1yr.to_pickle("clean_data/norm_fin_1yr.pkl")
norm_fin_3yr.to_pickle("clean_data/norm_fin_3yr.pkl")
norm_fin_5yr.to_pickle("clean_data/norm_fin_5yr.pkl")
norm_fin_10yr.to_pickle("clean_data/norm_fin_10yr.pkl")

sample = norm_fin_10yr.sample(frac=0.2)
sample.to_csv("clean_data/sample_norm_fin_10yr.csv")

# Financials
financials_1yr.to_pickle("clean_data/financials_1yr.pkl")
financials_3yr.to_pickle("clean_data/financials_3yr.pkl")
financials_5yr.to_pickle("clean_data/financials_5yr.pkl")
financials_10yr.to_pickle("clean_data/financials_10yr.pkl")

sample = financials_10yr.sample(frac=0.2)
sample.to_csv("clean_data/sample_financials_10yr.csv")

# Stock Info
stock_info_1yr.to_pickle("clean_data/stocks_1yr.pkl")
stock_info_3yr.to_pickle("clean_data/stocks_3yr.pkl")
stock_info_5yr.to_pickle("clean_data/stocks_5yr.pkl")
stock_info_10yr.to_pickle("clean_data/stocks_10yr.pkl")

sample = stock_info_10yr.sample(frac=0.2)
sample.to_csv("clean_data/sample_stock_info_10yr.csv")

# Monthly financials
monthly_10yr.to_pickle("clean_data/monthly_10yr.pkl")
monthly_5yr.to_pickle("clean_data/monthly_5yr.pkl")
monthly_3yr.to_pickle("clean_data/monthly_3yr.pkl")
monthly_1yr.to_pickle("clean_data/monthly_1yr.pkl")

sample = monthly_10yr.sample(frac=0.2)
sample.to_csv("clean_data/sample_monthly_10yr.csv")

# Accounts Payable Turnover
apt.to_pickle('clean_data/apt.pkl')

sample = apt.sample(frac=0.2)
sample.to_csv("clean_data/sample_apt.csv")

# Shareholder ROI calc
all_ROIs.to_pickle('clean_data/ROI_table.pkl')

sample = all_ROIs.sample(frac=0.2)
sample.to_csv("clean_data/sample_ROI_table.csv")

#%%

#
# Housekeeping
#

print( '\nPart 2 = Great Success! Analysis & files exported.')

end_time = datetime.datetime.now()

time_diff = (end_time - start_time)

print('\nTotal Processing Time:', time_diff, 'hr:min:secs\n')
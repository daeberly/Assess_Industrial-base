# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 18:04:46 2021

@author: eberly
"""
#
# Defense Industrial Base (DIB)
#


# Date: 6.13.2021
# Data Source: SEC Filings & Yahoo Finance Premier .csv reports
# .csv reports downloaded on 6.13.2021

import glob           # help: https://pynative.com/python-glob/
import pandas as pd
import os
import re             # used in back-up at bottom of file
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

start = time.time()

# Results:
    # 'DIB_Financials' dataframe (2021-1985) includes:
        # fundamentals, cash flow, balance sheet & valuation measures
    # 'stock_info' dataframe (2021 ~ 1980s) includes:
        # open, high, low, close, volume, dividend per stock, stock split

# today's date for exporting files
current = datetime.date.today()

#%%
# 
# Stock info (2021 to ~1980s)
#   open, high, low, close, volume, dividend per stock, stock split

# Reference: https://pypi.org/project/yfinance/#description

#pip install yfinance
import yfinance as yf

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']#,'SPX', 'SPSIAD']
    # SPX = S&P 500 index.  SPIAD = S&P 500 Aerospace & Defense Index

stock_info = pd.DataFrame()

for ticker in companies:
    tick  = yf.Ticker(ticker)
    stock_hist = tick.history(period="max")
    stock_hist['ticker'] = ticker
    stock_info = stock_info.append( stock_hist )

print('\n', stock_info.sample(10))
stock_info.columns

# set index
stock_info = stock_info.reset_index() 
stock_info = stock_info.set_index(['Date', 'ticker'])

# ready for .groupby()

sample = stock_info.sample(1000)
sample.to_csv(str(current) + '_sample_stock_info.csv')
    
#%%

#
# Combined Financials Sheets (Years 2021-1985)
#

# columns to keep: 'AccountsPayable', 'CommonStockDividendPaid',

# To DO:
    # delete 'ttm' entry since everything is quarterly & a 12-month total
    # clean columns names - remove tabs '\t'
    # plot measures
    # model - forecast
    # heatmap - correlation factors


DIB_Financials = pd.DataFrame()

path = "raw_data/*.csv"

for file in glob.glob(path, recursive = False):
    print(file) # visual cue for files imported 
    raw_data = pd.read_csv(file)
        # flip columns & rows
    raw_data = raw_data.transpose()
    
    # Clean table
        # pull out date from index & reset columns names
    raw_data = raw_data.reset_index()
    header_row = 0
    raw_data.columns = raw_data.iloc[header_row]
        # delete row used for header
    raw_data = raw_data.drop([0])
        # fix date header
    rename = {'name': 'Date'}
    raw_data.rename(columns= rename, inplace= True)
        # prep string values for data type conversion
    sub_in = {',':'','nan':np.nan}     
    raw_data = raw_data.replace(sub_in, regex=True)
        # delete 'ttm' entries - trailing 12 months (ttm) will skew data
    raw_data = raw_data[~raw_data.Date.str.contains('ttm')]
        # convert string date to datetime
    date_type = {'Date': 'datetime64'}
    raw_data = raw_data.astype(date_type)
        # convert all columns to floats
    raw_data = raw_data.apply(pd.to_numeric)
        # convert date from float to datetime format
    date_type = {'Date': 'datetime64[ns]'}
    raw_data = raw_data.astype(date_type)

    # Add ticker symbol per row
        # pull company ticker symbol from filename
    ticker = os.path.splitext(os.path.basename(file))[0]
    ticker = ticker[:3]       
        # create a column with company ticker in each row
    raw_data ['ticker'] = ticker
                
    # Add this dataframe to main dataframe
    DIB_Financials = DIB_Financials.append(raw_data)

# remove all tabs '\t' from column header names
DIB_Financials.columns = DIB_Financials.columns.str.strip()

# set index
DIB_Financials = DIB_Financials.set_index(['Date','ticker'])

print('\n', DIB_Financials.sample(10))
print('\nFinancial Measures:', DIB_Financials.columns.to_list())


# ready for .groupby()


# export columns to .csv
sample = DIB_Financials.sample(100)
sample.to_csv(str(current) + '_sample_DIB_Financials.csv')

end = time.time()
print('\n Great Success! \nTotal Processing Time:', round(end-start,2), 'seconds\n')

#%%

# PLOTS....

#%%
'''
#
# Combine Financials... for a specific .csv report
#               (i.e. 'LMT_quarterly_balance-sheet.csv')
#

DIB_BalanceSheets = pd.DataFrame()

name = 'balance-sheet'
# [a-z] for any name followed by '_'
# {file_name} name
regex = r'[a-z_]+{file_name}.*'.format(file_name= name)

path = "raw_data/*.csv"

for file in glob.glob(path, recursive = False):
    if re.search(regex,file):
        print(file) # visual cue for files imported 
        raw_data = pd.read_csv(file)
            # flip columns & rows
        raw_data = raw_data.transpose()
        
        # Clean table
            # pull out date from index & reset columns names
        raw_data = raw_data.reset_index()
        header_row = 0
        raw_data.columns = raw_data.iloc[header_row]
        raw_data = raw_data.drop([0])
            # fix date header
        rename = {'name': 'Date'}
        raw_data.rename(columns= rename, inplace= True)
            # prep string values for data type conversion
        sub_in = {',':'','nan':np.nan}
        raw_data = raw_data.replace(sub_in, regex=True)
            # convert string date to datetime
        date_type = {'Date': 'datetime64'}
        raw_data = raw_data.astype(date_type)
            # convert all columns to floats
        raw_data = raw_data.apply(pd.to_numeric)
            # convert date from float to datetime format
        date_type = {'Date': 'datetime64[ns]'}
        raw_data = raw_data.astype(date_type)
    
        # Add ticker symbol per row
            # pull company ticker symbol from filename
        ticker = os.path.splitext(os.path.basename(file))[0]
        ticker = ticker[:3]       
            # create a column with company ticker in each row
        raw_data ['ticker'] = ticker
                    
        # Add this dataframe to main dataframe
        DIB_BalanceSheets = DIB_BalanceSheets.append(raw_data)

# fun fact: convert text 'ttm' into the date the file it came from was created
    # {'ttm':time.ctime(os.path.getctime(file))} #ttm = trailing 12 months   

'''

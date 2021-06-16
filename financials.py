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


# File has 3 sections that produce:

    #1 Quarterly - 'DIB_Financials' dataframe (2021-1985) includes:
        # fundamentals, cash flow, balance sheet & valuation measures
     
    #2 Monthly - 'DIB_Financials' dataframe (2021-1985) includes:

    #3 'stock_info' dataframe (2021 ~ 1980s) includes:
        # open, high, low, close, volume, dividend per stock, stock split


import glob           # help: https://pynative.com/python-glob/
import pandas as pd
import os
import time
import datetime

start = time.time()
current = datetime.date.today()
    
#%%


# QUARTERLY Financials Sheets (Years 2021-1985)


#
#  Blank dataframe to hold the accumulated data
#

stack_all = pd.DataFrame()

#
#  Read the files one by one and stack the data onto stack_all
#
path = "raw_data/*.csv"

for file in glob.glob(path, recursive = False):

    raw = pd.read_csv(file,dtype=str)
    
    #  remove spaces and use the name as the index
    
    raw['name'] = raw['name'].str.strip()
    raw = raw.set_index('name')

    #  stack all the remaining columns; the date will become a level 
    #  in the index
    
    stk = raw.stack()
    
    #  set the names of the resulting index levels and the name of 
    #  the remaining data values
    
    stk.index.names = ['name','date']
    stk.name = 'value'
    
    #  remove commas and convert the data to floats
    
    stk = stk.str.replace(',','').astype(float)
    
    #  look for name,date duplicates
    
    dups = stk.index.duplicated()
    print( f'Duplicates in {file}:', dups.sum() )
    
    # convert Series to Dataframe
    stk = stk.to_frame()
        
    # add ticker to each row in data
    ticker = os.path.splitext(os.path.basename(file))[0]
    ticker = ticker.split('_')[0]     
    stk ['ticker'] = ticker
    
    #  append the data to the main stack

    stack_all = stack_all.append(stk)


#
#  Show the result for checking
#

print( stack_all )

#
#  Add ticker to index prior in order to unstack
#

stack_all = stack_all.set_index(['ticker'], append=True)

print( stack_all )

#
#  Turn the names into columns
#

uns = stack_all.unstack('name')['value']

print( uns )

#
#  Get rid of TTM, convert dates, and sort
#

uns = uns.drop('ttm',axis=0)
uns = uns.reset_index()
uns['date'] = pd.to_datetime( uns['date'] )
uns['date'] = uns['date'].dt.date    # keep only the date, remove hr/min/sec
uns = uns.set_index(['date','ticker'])
DIB_Financials = uns.sort_index( ascending= False)

print ( DIB_Financials )

#
# Trim dataframe to only financial measures of interest
#


# import .csv with measures of interest
keep = pd.read_csv('measures_toKeep.csv')

# create a new dataframe with only those measures
keep = keep.Measures.to_list()
measures = DIB_Financials[ keep ]

#
# export to .pkl file w/ zip compression added
#
measures.to_pickle("measures_qtrly.pkl.zip")

print('\n Financials exported to: measures_qrtly.pkl.zip')

'''
# sample
sample = measures.sample(frac = 0.1)
measures.to_csv(str(current) + '_sample_measures_qrtly.csv')
'''

#%%


# MONTHLY Financials Sheets (Years 2021-1985)


#
#  Blank dataframe to hold the accumulated data
#

stack_all = pd.DataFrame()

#
#  Read the files one by one and stack the data onto stack_all
#
path = "raw_monthly/*.csv"

for file in glob.glob(path, recursive = False):

    raw = pd.read_csv(file,dtype=str)
    
    #  remove spaces and use the name as the index
    
    raw['name'] = raw['name'].str.strip()
    raw = raw.set_index('name')

    #  stack all the remaining columns; the date will become a level 
    #  in the index
    
    stk = raw.stack()
    
    #  set the names of the resulting index levels and the name of 
    #  the remaining data values
    
    stk.index.names = ['name','date']
    stk.name = 'value'
    
    #  remove commas and convert the data to floats
    
    stk = stk.str.replace(',','').astype(float)
    
    #  look for name,date duplicates
    
    dups = stk.index.duplicated()
    print( f'Duplicates in {file}:', dups.sum() )
    
    # convert Series to Dataframe
    stk = stk.to_frame()
        
    # add ticker to each row in data
    ticker = os.path.splitext(os.path.basename(file))[0]
    ticker = ticker.split('_')[0]     
    stk ['ticker'] = ticker
    
    #  append the data to the main stack

    stack_all = stack_all.append(stk)


#
#  Show the result for checking
#

print( stack_all )

#
#  Add ticker to index prior in order to unstack
#

stack_all = stack_all.set_index(['ticker'], append=True)

print( stack_all )

#
#  Turn the names into columns
#

uns = stack_all.unstack('name')['value']

print( uns )

#
#  Get rid of TTM, convert dates, and sort
#

uns = uns.drop('ttm',axis=0)
uns = uns.reset_index()
uns['date'] = pd.to_datetime( uns['date'] )
uns['date'] = uns['date'].dt.date    # keep only the date, remove hr/min/sec
uns = uns.set_index(['date','ticker'])
DIB_Financials = uns.sort_index( ascending= False)

print ( DIB_Financials )

#
# Trim dataframe to only financial measures of interest
#


# import .csv with measures of interest
keep = pd.read_csv('measures_toKeep_monthly.csv')

# create a new dataframe with only those measures
keep = keep.Measures.to_list()
measures = DIB_Financials[ keep ]

#
# export to .pkl file w/ zip compression added
#
measures.to_pickle("measures_monthly.pkl.zip")

print('\n Financials exported to: measures_monthly.pkl.zip')

'''
# sample
sample = measures.sample(frac = 0.1)
measures.to_csv(str(current) + '_sample_measures_monthly.csv')
'''


#%%

# 
# Stock info (2021 to ~1980s)
#

# Includes:  open, high, low, close, volume, dividend per stock & stock splits

# Reference: https://pypi.org/project/yfinance/#description

#pip install yfinance
import yfinance as yf

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX','SPX', 'SPSIAD']
    # SPX = S&P 500 index.  
    # SPIAD = S&P 500 Aerospace & Defense Index

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

# export to .pkl
stock_info.to_pickle('stock_info.pkl.zip')

print('\nStock prices exported to : stock_info.pkl.zip')

'''
# sample
sample = stock_info.sample(1000)
sample.to_csv(str(current) + '_sample_stock_info.csv')
'''

  
#%%

#
# Housekeeping
#
print('Financials exported to: measures_monthly.pkl.zip')
print('Financials exported to: measures_qrtly.pkl.zip')


end = time.time()
print('\nPart 1 = Great Success! \nTotal Processing Time:', round(end-start,2), 'seconds\n')

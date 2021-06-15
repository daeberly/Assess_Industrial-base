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
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

start = time.time()

# import pickle file
measures=pd.read_pickle("measures.pkl.zip")

# Create ROE, ROA, ROI Variables
measures["ROA"] = measures["NetIncome"]/measures["TotalAssets"]
measures["ROE"] = measures["NetIncome"]/measures["StockholdersEquity"]
print(measures["ROA"].value_counts())

# Duplicate problem
print(measures.iloc[[311]])
print(measures.iloc[[270]])

# isolate last ten years
start = pd.to_datetime('2011-03-31 00:00:00')
end = pd.to_datetime('2021-03-31 00:00:00')

measures_ten = measures.loc[(('index < @start or index > @end')                            ​
                             
#%%


#
# Calculate ratios
# 



#
# Accounts Payable Turnover 
#
    # number of times debt can be paid off per period

# APT_ratio = 'CostOfRevenue' / (average of 'AccountsPayable' current & previous quarter)


#
# Accounts Payable Turnover Days
# 
   # how many days to payoff debts

# APT_days_ratio = days in period(date current - date previous) / APT Ratio

    # calculate number of days between periods
#sample[‘t_val’] = sample.index
#sample[‘delta’] = (sample[‘t_val’]-sample[‘t_val’].shift()).fillna(0)


#
# Normalize data for plotting
#


#%%

#
# Plots...
#

    # plot measures w/horizontal or vertical reference lines
    # model - forecast
    # heatmap - correlation factors
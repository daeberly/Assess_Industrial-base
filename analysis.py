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
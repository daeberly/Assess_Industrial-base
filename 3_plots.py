
#
# Plots
#

# Run this file after '2_analysis.py' 

# This code creates the following plots for 10,5,3, & 1-year timeframes:
    # Stock prices for all companies
    # ROA and ROE for all companies
    # ROA and ROE for all companies, excluding GE
    # All companies Dividends and Stock Repurchase (separate graphs)
    # Market Cap against P/E Ratio - company specific
    # Market Cap - All companies
    # P/E Ratios, excluding GE
    # Market Cap against Stock Repurchases per company
    # Accounts Payable Turnover in Days All
    # Plot Grid of 6 figures - Accounts Payable Turnover in Days, by company
    # Accounts Payable Turnover in Days, per company
    # Shareholder ROI - barchart
    # Rearch & Development Investments, by company & year
    # Plot Grid of 6 figures - R&D Investments, by company excludes GE

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from dateutil.relativedelta import relativedelta

start_time = datetime.datetime.now()

#%%

#
# Import data
#

  
financials_1yr = pd.read_pickle("clean_data/financials_1yr.pkl")
financials_3yr = pd.read_pickle("clean_data/financials_3yr.pkl")
financials_5yr = pd.read_pickle("clean_data/financials_5yr.pkl")
financials_10yr = pd.read_pickle("clean_data/financials_10yr.pkl")

    # norm_fin is short for normalized financials
norm_fin_1yr = pd.read_pickle("clean_data/norm_fin_1yr.pkl")
norm_fin_3yr = pd.read_pickle("clean_data/norm_fin_3yr.pkl")
norm_fin_5yr = pd.read_pickle("clean_data/norm_fin_5yr.pkl")
norm_fin_10yr = pd.read_pickle("clean_data/norm_fin_10yr.pkl")

stock_info_1yr = pd.read_pickle("clean_data/stocks_1yr.pkl")
stock_info_3yr = pd.read_pickle("clean_data/stocks_3yr.pkl")
stock_info_5yr = pd.read_pickle("clean_data/stocks_5yr.pkl")
stock_info_10yr = pd.read_pickle("clean_data/stocks_10yr.pkl")

monthly_1yr = pd.read_pickle("clean_data/monthly_1yr.pkl")
monthly_3yr = pd.read_pickle("clean_data/monthly_3yr.pkl")
monthly_5yr = pd.read_pickle("clean_data/monthly_5yr.pkl")
monthly_10yr = pd.read_pickle("clean_data/monthly_10yr.pkl")

    # Accounts Payable Turnover Ratios
apt = pd.read_pickle("clean_data/apt.pkl")
    # Research & Development Annual Totals
rd_data = pd.read_pickle("clean_data/R&D_data.pkl")
    # Shareholder ROI calculations
roi = pd.read_pickle("clean_data/ROI_table.pkl")

#%%

#
# Automatically query timeframes from data
#

##### TBD...still needs work

#
# Set parameters for plots
#

# Timeframes

# End Date
today = datetime.datetime.today()
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
# Create Timeframes for Accounts Payable Turnover plots
#

print(apt.dtypes)
apt_10yr = apt.query("date > '2011-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_5yr = apt.query("date > '2016-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_3yr = apt.query("date > '2018-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_1yr = apt.query("date > '2020-01-29 00:00:00' and date < '2021-06-11 00:00:00'")

#%%
# Company stock tickers used in plots below:
    
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

# This is used in df.query(" ticker != @exclude ") 
    # Only one company can be assigned to per variable
exclude = 'GE'

exclude2 = 'BA'     # excluded in one of R&D heatmaps

# Set colors for consistency across all plots
colors = { 'LMT' : 'lightgreen',
          'GE' : 'lightcoral',
          'RTX' : 'darkseagreen',
          'GD' : 'peru',
          'HII' : 'royalblue',
          'BA' : 'lightsteelblue',
          'LHX' : 'plum'
          }

#%%

##########################################
# Stock prices for all companies & S&P 500
##########################################

timeframes = {'Last 12 months':stock_info_1yr, '3 years':stock_info_3yr, 
              '5 years':stock_info_5yr, '10 years':stock_info_10yr}

for name,fin in timeframes.items():
    
    sns.set_theme(style="white", context='paper')

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)
    
    fig = sns.lineplot(data=fin, x='Date', y='norm_close', 
                       hue='ticker', palette= colors)
    plt.xlabel(' ')
    plt.xticks(rotation=0)
    plt.ylabel('Normalized Stock Price',fontsize=12)
    ax1.legend( ncol=8, loc='upper center', fontsize=8)
    plt.title(f'Stock Price, {name}', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'plots/stocks/{name}_stock_prices.png', dpi=300)
 


#%%

################################
# ROA and ROE for all companies
################################

timeframes = {'1yr':norm_fin_1yr, '3yr':norm_fin_3yr, 
              '5yr':norm_fin_5yr, '10yr':norm_fin_10yr}

for name,fin in timeframes.items():
    
    transpose = fin.transpose()
    sns.set_theme(style="white", context='paper')

# ROE 
    ci95 = pd.melt( frame= transpose, var_name= 'date', value_name= 'norm_ROE')

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)
    
    fig = sns.lineplot(data=fin, x='date', y='norm_ROE', 
                       hue='ticker', palette= colors)

#   Average & 95% confidence interval
#    fig = sns.lineplot(ax= ax1, data= ci95, x= 'date', y= 'norm_ROE', 
#                       alpha=.3, linestyle= '--', color= 'k')
    plt.xlabel(' ')
    plt.xticks(rotation=0)
#    plt.axhline(14, linewidth=1, color='r', linestyle= '-.', alpha=0.5)
    plt.ylabel('Normalized Ratio',fontsize=12)
    ax1.legend( ncol=7, loc='upper center', fontsize=9)
    plt.title(f'Return on Equity with General Electric, {name}', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'plots/ROE/{name}_ROE_GE.png', dpi=300)
 
# ROA
    ci95 = pd.melt( frame= transpose, var_name= 'date', value_name= 'norm_ROA')

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    
    fig = sns.lineplot(data=fin, x='date', y='norm_ROA', 
                       hue='ticker', palette= colors)

#   Average & 95% confidence interval
#    fig = sns.lineplot(ax= ax1, data= ci95, x= 'date', y= 'norm_ROA', 
#                       alpha=.3, linestyle= '--', color= 'k')
    plt.xlabel(' ')
    plt.xticks(rotation=0)
#    plt.axhline(5, linewidth=1, color='r', linestyle= '-.', alpha=0.5)    
    plt.ylabel('Normalized Ratio',fontsize=12)
    ax1.legend( ncol=7, loc='upper center', fontsize=9)
    plt.title(f'Return on Assets with General Electric, {name}', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'plots/ROA/{name}_ROA_GE.png', dpi=300)
 
 
#%%

##############################################
# ROA and ROE for all companies, excluding GE
##############################################

timeframes = {'1yr':norm_fin_1yr, '3yr':norm_fin_3yr, 
              '5yr':norm_fin_5yr, '10yr':norm_fin_10yr}

for name,fin in timeframes.items():
    
    fin = fin.query("ticker != @exclude ")
    
    transpose = fin.transpose()
    fin = fin.reset_index()
    sns.set_theme(style="white", context='paper')

# ROE 
    ci95 = pd.melt( frame= transpose, var_name= 'date', value_name= 'norm_ROE')

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)
    
    fig = sns.lineplot(data=fin, x='date', y='norm_ROE',
                       hue='ticker', palette= colors)

#   Average & 95% confidence interval
#    fig = sns.lineplot(ax= ax1, data= ci95, x= 'date', y= 'norm_ROE', 
#                       alpha=.3, linestyle= '--', color= 'k')
    plt.xlabel(' ')
    plt.xticks(rotation=0)
    plt.axhline(14, linewidth=1, color='r', linestyle= '-.', alpha=0.5)
    plt.ylabel('Normalized Ratio',fontsize=12)
    ax1.legend( ncol=6, loc='upper center', fontsize=10)
    plt.title(f'Return on Equity, {name}', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'plots/ROE/{name}_ROE.png', dpi=300)
 
# ROA
    ci95 = pd.melt( frame= transpose, var_name= 'date', value_name= 'norm_ROA')

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    
    fig = sns.lineplot(data=fin, x='date', y='norm_ROA', 
                       hue='ticker', palette= colors)

#   Average & 95% confidence interval
#    fig = sns.lineplot(ax= ax1, data= ci95, x= 'date', y= 'norm_ROA', 
#                       alpha=.3, linestyle= '--', color= 'k')
    plt.xlabel(' ')
    plt.xticks(rotation=0)
    plt.axhline(5, linewidth=1, color='r', linestyle= '-.', alpha=0.5)    
    plt.ylabel('Normalized Ratio',fontsize=12)
    ax1.legend( ncol=6, loc='upper center', fontsize=10)
    plt.title(f'Return on Assets, {name}', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'plots/ROA/{name}_ROA.png', dpi=300)
 

#%%

#################################################################
# All companies Dividends and Stock Repurchase (separate graphs)
#################################################################

timeframes = {'1yr':financials_1yr, '3yr':financials_3yr, 
              '5yr':financials_5yr, '10yr':financials_10yr}

for name,temp in timeframes.items():
    
    # covert values to $Millions
    temp = temp*-1/1e6

# Cash Dividends Paid    
    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)
 
    fig = sns.lineplot(data=temp, x='date', y='CashDividendsPaid',
                       hue='ticker', palette= colors)
    ax1.legend( ncol=7, loc='upper center', fontsize=8)
    plt.xlabel(' ')
    plt.ylabel('Cash Flow (millions)')
    plt.title('Cash Dividends Paid')
    plt.savefig('plots/CashFlow/{name}_CashFlowDiv_All.png', dpi=300)

# Stock Repurchases
    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)

    fig = sns.lineplot(data=temp, x='date', y='RepurchaseOfCapitalStock'
                       , hue='ticker', palette= colors)
    ax1.legend( ncol=7, loc='upper center', fontsize=8)
    plt.xlabel(' ')
    plt.ylabel('Cash Flow (millions)')
    plt.title('Repurchase of Capital Stock')
    plt.savefig('plots/CashFlow/{name}_CashFlowRepurchase_All.png', dpi=300)


#%%
#################################################
# Market Cap against P/E Ratio - company specific
#################################################

timeframes = { '1yr': monthly_1yr, '3yr': monthly_3yr,
              '5yr': monthly_5yr, '10yr': monthly_10yr}

for name, timeframe in timeframes.items():

    for ticker in companies:
      
        temp = timeframe.query("ticker == @ticker")
        temp = temp.dropna()
        temp = temp.reset_index()
        temp['MarketCap'] = temp['MarketCap']/1e9
        temp['date'] = pd.to_datetime(temp['date']).dt.date 
        
        fig, ax1 = plt.subplots() 
      
        color = 'tab:blue'
        plt.title(ticker)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Market Cap, $B', color = color) 
        temp.plot(x='date', y='MarketCap', color=color, ax=ax1)
        ax1.tick_params(axis ='y', labelcolor = color)
        ax1.get_legend().remove()
        ax1.set_xlabel('')
        
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('P/E Ratio', color = color) 
        temp.plot(y='PeRatio', x='date', color=color, ax=ax2)
        ax2.tick_params(axis ='y', labelcolor = color) 
        ax2.axhline(14,linewidth=2, color='r', linestyle='--', alpha=.5) #S&P 500 historic P/E
        ax2.get_legend().remove()
        ax2.set_xlabel('')
    
        fig.tight_layout()
        fig.savefig(f'plots/Purchase_MarketCap/{name}_MarketCap&PE_{ticker}.png', dpi=300)
        

#%%

############################
# Market Cap - All companies
############################

timeframes = {'1yr':monthly_1yr, '3yr':monthly_3yr, 
              '5yr':monthly_5yr, '10yr':monthly_10yr}

for name,time in timeframes.items():    
    
    time = time[['PeRatio','MarketCap']]
    time = time.copy()
    time['MarketCap']=time['MarketCap']/1e9
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='MarketCap',
                       hue='ticker', palette= colors)
    plt.xlabel('')
    plt.xticks(rotation=45)
    ax1.axhline(10,linewidth=2, color='r', linestyle='--', alpha=.5)
    
    plt.ylabel('Market Cap (billions)')
    plt.title(' ')
    ax1.legend( ncol=7, loc='upper center', fontsize=8)
    plt.tight_layout()
    plt.savefig(f'plots/MarketCap_All_{name}.png', dpi=300)

    
#%%

##########################
# P/E Ratios, excluding GE
##########################

timeframes = {'1yr':monthly_1yr, '3yr':monthly_3yr, 
              '5yr':monthly_5yr, '10yr':monthly_10yr}

for name,time in timeframes.items():  
    
    time = time.query("ticker != @exclude ")
    time = time.dropna()
 
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='PeRatio', 
                       hue='ticker', palette= colors)
    ax1.axhline(14, linewidth=2, color='r', linestyle= '--', alpha=0.5)
    plt.xlabel('')
    plt.xticks(rotation=45)
    plt.ylabel('Ratio')
    plt.title('P/E Ratio')
    ax1.legend( ncol=7, loc='upper center', fontsize=8)
    plt.tight_layout()
    plt.savefig(f'plots/PERatio_DropGE_{name}.png', dpi=300)
    
#%%

##################################################
# Market Cap against Stock Repurchases per company
##################################################

# 10, 5, 3, & 1 year intervals

#####
#
# Merge Timeframe data sets
#

#
# Merge - 1 year Market Cap and Stock Repurchase
#
monthly_1yr = monthly_1yr.reset_index()
trim = monthly_1yr[['date','ticker','MarketCap']]

financials_1yr = financials_1yr.reset_index()
fin_trim = financials_1yr[['date','ticker','RepurchaseOfCapitalStock']]

merge = trim.merge(fin_trim, on=["date","ticker"], how="outer", validate="1:1", indicator=True)
print(merge['_merge'].value_counts())

merge = merge.query("_merge == 'both'")

merge_1yr = merge.drop('_merge', axis='columns')
merge_1yr.set_index(['date','ticker'], inplace=True)
merge_1yr['RepurchaseOfCapitalStock'] = merge_1yr['RepurchaseOfCapitalStock']*-1/1e6
merge_1yr['MarketCap'] = merge_1yr['MarketCap']/1e9

#
# Merge - 3 year Market Cap and Stock Repurchase
#

monthly_3yr = monthly_3yr.reset_index()
trim = monthly_3yr[['date','ticker','MarketCap']]

financials_3yr = financials_3yr.reset_index()
fin_trim = financials_3yr[['date','ticker','RepurchaseOfCapitalStock']]

merge = trim.merge(fin_trim, on=["date","ticker"], how="outer", validate="1:1", indicator=True)
print(merge['_merge'].value_counts())

merge = merge.query("_merge == 'both'")

merge_3yr = merge.drop('_merge', axis='columns')
merge_3yr.set_index(['date','ticker'], inplace=True)
merge_3yr['RepurchaseOfCapitalStock'] = merge_3yr['RepurchaseOfCapitalStock']*-1/1e6
merge_3yr['MarketCap'] = merge_3yr['MarketCap']/1e9

#
# Merge - 5 year Market Cap and Stock Repurchase
#

monthly_5yr = monthly_5yr.reset_index()
trim = monthly_5yr[['date','ticker','MarketCap']]

financials_5yr = financials_5yr.reset_index()
fin_trim = financials_5yr[['date','ticker','RepurchaseOfCapitalStock']]

merge = trim.merge(fin_trim, on=["date","ticker"], how="outer", validate="1:1", indicator=True)
print(merge['_merge'].value_counts())

merge = merge.query("_merge == 'both'")

merge_5yr = merge.drop('_merge', axis='columns')
merge_5yr.set_index(['date','ticker'], inplace=True)
merge_5yr['RepurchaseOfCapitalStock'] = merge_5yr['RepurchaseOfCapitalStock']*-1/1e6
merge_5yr['MarketCap'] = merge_5yr['MarketCap']/1e9

#
# Merge - 10 year Market Cap and Stock Repurchase
#

monthly_10yr = monthly_10yr.reset_index()
trim = monthly_10yr[['date','ticker','MarketCap']]

financials_10yr = financials_10yr.reset_index()
fin_trim = financials_10yr[['date','ticker','RepurchaseOfCapitalStock']]

merge = trim.merge(fin_trim, on=["date","ticker"], how="outer", validate="1:1", indicator=True)
print(merge['_merge'].value_counts())

merge = merge.query("_merge == 'both'")

merge_10yr = merge.drop('_merge', axis='columns')
merge_10yr.set_index(['date','ticker'], inplace=True)
merge_10yr['RepurchaseOfCapitalStock'] = merge_10yr['RepurchaseOfCapitalStock']*-1/1e6
merge_10yr['MarketCap'] = merge_10yr['MarketCap']/1e9


#####
#
# Plots
#


timeframes = {'1yr':merge_1yr, '3yr':merge_3yr, 
              '5yr':merge_5yr, '10yr':merge_10yr}

for name, time in timeframes.items():

    for ticker in companies:
      
        temp = time.query("ticker == @ticker").copy()
        temp = temp.reset_index()
        temp['date'] = pd.to_datetime(temp['date']).dt.date 
        
        fig, ax1 = plt.subplots() 

 # Markey Cap     
        color = 'tab:blue'
        plt.title(ticker)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Market Cap, $B', color = color) 
        temp.plot(x='date', y='MarketCap', color=color, ax=ax1)
        ax1.tick_params(axis ='y', labelcolor = color)
        ax1.grid(b=None, alpha=0.1)
        ax1.get_legend().remove()
        ax1.set_xlabel('')

 # Stock Repurchase      
        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Stock Repurchase, $M', color = color) 
        temp.plot(y='RepurchaseOfCapitalStock', x='date', color=color, ax=ax2)
        ax2.tick_params(axis ='y', labelcolor = color) 
        ax2.get_legend().remove()
        ax2.set_xlabel('')
    
        fig.tight_layout()
        fig.savefig(f'plots/Purchase_MarketCap/{name}_Purchase_MarketCap_{ticker}.png', dpi=300)
    
#%%

#################################
# Accounts Payable Turnover (APT)
#################################


#
# Create Timeframes for APT plots
#


apt_10yr = apt.query("date >'2011-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_5yr = apt.query("date > '2016-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_3yr = apt.query("date > '2018-01-29 00:00:00' and date < '2021-06-11 00:00:00'")
apt_1yr = apt.query("date > '2020-01-29 00:00:00' and date < '2021-06-11 00:00:00'")

#%%

#
# Accounts Payable Turnover in Days All
#

timeframes = {'1yr':apt_1yr, '3yr':apt_3yr, 
          '5yr':apt_5yr, '10yr':apt_10yr}

for name,time in timeframes.items():
    temp = time.copy()
    temp = temp.reset_index()
    temp['date'] = pd.to_datetime(temp['date']).dt.date 
        
    fig, ax1 = plt.subplots(dpi=300)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)

    fig = sns.lineplot(data=temp, x='date', y='APT_days', 
                       hue='ticker', palette= colors)
    plt.xticks(rotation=45)
    plt.ylabel('Ratio (Days)')
    plt.xlabel(' ')
    plt.title('Accounts Payable Turnover in Days')
    ax1.legend( ncol=7, loc='upper center', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'plots/APT/{name}_APTdays_all.png', dpi=300)

#%%

#
# Plot Grid of 6 figures - Accounts Payable Turnover in Days, by company
#

timeframes = {'1yr':apt_1yr, '3yr':apt_3yr, 
              '5yr':apt_5yr, '10yr':apt_10yr}

for name, time in timeframes.items():

    fig, axs = plt.subplots(2,3, figsize=(16,10),
                            sharex=True, sharey=True)
    ax1 = axs[0][0]
    ax2 = axs[0][1]
    ax3 = axs[0][2]
    ax4 = axs[1][0]
    ax5 = axs[1][1]
    ax6 = axs[1][2]
    
    grid_plot = {'LMT': ax1, 'HII': ax2,'GD' : ax3,
                 'LHX':ax4,'RTX':ax5, 'BA':ax6}

    sns.set_theme(style="whitegrid", context='paper')
    
    for ticker, axis in grid_plot.items():
      
        temp = time.query(" ticker == @ticker ")
        temp = temp.reset_index()
        temp['date'] = pd.to_datetime(temp['date']).dt.date 
    
        sns.lineplot(data=temp, x='date', y='APT_days', ax= axis)
    
        axis.grid(b = True, color ='grey',linestyle ='-.', 
                  linewidth = 0.5, alpha = 0.2)
        axis.set_title( f' {ticker} ', fontsize=12, weight='bold')
        axis.set_xlabel(' ')
        axis.set_ylabel('')
        
    plt.xlabel('')
    fig.suptitle(f'Accounts Payable Turnover in Days, {name}', 
                 fontsize=14, weight='bold')
    fig.supylabel('Days', fontsize=16, weight='bold')
    fig.tight_layout(pad= 1.5)
    plt.savefig(f'plots/R&D/{name}R&D_grid.png', dpi=300)


#%%

#
# Accounts Payable Turnover in Days, per company
#

timeframes = {'1yr':apt_1yr, '3yr':apt_3yr, 
          '5yr':apt_5yr, '10yr':apt_10yr}

for name,time in timeframes.items():
    
    for ticker in companies:

        temp = time.query("ticker == @ticker").copy()
        temp = temp.reset_index()
        temp['date'] = pd.to_datetime(temp['date']).dt.date 
    
        fig, ax1 = plt.subplots()
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(b = True, color ='black',linestyle ='-.', linewidth = 0.5, alpha = 0.1)

        fig = sns.lineplot(data=temp, x='date', y='APT_days', hue="ticker")
        plt.xlabel('')
        plt.ylabel('Days')
        plt.xticks(rotation=45)
        plt.title(f'Accounts Payable Turnover in Days, {ticker}')
        ax1.get_legend().remove()
        plt.tight_layout()
        plt.savefig(f'plots/APT/{name}_APT_{ticker}.png', dpi=300)

   
#%%     

########################
# Shareholder ROI plots
########################


# Sort variables to plot
roi_div_10yr = roi['roi_div_10yr'].sort_values()
roi_10yr = roi['roi_10yr'].sort_values()
roi_diff_10yr = roi['roi_%diff_10yr'].sort_values()
roi_div_5yr = roi['roi_div_5yr'].sort_values()
roi_5yr = roi['roi_5yr'].sort_values()
roi_diff_5yr = roi['roi_%diff_5yr'].sort_values()
roi_div_3yr = roi['roi_div_3yr'].sort_values()
roi_3yr = roi['roi_3yr'].sort_values()
roi_diff_3yr = roi['roi_%diff_3yr'].sort_values()
roi_div_1yr = roi['roi_div_1yr'].sort_values()
roi_1yr = roi['roi_1yr'].sort_values()
roi_diff_1yr = roi['roi_%diff_1yr'].sort_values()

#%%

#
# Define dictionary to iterate through
#

rois = {'10 years, dividends': roi_div_10yr,
        '10 years, no dividends':roi_10yr, 
        '10 years, added impact of a dividend':roi_diff_10yr, 
        '5 years, dividends':roi_div_5yr, 
        '5 years, no dividends':roi_5yr, 
        '5 years, added impact of a dividend':roi_diff_5yr,
        '3 years, dividends':roi_div_3yr, 
        '3 years, no dividends':roi_3yr,
        '3 years, added impact of a dividend':roi_diff_3yr,
        '1 year, dividends':roi_div_1yr, 
        '1 year, no dividends':roi_1yr,
        '1 years, added impact of a dividend':roi_diff_1yr, 
        }
####
#
# Bar Charts - ROI
#
# Iterate through dictionary

for name, roi in rois.items():

    fig, ax1 = plt.subplots(dpi=300)
    ax1 = roi.plot.barh( alpha= .5 )

        # Label each bars
    for index, value in enumerate( roi ):
        plt.text(value, index, str(round(value,1))+'%', 
                 verticalalignment= 'center',
                 horizontalalignment= 'center',
                 fontweight= 'medium')
        # Remove axes splines
    for s in ['top', 'right']: # other options - 'bottom', 'left'
        ax1.spines[s].set_visible(False)

    ax1.xaxis.set_ticks_position('none')
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_tick_params(pad = 5)
    ax1.yaxis.set_tick_params(pad = 10)
    ax1.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5, alpha = 0.2)

    ax1.set_xlabel('ROI per one share of stock')
    ax1.set_ylabel('Stock Ticker')
    ax1.set_title(f'ROI: {name}')

    fig.tight_layout()
    fig.savefig(f"plots/ROI_{name}.png", format='png',dpi=300)
    
    
#%%

#####################################################
# Rearch & Development Investments, by company & year
#####################################################

# All companies R&D Investments

rd_data1 = rd_data.copy()
rd_data1['Date'] = pd.to_datetime(rd_data1['Date']).dt.year
rd_data1['R&D_total'] =  rd_data1['R&D_total']/ 1e6

# Exclude GE('exclude') and BA ('exclude') to remove outliers

rd_data_trim = rd_data1.query("ticker != @exclude and ticker != @exclude2 ")

# Create pivot table for Heatmap plot
rd_data_map = rd_data_trim.pivot("ticker", "Date", "R&D_total")

####
#
# Plot - R&D Heatmap, excluding GE & BA
#

sns.set_theme(context='paper')
fig, ax = plt.subplots( figsize=(7,4))
ax = sns.heatmap(rd_data_map, linewidths = .5, cmap="Greens", annot=True, fmt='g')
ax.set_xlabel(' ')
ax.set_ylabel(' ')
plt.title('Company Research & Development Investments, in $ millions')
plt.tight_layout()
plt.savefig('plots/R&D/All_RD_heatmap.png', dpi=300)


#%%
#
# Plot Grid of 6 figures - R&D Investments, by company excludes GE
#

rd_data2 = rd_data.copy().sort_values(by='Date', ascending= False)

fig, axs = plt.subplots(2,3, figsize=(14,10),
                        sharex=False, sharey=False)

sns.set_theme(style="whitegrid", context='paper')

ax1 = axs[0][0]
ax2 = axs[0][1]
ax3 = axs[0][2]
ax4 = axs[1][0]
ax5 = axs[1][1]
ax6 = axs[1][2]

grid_plot = {'LMT': ax1, 'RTX': ax2,'BA' : ax3,'GD':ax4,
              'HII':ax5, 'LHX':ax6}

for ticker, axis in grid_plot.items():
  
    temp = rd_data2.query("ticker == @ticker")
    temp = temp.reset_index()
    temp['R&D_total'] = temp['R&D_total']/1e6
    temp['Date'] = pd.to_datetime(temp['Date']).dt.year 

    sns.barplot(data=temp, x='Date', y='R&D_total', 
                ax= axis, color='steelblue', alpha=.8)
    axis.set_title( f' {ticker} ', fontsize=14, weight='bold')
    axis.set_xlabel(' ')
    axis.set_ylabel('')
    
plt.xlabel('')
fig.suptitle('Research and Development Investments', fontsize=16, weight='bold')
fig.supylabel('Millions ($)', fontsize=16, weight='bold')
fig.tight_layout()
plt.savefig('plots/R&D/R&D_grid.png', dpi=300)

#%%

#
# Housekeeping
#

print( '\nPart 3 = Great Success!')

end_time = datetime.datetime.now()

time_diff = (end_time - start_time)

print('\nTotal Processing Time:', time_diff, 'hr:min:secs\n')









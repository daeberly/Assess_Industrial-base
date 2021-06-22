
#
# Plots
#

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

start = time.time()

#
# Import data
#

financials_1yr = pd.read_pickle("clean_data/financials_1yr.pkl")
financials_3yr = pd.read_pickle("clean_data/financials_3yr.pkl")
financials_5yr = pd.read_pickle("clean_data/financials_5yr.pkl")
financials_10yr = pd.read_pickle("clean_data/financials_10yr.pkl")

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

apt = pd.read_pickle("clean_data/apt.pkl")
RD_data = pd.read_pickle("clean_data/R&D_data.pkl")
roi = pd.read_pickle("clean_data/ROI_table.pkl")


#%%

#
# Consistent variables
#

companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

colors = { 'LMT' : 'lightgreen',
          'GE' : 'lightcoral',
          'RTX' : 'darkseagreen',
          'GD' : 'peru',
          'HII' : 'royalblue',
          'BA' : 'lightsteelblue',
          'LHX' : 'plum'
          }

colors = { 'LMT' : 'blue',
          'GE' : 'orange',
          'RTX' : 'green',
          'GD' : 'purple',
          'HII' : 'red',
          'BA' : 'gray',
          'LHX' : 'olive'
          }
#%%

#
# ROI plots
#

# Sort variables to plot

roi.columns
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


# Define dictionary to iterate through

rois = {'10 years, dividends': roi_div_10yr,
        '10 years, no dividends':roi_10yr, 
        '10 years, dividend difference':roi_diff_10yr, 
        
        '5 years, dividends':roi_div_5yr, 
        '5 years, no dividends':roi_5yr, 
        '5 years, dividend difference':roi_diff_5yr,
         
        '3 years, dividends':roi_div_3yr, 
        '3 years, no dividends':roi_3yr,
        '3 years, dividend difference':roi_diff_3yr,
        
        '1 year, dividends':roi_div_1yr, 
        '1 year, no dividends':roi_1yr,
        '1 years, dividend difference':roi_diff_1yr, 
        }

#%%
####
#
# Bar Charts - ROI
#


# Iterate through dictionary
for name, roi in rois.items():

    # plot data
    fig, ax1 = plt.subplots(dpi=300)
    ax1 = roi.plot.barh( alpha= .5 )
    
    # Set plot appearance - labels, colors, background
        # Label each bars
    for index, value in enumerate( roi ):
        plt.text(value, index, str(round(value,1))+'%', 
                 verticalalignment= 'center',
                 horizontalalignment= 'center',
                 fontweight= 'medium')
    
        # Remove axes splines
    for s in ['top', 'right']: # other options - 'bottom', 'left'
        ax1.spines[s].set_visible(False)
     
        # Remove x, y Ticks
    ax1.xaxis.set_ticks_position('none')
    ax1.yaxis.set_ticks_position('none')
     
        # Add padding between axes and labels
    ax1.xaxis.set_tick_params(pad = 5)
    ax1.yaxis.set_tick_params(pad = 10)
     
       # Background
    ax1.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
        # Plot axis labels & title
    ax1.set_xlabel('ROI per one share of stock')
    ax1.set_ylabel('Stock Ticker')
    ax1.set_title(f'Shareholder ROI: {name}')
    
    # Export plot
    fig.tight_layout()
    fig.savefig(f"plots/ROI_{name}.png", format='png',dpi=300)

#%%

timeframes = [norm_fin_1yr, norm_fin_3yr, norm_fin_5yr, norm_fin_10yr]

for time in timeframes:

            # Remove axes splines
   for s in ['top', 'right']: # other options - 'bottom', 'left'
       ax1.spines[s].set_visible(False)
     
        # Remove x, y Ticks
   ax1.xaxis.set_ticks_position('none')
   ax1.yaxis.set_ticks_position('none')
     
        # Add padding between axes and labels
   ax1.xaxis.set_tick_params(pad = 5)
   ax1.yaxis.set_tick_params(pad = 10)
     
       # Background
   ax1.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)
    
   fig, ax1 = plt.subplots(dpi=300)
   fig = sns.lineplot(data=time, x='date', y='norm_ROE', hue='ticker', palette = colors)
   plt.xlabel('Year')
   plt.ylabel('ratio')
   ax1.set_title('Return on Equity')
   plt.savefig('plots/ROE_1yr.png',dpi=300)
    
   fig, ax1 = plt.subplots(dpi=300)
   fig = sns.lineplot(data=time, x='date', y='norm_ROA', hue='ticker', palette = colors)
   plt.xlabel('Year')
   plt.ylabel('Return on Assets')
   plt.savefig('plots/ROA_1yr.png',dpi=300)
#%%

timeframes = [norm_fin_1yr, norm_fin_3yr, norm_fin_5yr, norm_fin_10yr]

for time in timeframes:
    time = time.query("ticker != 'GE'")
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='norm_ROE', hue='ticker')
    plt.xlabel('Year')
    plt.ylabel('Return on Equity')
    plt.savefig('plots/ROE_1yr.png',dpi=300)
    
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='norm_ROA', hue='ticker')
    plt.xlabel('Year')
    plt.ylabel('Return on Assets')
    plt.savefig('plots/ROA_1yr.png',dpi=300)

#%%
#Company specific Dividends and Repurchase

frames = {'1yr':financials_1yr, '3yr':financials_3yr, '5yr':financials_5yr, '10yr':financials_10yr}

for name,fin in frames.items():
    
    for ticker in companies:
  
        tick = ticker
        temp = fin.query("ticker == @tick")
    
    # format
        temp = temp[['CashDividendsPaid','RepurchaseOfCapitalStock']]*-1/1e6
        temp = temp.reset_index()
        temp['date'] = temp['date'].values.astype('datetime64[D]')
        temp.set_index(['date'],inplace=True)

        plt.figure()
        temp.plot()
        plt.xticks(rotation=45)
        plt.xlabel('Quarters')
        plt.ylabel('Cash Flow (millions)')
        plt.title(f'{name}{ticker}')
        plt.savefig(f'plots/CashFlow_{name}{ticker}.png')

#%%

#All companies

timeframes = [financials_1yr, financials_3yr, financials_5yr, financials_10yr]

for time in timeframes:
    millions = time*-1/1e6
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=millions, x='date', y='CashDividendsPaid', hue='ticker')
    plt.xlabel('Year')
    plt.ylabel('Cash Flow (millions)')
    plt.title('Cash Dividends Paid')
    plt.savefig('plots/CashFlowDiv_All.png', dpi=300)
    
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=millions, x='date', y='RepurchaseOfCapitalStock', hue='ticker')
    plt.xlabel('Year')
    plt.ylabel('Cash Flow (millions)')
    plt.title('Repurchase of Capital Stock')
    plt.savefig('plots/CashFlowRepurchase_All.png', dpi=300)

#%%
# Market Cap and P/E Ratio

# 1 year company specific

for ticker in companies:
  
    tick = ticker
    temp = monthly_1yr.query("ticker == @tick")
    temp = temp.dropna()
    print(temp)
    
    temp = temp[['PeRatio','MarketCap']]
    temp['MarketCap'] = temp['MarketCap']/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True) 

    plt.figure()
    temp.plot()
    plt.xlabel('Quarters')
    plt.ylabel('What am I (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/MarketCap&PE_1yr_{ticker}.png')
    
#%%
# 3 year Market Cap/PE Ratio company specific

for ticker in companies:
  
    tick = ticker
    temp = monthly_3yr.query("ticker == @tick")
    temp = temp.dropna()
    print(temp)
    
    temp = temp[['PeRatio','MarketCap']]
    temp['MarketCap'] = temp['MarketCap']/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True) 

    plt.figure()
    temp.plot()
    plt.xlabel('Years')
    plt.ylabel('What am I (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/MarketCap&PE_3yr_{ticker}.png')
#%%
# 5 year Market Cap/PE Ratio company specific

for ticker in companies:
  
    tick = ticker
    temp = monthly_5yr.query("ticker == @tick")
    temp = temp.dropna()
    print(temp)
    
    temp = temp[['PeRatio','MarketCap']]
    temp['MarketCap'] = temp['MarketCap']/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True) 

    plt.figure()
    temp.plot()
    plt.xlabel('Years')
    plt.ylabel('What am I (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/MarketCap&PE_5yr_{ticker}.png')

#%%
# 10 year Market Cap/PE Ratio company specific

for ticker in companies:
  
    tick = ticker
    temp = monthly_10yr.query("ticker == @tick")
    temp = temp.dropna()
    print(temp)
    
    temp = temp[['PeRatio','MarketCap']]
    temp['MarketCap'] = temp['MarketCap']/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True) 

    plt.figure()
    temp.plot()
    plt.xlabel('Years')
    plt.ylabel('What am I (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/MarketCap&PE_10yr_{ticker}.png')

#%%

# Market Cap and P/E Ratio
# All companies

timeframes = [monthly_1yr, monthly_3yr, monthly_5yr, monthly_10yr]

for time in timeframes:
    time = time[['PeRatio','MarketCap']]
    time = time.copy()
    time['MarketCap']=time['MarketCap']/1e6
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='MarketCap', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('Market Cap (millions)')
    plt.title('Market Cap')
    plt.savefig('plots/MarketCap_All.png', dpi=300)
    
    time = time.dropna()
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='PeRatio', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('P/E Ratio')
    plt.title('P/E Ratio')
    plt.savefig('plots/PERatio_All.png', dpi=300)

#%%
# P/E Ratios
# Drop GE
timeframes = [monthly_1yr, monthly_3yr, monthly_5yr, monthly_10yr]

for time in timeframes:
    time = time.query("ticker != 'GE'")
    time = time.dropna()
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='PeRatio', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('P/E Ratio')
    plt.title('P/E Ratio')
    plt.savefig('plots/PERatio_DropGE.png', dpi=300)
   
#%%
#Merge Market Cap and Stock Repurchase

#merge monthly and financials
fig, ax1 = plt.subplots()
fig.suptitle('Market Cap and Stock Repurchase')
ax1.set_title('BA')
#ax1.axhline(15)
ax1 = monthly_1yr['MarketCap'].plot(legend=True)
ax1 = financials_1yr['RepurchaseOfCapitalStock'].plot(legend=True)
plt.legend(loc='upper left', prop={'size':6})
fig.tight_layout()
#fig.savefig("4d_timeseries_wind_byLocation.svg", format='svg',dpi=300)

#%%
#Merge Market Cap and Stock Repurchase
monthly_1yr = monthly_1yr.reset_index()
trim = monthly_1yr[['date','ticker','MarketCap']]

financials_1yr = financials_1yr.reset_index()
fin_trim = financials_1yr[['date','ticker','RepurchaseOfCapitalStock']]

merge = trim.merge(fin_trim, on=["date","ticker"], how="outer", validate="1:1", indicator=True)
print(merge['_merge'].value_counts())


#%%

merge = merge.query("_merge == 'both'")
merge = merge.drop('_merge', axis='columns')
merge.set_index(['date','ticker'], inplace=True)
merge['RepurchaseOfCapitalStock'] = merge['RepurchaseOfCapitalStock']*-1/1e6
merge['MarketCap'] = merge['MarketCap']/1e6

#%%
fig, ax1 = plt.subplots(dpi=300)
fig.suptitle('Market Cap and Stock Repurchase')
ax1.set_title('All Companies')
#ax1.axhline(15)
ax1 = merge["MarketCap"].plot()
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.ylabel('Millions') 
plt.title('P/E Ratio')
plt.savefig('plots/PERatio_DropGE.png', dpi=300)

plt.title( tick )
#%%
'''
# Market Cap and Stock Repurchase
# All companies

monthly_timeframes = [monthly_1yr, monthly_3yr, monthly_5yr, monthly_10yr]

for df in monthly_timeframes:
    
quarterly_timeframes = [financials_1yr, financials_3yr, financials_5yr, financials_10yr]



for time in timeframes:
    time = time[['PeRatio','MarketCap']]
    time = time.copy()
    time['MarketCap']=time['MarketCap']/1e6
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='MarketCap', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('Market Cap (millions)')
    plt.title('Market Cap')
    plt.savefig('plots/MarketCap_All.png', dpi=300)
    
    time = time.dropna()
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='PeRatio', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('P/E Ratio')
    plt.title('P/E Ratio')
    plt.savefig('plots/PERatio_All.png', dpi=300)

'''
#%%

#
# Housekeeping
#


end = time.time()
print('\nPart 3.Plots = Great Success! \nTotal Processing Time:', round(end-start,2), 'seconds\n')


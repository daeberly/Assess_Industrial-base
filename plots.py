import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

financials_1yr = pd.read_pickle("financials_1yr.pkl")
financials_3yr = pd.read_pickle("financials_3yr.pkl")
financials_5yr = pd.read_pickle("financials_5yr.pkl")
financials_10yr = pd.read_pickle("financials_10yr.pkl")

norm_fin_1yr = pd.read_pickle("norm_fin_1yr.pkl")
norm_fin_3yr = pd.read_pickle("norm_fin_3yr.pkl")
norm_fin_5yr = pd.read_pickle("norm_fin_5yr.pkl")
norm_fin_10yr = pd.read_pickle("norm_fin_10yr.pkl")

stock_info_1yr = pd.read_pickle("stocks_1yr.pkl")
stock_info_3yr = pd.read_pickle("stocks_3yr.pkl")
stock_info_5yr = pd.read_pickle("stocks_5yr.pkl")
stock_info_10yr = pd.read_pickle("stocks_10yr.pkl")

monthly_1yr = pd.read_pickle("monthly_1yr.pkl")
monthly_3yr = pd.read_pickle("monthly_3yr.pkl")
monthly_5yr = pd.read_pickle("monthly_5yr.pkl")
monthly_10yr = pd.read_pickle("monthly_10yr.pkl")

apt = pd.read_pickle("apt.pkl")
RD_data = pd.read_pickle("RD_data.pkl")

#%%

timeframes = [norm_fin_1yr, norm_fin_3yr, norm_fin_5yr, norm_fin_10yr]

for time in timeframes:
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
#1 year
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

for ticker in companies:
  
    tick = ticker
    temp = financials_1yr.query("ticker == @tick")
    
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
    plt.title(f'{ticker}')
    plt.savefig(f'plots/CashFlow_{ticker}.png')
    
#%%
#3 years
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

for ticker in companies:
  
    tick = ticker
    temp = financials_3yr.query("ticker == @tick")
    
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
    plt.title(f'{ticker}')
    plt.savefig(f'plots/CashFlow_{ticker}.png')
    
#%%
#5 years
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

for ticker in companies:
  
    tick = ticker
    temp = financials_5yr.query("ticker == @tick")
    
    # format
    temp = temp[['CashDividendsPaid','RepurchaseOfCapitalStock']]*-1/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True)

    plt.figure()
    temp.plot()
    plt.xticks(rotation=45)
    plt.xlabel('Years')
    plt.ylabel('Cash Flow (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/CashFlow_{ticker}.png')

#%%
#10 years
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

for ticker in companies:
  
    tick = ticker
    temp = financials_10yr.query("ticker == @tick")
    
    # format
    temp = temp[['CashDividendsPaid','RepurchaseOfCapitalStock']]*-1/1e6
    temp = temp.reset_index()
    temp['date'] = temp['date'].values.astype('datetime64[D]')
    temp.set_index(['date'],inplace=True) 

    plt.figure()
    temp.plot()
    plt.xticks(rotation=45)
    plt.xlabel('Years')
    plt.ylabel('Cash Flow (millions)')
    plt.title(f'{ticker}')
    plt.savefig(f'plots/CashFlow_{ticker}.png')

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
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    #plt.savefig(f'plots/CashFlow_{ticker}.png')
    
#%%
# 3 year Market Cap/PE Ratio company specific
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    #plt.savefig(f'plots/CashFlow_{ticker}.png')
#%%
# 5 year Market Cap/PE Ratio company specific
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    #plt.savefig(f'plots/CashFlow_{ticker}.png')

#%%
# 10 year Market Cap/PE Ratio company specific
companies = ['LMT', 'RTX', 'BA' , 'GD', 'GE', 'HII', 'LHX']

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
    #plt.savefig(f'plots/CashFlow_{ticker}.png')

#%%

# Market Cap and P/E Ration
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
    #plt.savefig('plots/CashFlowDiv_All.png', dpi=300)
    
    time = time.dropna()
    fig, ax1 = plt.subplots(dpi=300)
    fig = sns.lineplot(data=time, x='date', y='PeRatio', hue='ticker')
    plt.xlabel('Year')
    plt.xticks(rotation=45)
    plt.ylabel('P/E Ratio')
    plt.title('P/E Ratio')
    #plt.savefig('plots/CashFlowRepurchase_All.png', dpi=300)





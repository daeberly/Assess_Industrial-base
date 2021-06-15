import pandas as pd
import os

#
#  Files to process
#

files = [
    'HII_quarterly_balance-sheet.csv',
    'HII_monthly_valuation_measures.csv',
    'HII_quarterly_cash-flow.csv',
    'HII_quarterly_financials.csv'
    ]

#
#  Blank dataframe to hold the accumulated data
#

stack_all = pd.DataFrame()

#
#  Read the files one by one and stack the data onto stack_all
#

for f in files:

    raw = pd.read_csv(f,dtype=str)
    
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
    print( f'Duplicates seen in {f}:', dups.sum() )
    
    # convert Series to Dataframe
    stk = stk.toframe()
        
    # add ticker to data
    ticker = os.path.splitext(os.path.basename(file))[0]
    ticker = ticker.split('_')[0]     
    raw_data ['ticker'] = ticker
    
    #  append the data to the main stack

    stack_all = stack_all.append(stk.to_frame())


#
#  Show the result for checking
#

print( stack_all )

#
#  Turn the names into columns
#

uns = stack_all.unstack('name')['value']

#
#  Get rid of TTM, convert dates, and sort
#

uns = uns.drop('ttm',axis=0)
uns['date'] = pd.to_datetime( uns.index )
uns = uns.set_index('date')
uns = uns.sort_index()

# 
#  Show results for checking and save to CSV
#

print( uns )
uns.to_csv('hii.csv')

ticker in row
split on _ & take element [0]
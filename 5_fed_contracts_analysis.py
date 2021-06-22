# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:48:06 2021

@author: eberly
"""

#
# Contract info
#

# Sources: 
    # USA Spending.gov 
        # https://www.usaspending.gov/download_center/custom_award_data        
        # https://www.usaspending.gov/download_center/dataset_metadata
    # Congressional, State & Zipcode shapefiles
        # https://www.census.gov/cgi-bin/geo/shapefiles/index.php

# References:
    # glob https://pynative.com/python-glob/
    # zipfile https://docs.python.org/3/library/zipfile.html
    # pd.concat https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html
    # geopandas https://geopandas.org/docs.html
        # coordinate systems https://epsg.io/?q=26918
    
import glob
import zipfile
import pandas as pd
import datetime

start_time = datetime.datetime.now()

from scipy.stats import skew, mode
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas                  # for state/congressional district totals


#%%
#
# Import .pkl.zip data
#

# .pkl.zip options: 'FY21_contracts.pkl.zip' or 'FY20_contracts.pkl.zip'

sample = pd.read_pickle('clean_data/FY21_contracts.pkl.zip')
print (sample.dtypes)
print (sample.shape)

# Look for duplicates
dups = sample.duplicated( subset=['usaspending_permalink'], keep=False )
print( '\nduplicate records:', dups.sum() )

dup_rec = sample[ dups ]
#print( dup_rec.sort_values('last_modified_date') ) 
#%%

#
# Clean entry names
#

names = {'ORDER DEPENDENT (IDV ALLOWS PRICING ARRANGEMENT TO BE DETERMINED SEPARATELY FOR EACH ORDER)' : 'ORDER DEPENDENT',
         'FIXED PRICE WITH ECONOMIC PRICE ADJUSTMENT' : 'FIXED PRICE - ECONOMIC PRICE ADJUSTMENT'
         } 

sample = sample.replace( names )

#
# Select contracts based on start date
#       Data includes multi-year contracts starting back to 1993
#

# keep FY start date
start_date = '2020-10-01'

df_start = sample.query(' period_of_performance_start_date >= @start_date')

#
# Get unique names of companies
#    ***Manually review list to find different spellings of company names
#

comp = df_start['recipient_parent_name'].sort_values()
dups = comp.duplicated()
print( '\nExtracting list of unique contractor parent names.' )
print( '\nduplicate Parent Name records:', dups.sum() )
comp = comp.drop_duplicates( keep='last')
dups = comp.duplicated()
print( '\nduplicate records remaining:', dups.sum() )
print( '\nList of contracts exported to companies.csv')

comp.to_csv('inputs/full_list_unique_company_names.csv', index=False)


#%%
#
# Aggregate & Describe data
#

# 'awarding_agency_name' i.e. DoD
agg_func = {'potential_total_value_of_award': ['sum'],
            'total_dollars_obligated': ['sum'],
            'award_type': ['count', 'nunique'] ,           
            'type_of_contract_pricing': ['count', 'nunique'],            
            'subcontracting_plan': ['count', 'nunique'],            
            'multi_year_contract': ['count', 'nunique'],            
           }

groups = ['awarding_agency_name'] 

grouped = sample.groupby( groups ).agg( agg_func ).round(1)

# Contracts Awarded (includes multi-year amounts)

agg_sum = {'potential_total_value_of_award': ['sum']}
    # Totals in $Billions (1e9)
award_starts = df_start.groupby( groups ).agg( agg_sum) / 1e9
potential_pct_total = award_starts.assign(pct_total=lambda x: x / x.sum())
potential_pct_total = potential_pct_total.sort_values(by=('potential_total_value_of_award','sum'), ascending= False)
top_10_awarded = potential_pct_total[:10]
top_10_awarded.plot.barh()


# Contract payments obligated for FY (expected to be paid this FY to company)

agg_sum = { 'total_dollars_obligated': ['sum'] }
    # Totals in $Billions (1e9)
obligated = df_start.groupby( groups ).agg( agg_sum) / 1e9
obligated_pct_total = obligated.assign(pct_total=lambda x: x / x.sum())
obligated_pct_total = obligated_pct_total.sort_values(by=('total_dollars_obligated','sum'), ascending= False)
top_10_obligated = obligated_pct_total[:10]
top_10_obligated.plot.barh()


#%%

#
# Contract Types - Entire Fed Government
#

#
# Contract Type vs. Pricing - Counts

types_grouped = df_start.groupby( ['type_of_contract_pricing' ,'award_type'])['federal_action_obligation'].count()
types_grouped = types_grouped.to_frame()
uns = types_grouped.unstack('award_type')['federal_action_obligation']
uns = uns.fillna(0)

# Heat map
sns.set_theme(context='paper')
fig, ax = plt.subplots( figsize=(7,4))
ax = sns.heatmap(uns, linewidths = .5, cmap="Blues", annot=True, fmt='g')
ax.set_xlabel(' ')
ax.set_ylabel(' ')
plt.title('FY21 Contract Pricing Type by Award Type',fontsize=12)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('plots/contracts/FY21_pricingType_Vs_awardType_heatmap.png', dpi=300)

#
# Contract Type vs. Pricing - $ totals

types_grouped = df_start.groupby( ['type_of_contract_pricing' ,'award_type'])['total_dollars_obligated'].sum() / 1e6
types_grouped = types_grouped.to_frame()
uns = types_grouped.unstack('award_type')['total_dollars_obligated']
uns = uns.fillna(0).round(2)

# Heat map
sns.set_theme(context='paper')
fig, ax = plt.subplots( figsize=(7,4) )
ax = sns.heatmap(uns, linewidths = .5, cmap="Greens", annot=True, fmt='g')
ax.set_xlabel(' ')
ax.set_ylabel(' ')
plt.title('FY21 Total Obligations, in millions ', fontsize=14)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('plots/contracts/FY21_obligated_byContractAwardTypes_heatmap.png', dpi=300)


# Contract Types - DoD only

groups = ['awarding_agency_name'] 

names = {'ORDER DEPENDENT (IDV ALLOWS PRICING ARRANGEMENT TO BE DETERMINED SEPARATELY FOR EACH ORDER)' : 'ORDER DEPENDENT',
         'FIXED PRICE WITH ECONOMIC PRICE ADJUSTMENT' : 'FIXED PRICE - ECONOMIC PRICE ADJUSTMENT'
         } 

sample = sample.replace( names )

contract_types = df_start.groupby( groups )['type_of_contract_pricing'].value_counts()
types = contract_types.to_frame()
types = types.rename( columns= {'type_of_contract_pricing': 'total'})
types = types.reset_index()

types_DoD = types.query(" awarding_agency_name == 'DEPARTMENT OF DEFENSE (DOD)' ")

# Heat map
DoD_map = types_DoD.pivot("type_of_contract_pricing", "awarding_agency_name", "total")
DoD_map = DoD_map.sort_values( by= 'DEPARTMENT OF DEFENSE (DOD)', ascending = False)

sns.set_theme(context='paper')
fig, ax = plt.subplots( figsize=(7,4))
ax = sns.heatmap(DoD_map, linewidths = .5, cmap="Greens", annot=True, fmt='g')
ax.set_xlabel(' ')
ax.set_ylabel(' ')
plt.title('Number of Contracts Types in FY21')
plt.tight_layout()
plt.savefig('plots/contracts/FY21_contract_types_heatmap_DoD.png', dpi=300)


#%%

#
# Stats on select Defense Industrial Base Companies
#

#
# Create dataframe with select companies from *manually* cleaned list 
#

comps = pd.read_csv('inputs/DIB_companies.csv')
comps_data = df_start.merge(comps, 
                             how="outer", 
                             on=['recipient_parent_name'], 
                             validate="m:m",
                             indicator=True)
# check clean merge
print(comps_data['_merge'].value_counts())

DIB_data = comps_data.query(( " _merge == 'both' "))

#%%

#
# Stats on select Defense Industrial Base Companies
#


names = DIB_data['std_name'].drop_duplicates( keep='first').to_list()

for company in names:
    
    #
    # Contract Type vs. Award Type - counts per type
    #
    
    temp = DIB_data.query( " std_name == @company " )
    types_grouped = temp.groupby( ['type_of_contract_pricing' ,'award_type'])['federal_action_obligation'].count()
    types_grouped = types_grouped.to_frame()
    uns = types_grouped.unstack('award_type')['federal_action_obligation']
    uns = uns.fillna(0)

    # Heat map
    sns.set_theme(context='paper')
    fig, ax = plt.subplots( figsize=(7,4))
    ax = sns.heatmap(uns, linewidths = .5, cmap="Blues", annot=True, fmt='g')
    ax.set_xlabel(' ')
    ax.set_ylabel(' ')
    plt.title(f'{company} - FY21 Contract Pricing Type by Award Type',fontsize=12)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f'plots/contracts/FY21_pricingType_Vs_awardType_heatmap_{company}.png', dpi=300)

    #
    # Contract Type vs. Award Type - $ obligations per type
    #
    
    types_grouped = temp.groupby( ['type_of_contract_pricing' ,'award_type'])['total_dollars_obligated'].sum() / 1e6
    types_grouped = types_grouped.to_frame()
    uns = types_grouped.unstack('award_type')['total_dollars_obligated']
    uns = uns.fillna(0).round(2)
    
    # Heat map
    sns.set_theme(context='paper')
    fig, ax = plt.subplots( figsize=(7,4) )
    ax = sns.heatmap(uns, linewidths = .5, cmap="Greens", annot=True, fmt='g')
    ax.set_xlabel(' ')
    ax.set_ylabel(' ')
    plt.title(f'{company} - FY21 Total Obligations, in millions ', fontsize=14)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f'plots/contracts/FY21_obligated_byContractAwardTypes_heatmap_{company}.png', dpi=300)
    
#%%

#
# Housekeeping
#

print( '\nPart 5 Complete = Great Success!)

end_time = datetime.datetime.now()

time_diff = (end_time - start_time)

print('\nTotal Processing Time:', time_diff, 'hr:min:secs\n')



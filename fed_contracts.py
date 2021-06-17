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
import time
start = time.time()

import matplotlib.pyplot as plt
import geopandas                  # for state/congressional district totals


#
# Import Federal Contract Data
#


# Columns to keep from USA Spending report

raw = pd.read_csv('Contract_Categories.csv')
keep = raw.Columns.to_list()


# Set data type in columns 

dates = ['action_date', 
         'period_of_performance_start_date', 
         'period_of_performance_potential_end_date',
         'last_modified_date']

data_types = {'recipient_zip_4_code': str,
            'recipient_congressional_district': str,
            'primary_place_of_performance_zip_4': str,
            'primary_place_of_performance_congressional_district':str}


# Location of external hard drive

folder = '//tplinkwifi.net/G/Workshop - GAO/'

fy21_data = 'contract_data/'
fy20_data = 'FY20_data/'

# Combine all .csv files in zipfile into 1 dataframe
    # FY20 unzipped  5.7GB
'''    
# Don't know how to fix error

# Option 1
#   pull certain .csv files out of .zip
    
for zip_file in glob.glob( folder + fy20_data + '*.zip' ):
    zf = zipfile.ZipFile(zip_file)
    
    for file in zf.namelist():
       if file.startswith('All_Contracts_Prime'):
           print ( file )
           csv_file = pd.read_csv(zf.open( file ), 
                                  header=0, 
                                  usecols= keep, 
                                  parse_dates=( dates ),
                                  dtype=( data_types ))
           
    combined_csv = pd.concat(csv_file,ignore_index=True)  # 'concat' joins each dataframe 
    print("\nTotal (rows,columns) in 'combined_csv': ",combined_csv.shape)

# TypeError: first argument must be an iterable of pandas objects, you passed an object of type "DataFrame"
    # line 90 Troubleshooting 
        # adjusted indent
        # 
    # Fix... ?

'''
#   Option # 2. 
#       .csv files must be extracted from .zip

combined_csv = pd.DataFrame()

for file in glob.glob( folder + fy21_data + '*.csv' ):

    raw = pd.read_csv( file, 
                      header=0, 
                      usecols= keep, 
                      parse_dates=( dates ),
                      dtype=( data_types ))
    
    combined_csv = combined_csv.append( raw )

print("\nTotal (rows,columns) in 'combined_csv': ",combined_csv.shape)


# Create a subset of data to develop code for this dataset

sample = combined_csv.sample(frac=.05)
print('\n', sample.dtypes )
print("\nTotal (rows,columns) in 'sample': ",sample.shape)
sample.to_pickle('sample_contracts.pkl.zip')

print('\nGreat Success!\nsample_contracts.pkl.zip exported.\nReady to code...')

end = time.time()
print('\nProcessing Time:', round(end-start,2), 'seconds\n')


#%%

#
# Import .pkl.zip data
#

sample = pd.read_pickle('sample_FY21_contracts.pkl.zip')
print (sample.dtypes)
print (sample.shape)

#%%

#
# Import shapefiles
#

folder = '//tplinkwifi.net/G/Workshop - GAO/shapefiles/'

geo_zipcodes = geopandas.read_file( folder +'tl_2020_us_zcta510.zip')
geo_cong_districts = geopandas.read_file( folder +'tl_2020_us_cd116.zip')
geo_states = geopandas.read_file( folder +'tl_2020_us_state.zip')
geo_mil_bases = geopandas.read_file( folder +'tl_2020_us_mil.zip')

shapefiles = [geo_zipcodes, geo_cong_districts, geo_states, geo_mil_bases ]

'''
# Do I need to reset CRS if census data already in NAD83?
for file in shapefiles:
    file = file.to_crs(epsg= )
'''

#%%

#
# Get summaries & plot
#

# groupby() https://pandas.pydata.org/pandas-docs/stable/reference/groupby.html
# Should I rename the columns in dataframe so they appear of graphs nicer?
    # example: 'award_type' should be 'Award Type'
    # or..not worth the effort

## Overall Contract Trends

#1 Totals:
    # float('potential_total_value_of_awards') 
    # float('total_dollars_obligated')
    # 'number_of_offers_received' per 'award_type' # i.e. fixed price, cost plus
    # 'action_type' per 'award_type'               # i.e.terminated for cause

'''
 interests = pd.read_csv('contract_category_toPlot.csv')
 keep = interests.Columns.to_list()      # 23 variables

for variable in keep:
    # plot vertical bar chart w/ subtotals [sum() or count()] for each unique value in variable
        # label each bar with it's total on top of bar
        # sort bars from largest to smallest
        # title of plot = variable
        # plt.savefig('plots/{variable}.png', dpi=300)
# end loop 
'''    
#2 Subset w/ 'period_of_performance_start_date' & 'potential_total_value_of_award'
    # line graph of money spent over FY
        # x-axis = start Oct 1 end Sep 31 (FY)
        # y-axis = $ Millions ( value_of_award / 1e6 )

#3 - Total 'potential_total_value_of_awards' by 'award_type' for
    # awarding_agency_name = ex. DoD, DHS...all agencies 
    # awarding_agency_name = for DoD only
        # for DoD only... awarding_sub_agency_name
            # subagencies show Navy, Army, AF, Missle Defense, NGIA & combine others
    # recipient_name
        # for only our 7 companies... Lockheed, Raytheon, 
        
## Case Study: Where is the money going? - For DoD data only...  
# Geopandas- total of 'potential_total_value_of_award' (color ramp - green) for...
    # recipient_country_name
    # recipient_zip_4_code 
    
    # country_of_product_or_service_origin
    # place_of_manufacture
        
    # primary_place_of_performance_state_name
    # primary_place_of_performance_zip_4
    # primary_place_of_performance_congressional_district


'''
# 
#  Maps
#

# Ref: https://geopandas.org/docs/user_guide/mapping.html

# Total Value by Country

fig, ax = plt.subplots(1, 1)

world.plot(column='potential_total_value_of_award',
           ax=ax,
           cmap='Greens',
           legend=True,
           legend_kwds={'label': "Contract Value, in millions",
                        'orientation': "horizontal"})
'''

end = time.time()
print('\nTotal Processing Time:', round(end-start,2), 'seconds\n')
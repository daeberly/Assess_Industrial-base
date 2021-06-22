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

    
import glob
import zipfile
import pandas as pd
import datetime

start_time = datetime.datetime.now()

#%%
#
# Import Federal Contract Data
#


# Columns to keep from USA Spending report

raw = pd.read_csv('inputs/Contract_Categories.csv')
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

fy21_data = 'FY21_contract_data/'
fy20_data = 'FY20_contract_data/'

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

for file in glob.glob( folder + fy20_data + '*.csv' ):

    raw = pd.read_csv( file, 
                      header=0, 
                      usecols= keep, 
                      parse_dates=( dates ),
                      dtype=( data_types ))
    
    combined_csv = combined_csv.append( raw )

print('\n', combined_csv.dtypes )
print("\nTotal (rows,columns) in 'combined_csv': ",combined_csv.shape)
'''
# Create a subset of data to develop code for this dataset

sample = combined_csv.sample(frac=.05)
print('\n', sample.dtypes )
print("\nTotal (rows,columns) in 'sample': ",sample.shape)
'''

print('\nImport successful!')
end = time.time()
print('\nProcessing Time to Import files:', round(end-start,2), 'seconds\n')


#%%

#
# 1. REMOVE DUPLICATE RECORDS
# 

# Every time a contract is updated a new row is entered into the dataframe
# The most recently modified record will have accurate totals

# Look for duplicates
dups = combined_csv.duplicated( subset=['usaspending_permalink'], keep=False )
#print( '\nduplicate records:', dups.sum() )

dup_rec = combined_csv[ dups ]
#print( dup_rec.sort_values('last_modified_date') ) 
# 3039 duplicate records in 'sample'

# Keep most recently updated
combined_csv = combined_csv.sort_values('last_modified_date').drop_duplicates(['usaspending_permalink'], keep='last')

# Check
dups2 = combined_csv.duplicated( subset=['usaspending_permalink'], keep=False )
#print( '\nduplicate records:', dups2.sum() )
# 0 duplicates

print('\nDuplicate records found =', dups.sum(), '\nLast modified records kept.' )
print('Duplicate records remaining =', dups2.sum())

#%%

# Export smaller file because of computer MemoryError

raw = pd.read_csv('inputs/Contract_Categories_keep.csv')
keep = raw.Columns.to_list()

refined_combined_csv = combined_csv[ keep ]

refined_combined_csv.to_pickle('clean_data/FY20_contracts.pkl.zip')


#%%

# Export 

combined_csv.to_pickle('clean_data/FY20_contracts.pkl.zip')

print('\nclean_data/contracts.pkl.zip exported.\nReady to code...')

print( '\nPart 4 Complete = Great Success!')

end_time = datetime.datetime.now()
time_diff = (end_time - start_time)
print('\nTotal Processing Time:', time_diff, 'hr:min:secs\n')
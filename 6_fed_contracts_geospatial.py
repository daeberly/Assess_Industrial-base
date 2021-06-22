# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 08:27:43 2021

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
    # geopandas https://geopandas.org/docs.html
        # coordinate systems https://epsg.io/?q=26918
    

import pandas as pd
import datetime
start = time.time()

from scipy.stats import skew, mode
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas                  # for state/congressional district totals

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


# Do I need to reset CRS if census data already in NAD83?
for file in shapefiles:
    file = file.to_crs(epsg= )


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

# plot 
    # circular bar plot https://www.python-graph-gallery.com/circular-barplot-basic
    # tree map https://www.python-graph-gallery.com/treemap/


 interests = pd.read_csv('contract_category_toPlot.csv')
 keep = interests.Columns.to_list()      # 23 variables

for variable in keep:
    # plot vertical bar chart w/ subtotals [sum() or count()] for each unique value in variable
        # label each bar with it's total on top of bar
        # sort bars from largest to smallest
        # title of plot = variable
        # plt.savefig('plots/{variable}.png', dpi=300)
# end loop 

    
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

# publish on github
    # https://www.python-graph-gallery.com/choropleth-map-plotly-python
    


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


#%%

#
# Housekeeping
#

end_time = datetime.datetime.now()

time_diff = (end_time - start_time)

print('\nTotal Processing Time:', time_diff, 'hr:min:secs\n')

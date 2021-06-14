# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 23:57:12 2021

@author: eberly
"""
#
# Bureau of Labor Statistics (BLS)
#

    # PPI codes: https://download.bls.gov/pub/time.series/wp/wp.series
    # PPI details https://download.bls.gov/pub/time.series/wp/wp.txt

# Personal BLS API Key:  91ce6400e7034f558a460b7693529c56
    # API aceess details: https://www.bls.gov/developers/api_faqs.htm#register4
    # API code samples: https://www.bls.gov/developers/api_signature_v2.htm#multiple

import requests
import json
import pandas as pd

# Personal API key
key_value = '91ce6400e7034f558a460b7693529c56'

# Search Parameters
codes =  ['WPU143102','WPU14310201']
    # WPU143102 = 'PPI Commodity data for Transportation equipment-Military self-propelled ships, new construction, not seasonally adjusted',
    # WPU14310201 =
year_start = 2002    # restricted to 20yr window
year_end = 2021

# Prep search request
headers = {'Content-type': 'application/json'}
payload = json.dumps({"seriesid": codes,
                   "startyear":year_start,  
                   "endyear":year_end, 
                   "catalog": "true",
                   "calculations": "false",
                   "annualaverage": "false",
                   "aspects": "false",
                   "registrationkey":key_value
                   })

# Submit & Check search response
response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data= payload, headers= headers)
#print(response.json())

print( '\nurl:', response.url )
print( '\nstatus:', response.status_code )
print( '\n', response.text )

if response.status_code == 200:
    print('Request successful!  Status Code = 200. ')
else:
    print('error', response.status_code, response.text)
    assert False
    
#%%

#
# Convert json result to dataframe
#

# Save json result to Panda dataframe
result = response.json()
print(result)
#print( json.dumps(result,indent=4) )
#print(result.keys())

series_list = result['Results']['series']
for series in series_list:
    s_id = series['seriesID']
    s_cat = series['catalog']
    s_dat = series['data']
    dat = pd.DataFrame.from_records( s_dat )
    print( s_id )
    print( s_cat )
    print( dat )
    


#%%

'''
#
# Bureau of Labor example 
#

#pip install PrettyTable
import prettytable

json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
'''
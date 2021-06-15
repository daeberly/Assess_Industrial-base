# Created: 6-3-2021
# GitHub Repository: Assess_Industrial-bas
# https://github.com/daeberly/Assess_Industrial-base


#
# Scrap text from SEC reports
#

'''
I would like to make this whole thing a function that we can just throw 
a list of companies and words in, then have it pull it all from their 10Ks

reference: https://codingandfun.com/sec-annual-reports-python/

def Sec_10Ks(companies, key_words):
'''

import bs4 as bs    # BeautifulSoup to scrape web data
import requests
import nltk    # nltk is natural language tool kit

#
## 1. USER INPUT: Change the Company name & info you'd like
#

# https://www.sec.gov/edgar/searchedgar/companysearch.html
company = 'RAYTHEON TECHNOLOGIES CORP' # company name is case sensitive - look it up on SEC website

words_to_find = 'research and development'
    # Examples: COVID-19, supply chain, risks, raw materials, workforce, China,
    # primary customer, contracts with the U.S. government

filing = '10-Q'    # options: '10-K', '10-Q', etc...
year = 2020         
quarter = 'QTR2'


#
## 2. Build url to get the SEC report 
#
    
# get a list with all SEC reports 
download = requests.get(f'https://www.sec.gov/Archives/edgar/full-index/{year}/{quarter}/master.idx').content
download = download.decode("utf-8").split('\n')

# finds the report for a specific company &
# makes the url to access that report
for item in download:
  #company name and report type
  if (company in item) and (filing in item): 
    print(item)
    entry = item
    entry = entry.strip()
    split_entry = entry.split('|')
    url = split_entry[-1]
    print('url', url) # edgar/data/936468/0000936468-21-000013.txt

url2 = url.split('-') 
url2 = url2[0] + url2[1] + url2[2]
url2 = url2.split('.txt')[0]
    #print(url2) # edgar/data/936468/000093646821000013

to_get_html_site = 'https://www.sec.gov/Archives/' + url
data = requests.get(to_get_html_site).content
data = data.decode("utf-8") 
data = data.split('FILENAME>')  # split the file in half after this
    #data[1]
data = data[1].split('\n')[0]   # split 2nd half after the line break & keep the filename

url_to_use = 'https://www.sec.gov/Archives/'+ url2 + '/'+data
print('\nSEC report website:', url_to_use)

# get the desired SEC report 
resp = requests.get(url_to_use)
soup = bs.BeautifulSoup(resp.text, 'lxml')

#
## 3. Extract specific sentences from SEC Report
#


# Only need this once to download tool kit
#nltk.download('punkt')

# Output Header
print('\n****\n' + str(year) +' SEC ' + filing + ' report for ' + company)
print("\nExcerpts below related to '" + words_to_find + "'.\n")

# Sentences related to target words
for tag in soup.div.find_all_next('span'):  # spans are parts of the html webdoc
    #print(type(tag))
    tag = tag.getText()
    #print(tag)
    if words_to_find in tag:
      sentences = nltk.sent_tokenize(tag)
      result = [sentence for sentence in sentences]
      print(result, '\n ****')
      
print('End of search.')

#%%

#
# Create report (.pdf)
# 

#pip install reportlab
from reportlab.pdfgen import canvas

filename = company + 'SEC_report'
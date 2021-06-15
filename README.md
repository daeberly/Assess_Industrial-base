# Assess_Industrial-base

## Data Collection
.py files
1. 'scrape_SEC_reports.py' pulls text from a company's SEC filling (i.e, 10-Q, 10-K). 
1. 'financials.py' combines & cleans Yahoo Finance reports...
1. 'analysis.py' calculates ratios, analyzes , plot, & forecasts...
3. 'API_data_BureauOfLabor.py' get BLS data...

Next steps:
1. 'financials.py' - clean up duplicates in DIB_Financials, add R&D dataframe
1. 'analysis.py' - calculations, analyze, plot & forecast for report 
3. 'scrape_SEC_reports.py' - not sure if its useful for the report; possibly set up to export a pdf with extracted sentences based on search criteria. Create a loop to look at each company's filing and search criteria i.e. "COVID-19" and have a pdf per company or combined pdf.

### Samples
1. '2021-06-14_sample_DIB_Financials.csv' is a sample of combined finance reports with >200 financial measures (i.e. Total Revenues, P/E ratio) downloaded from Yahoo Finance. Yahoo Finance pulls data from SEC filings. Records were spot checked for accuracy. Date Range: 2021-1980s. Frequency: Quarterly. 
2. '2021-06-14_sample_stock_info.csv' is a sample from yFinance free library that pulls from Yahoo Finance stock records. Date Range: 2021-1980s. Frequency: Daily.

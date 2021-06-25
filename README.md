# Assess_Industrial-base

## Data Collection
.py files
1. '1_inputs.py' (1) imports .csv files in raw_data exportedfrom Yahoo Finance and (2) downloads daily stock information from the Yahoo Finance API dating back to 1985. It then reformats the raw data and creates Pandas dataframes for analysis.
1. '2_analysis.py' cleans dataframes, creates timeframes, calculates ratios (Accounts Payable Turnover (APT), APT days, ROE, and ROA) and normalized ratios for the start day of our 10-, 5-, 3-, and 1-year time frames.
1. '3_plots.py' creates all figures and tables used in our report to the GAO.

Results from these .py files were omitted from the report because results from datasets required addition analysis.
1. '4_fed_contracts.py' (1) imports user provided USAspending contract reports and (2) creates a Pandas dataframe for analysis.
1. '5_fed_contracts_analysis.py' (1) aggregates contact data for user-defined categories of any number of agencies or companies, then (2) produces figures and heatmaps 

.py files used during research
1. 'scrape_SEC_reports.py' pulls text from a company's SEC filling (i.e, 10-Q, 10-K). 

### Samples
1. '2021-06-14_sample_DIB_Financials.csv' is a sample of combined finance reports with >200 financial measures (i.e. Total Revenues, P/E ratio) downloaded from Yahoo Finance. Yahoo Finance pulls data from SEC filings. Records were spot checked for accuracy. Date Range: 2021-1980s. Frequency: Quarterly. 
2. '2021-06-14_sample_stock_info.csv' is a sample from yFinance free library that pulls from Yahoo Finance stock records. Date Range: 2021-1985. Frequency: Daily.

### Example figures

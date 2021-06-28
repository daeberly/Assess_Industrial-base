# Assess the "health" of the Defense Industrial base
This respository supports the research and analysis conducted during our gradute capstone project at the Syracuse University Maxwell School for the Government Accountability Office (GAO), Contracting and National Security Acquisition (CNSA) Team.

Our goal was to create an auditable, repeatable and customizable analysis. This repository was not a requested deliverable. The code here collects, combines, analyzes and plots financial data for eight financial measures on seven companies. Our analysis looks at four time periods - 10, 5, 3 and one year intervals. Customizable user-imputs can easily change our seven to 1,000s of companies and any number of financial measures or ratios. 

Of note, USAspending federal contractor data was explored but results were not included in the report due to time-limitations of this project to confirm multi-year contracts were not counted more than once when aggregating results.

### Project Scope
"Only using on publicaly available data, identify indicators to assess the health of the Defense Industrial base (DIB) to include a specific focus on impacts of COVID-19."

Over 21 days, our research spanned from defense industry professionals to a former DOD Under Secretary on Industrial Policy to congressional and non-profit DIB studies. Large in scope, our project was refined to only financial indicators, mainly information derived from  SEC-10K (annual) and SEC-10Q (quarterly) balance sheets and qualitative measures. 

In the end, we focused on eight financial indicators, risks identified in SEC-10Ks and used seven of the top Department of Defense prime contractors. Using only publicly available information, our analysis was limited to only U.S. publicly traded companies. Also, by focusing on seven companies, we assessed the validity and effectiveness of our financial measures. Overall, our measures provided a good overall financial assessment, but should be complimented by SEC-10K text to best understand trends. Lastly, health of DIB companies should be assess in relation to their commercial sector and not the DIB as a whole.

DoD Primes evaluated:

Lockheed Martin (LMT)   Boeing (BA)   L3Harris (LHX)  General Dynamics (GD)  
Raytheon Technologies (RTX)  Huntington Ingalls (HII) General Electric (GE)

Indicators...

*Overall Financial Health*: Return on Equity (ROE), Return on Assets (ROA), Market Cap, P/E Ratio, Stock Prices

*Behavioral Indicators*: Accounts Payable Turnover in days, Dividends, Capital Stock Repurchases, Research and Development

### Data Sources 
1. SEC 10-K & 10-Q. Primary source of all data - quantitative (i.e., net income, cost of revenues) and qualitative (i.e. identified company risks, COVID-19 impacts, reasons for changes in R&D spending). Data frequency - yearly & quarterly.
1. Yahoo Financial Premier. Primary source of SEC quantitative data. Included data back to early 1990s on each company.  Data frequency - monthly & quarterly.
1. yFinance. Primary source of stock prices (i.e., open, close, dividends). Data ranged from today to 1985. Data frequency - daily.

### Code Files (.py)
1. '1_inputs.py' (1) imports .csv files in raw_data exportedfrom Yahoo Finance and (2) downloads daily stock information from the Yahoo Finance API dating back to 1985. It then reformats the raw data and creates Pandas dataframes for analysis.
1. '2_analysis.py' cleans dataframes, creates timeframes, calculates ratios (Accounts Payable Turnover (APT), APT days, ROE, and ROA) and normalized ratios for the start day of our 10-, 5-, 3-, and 1-year time frames.
1. '3_plots.py' creates all figures and tables used in our report to the GAO.

Results from these .py files were omitted from the report because results from datasets required addition analysis.
1. '4_fed_contracts.py' (1) imports user provided USAspending contract reports and (2) creates a Pandas dataframe for analysis.
1. '5_fed_contracts_analysis.py' (1) aggregates contact data for user-defined categories of any number of agencies or companies, then (2) produces figures and heatmaps 

#### Code files used for SEC-10K * 10Q research
1. 'scrape_SEC_reports.py' pulls text from a company's SEC filling (i.e, 10-Q, 10-K). 

#### Code Overview & Run Times.
*The beauty of coding...auditable, repeatable, and customizable plus it only takes 2 minutes 17 seconds to run the analysis!*
![image](https://user-images.githubusercontent.com/68342740/123573958-f9c15880-d79c-11eb-9df5-90be11c435de.png)

#### User-Defined parameters
List of companies, financial measures, etc... https://github.com/daeberly/Assess_Industrial-base/tree/main/inputs

#### Example raw data
Quarterly data samples: https://github.com/daeberly/Assess_Industrial-base/tree/main/raw_data <br />
Monthly data samples: https://github.com/daeberly/Assess_Industrial-base/tree/main/raw_monthly <br />
Daily stock data pulled from yfinance API.

#### Examples of cleaned data used in '2_analysis.py' & '3_plots.py'
https://github.com/daeberly/Assess_Industrial-base/tree/main/clean_data

### Example figures generated by "3_plots.py"
More example plots available at: https://github.com/daeberly/Assess_Industrial-base/tree/main/plots
![](https://github.com/daeberly/Assess_Industrial-base/blob/main/plots/Purchase_MarketCap/10yr_MarketCap%26PE_LMT.png)
![](https://github.com/daeberly/Assess_Industrial-base/blob/main/plots/R%26D/All_RD_heatmap.png)
![](https://github.com/daeberly/Assess_Industrial-base/blob/main/plots/APT/10yr_APTdays_all.png)


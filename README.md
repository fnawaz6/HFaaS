# HFaaS
Hedge Fund As A Service
_________________
## Done so-far:
- Read Financial Stamenets From Google Finance:
    - Available Data: 2014Q1-2017Q3
    - Module: downGoogle
    - Purpose: to use a benchmark
- Financial Statements from EDGAR (consolidated quarterly)
    - Available Data: 2009Q1-2017Q3
    - Module: sec2df
    - Purpose: the main source of financial statements
_____________________
## To-Do
- Read daily 10-K, 10-Q 
    - Purpose: to read reports submitted on daily basis before going to quarterly consolidated
    - url: 
    - Tasks:
        - Read one report: https://www.sec.gov/Archives/edgar/data/1416697/000112785517000297/0001127855-17-000297-index.htm
        - Make a list of daily urls to read
        - Read all latest reports since some date
    - Read means reading data into dataframe, converting to our data base

- Make a mapping list of items from SEC to Google

- Create Ready to go datasets:
    - 10-K, 10-Q (raw data)
    - A, Q (standard data)
    - Covers 10 years and 8000 companies

- Contact with Quandl and others to sell
___________________
## Code Files
- Program main.py: the logic and test
- Module sec2df.py: read SEC data
- std2items.tsv from google standard sheets to our standard
- Module downGoogle.py: code to download google finance
- File Readme.md: Contains to-do, Outputs, objectives, project management, Bugs, Data Sources, Scope, Iteration, ...
___________________
## Output Files

___________
## Input and Archive Files

_____________
Directories:
- DevCodes: all devcodes, shared on github
    - Main.py
    - Sec2df.py
    - Readme.md
    - downGoogle.py
- Input
    - SEC
        - Archive
- Output
- Temp

_________
## Language
Python 3.6+
____________
## Objectives
1. API call to fetch "distilled/processed" financial data about all US stocks
    * Daily Prices
    * Fundemental: Income Statement, Balance Sheet, Cash Flow
2. API call to provide "intrinsic value" of a stock based on Machine Learning and Asset Pricing
3. API call to provide "best/better investment" similar to a given stock
4. API call to analyze the performance of a portfolio
5. API call to clean SEC 10k and 10Q data and pickle
_________
## Phase1: API call to fetch financial Data
    HFetch (FirmSymbol, Frequency='D', Start_date, End_date, Statement='Price', Item)
    * Load data (Price and Fundemental) into class Firm and pickle
    * readIn method from csv file
    * downLoad method from websites
___________
## Iteration 1.1: file name: Firm.py
- Readin 1 Quarter (2017Q3) data from SEC Edgar:  
ReadSEC(url="https://www.sec.gov/files/dera/data/financial-statement-data-sets/", file="2017q3.zip") -> Data.DataSet 
    - Download from: https://www.sec.gov/files/dera/data/financial-statement-data-sets/2017q3.zip
    - Store it in proper format (To Discuss!!!) 
    - Write it into DataBase format or BigData format (Extra feature)
- Read in 7 files from finance.google and store it in proper format and write a program to do it automatically
- Transform IBM from quarterly to standard format (as in google)
___________
## Liscense
- All rights belongs to the contributors
______________
## Data Sources:
- Accounting Datasets:
https://www.sec.gov/dera/data/financial-statement-data-sets.html

- Latest 10-Q reports on Edgar:
https://www.sec.gov/cgi-bin/browse-edgar?&type=10-Q&count=100&action=getcurrent&output=atom

- Accessing EDGAR data:
https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm

- CIK lookup:
https://www.sec.gov/Archives/edgar/cik-lookup-data.txt

- Researching Edgar:
https://www.sec.gov/oiea/Article/edgarguide.html

- Edgar Developer Resource page:
https://www.sec.gov/developer

- Google Finance:
finance.google.com

______________
## Bugs
- 
___________________
## Trash
- centurylink cancellation confirmation: d75573679
__________________

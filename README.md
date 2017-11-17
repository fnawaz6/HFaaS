# HFaaS
Financial Services App

# Code Files
- main.py: the logic
- firm.py all methods of Firm class
- firms.py
- std2items.tsv from google standard sheets to our standard
- Bug.md: all bugs to be resolved
- downgoogle.py: code to download google finance

_________
## Language
Python 3.6+

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
All rights belongs to the contributors


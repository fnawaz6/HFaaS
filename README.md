# HFaaS
"Hedge Fund as a Service" uses Machine Learning and Asset Pricing science
***

## Contribution
If you like to be part of this project email me alan.khosro at gmail

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

## Current Release Goal
1. API call to fetch financial Data
    HFetch (FirmSymbol, Frequency='D', Start_date, End_date, Statement='Price', Item)
    * Load data (Price and Fundemental) into class Firm and pickle
    * readIn method from csv file
    * downLoad method from websites
## Liscense
All rights belongs to the contributors


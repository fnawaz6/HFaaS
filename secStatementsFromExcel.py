import pandas as pd
from dateutil import parser
 
url = url_to_excel_file_of_financial_statements = "https://www.sec.gov/Archives/edgar/data/1416697/000112785517000297/Financial_Report.xlsx"

######### Read Income Statement
IS = pd.read_excel(url, sheet_name=3, index_col=0, header=[0,1])
a = IS.stack(dropna=True, level=[0,1]).reset_index()
a.columns = ["item", "qtrs", "date", "value"]
a['value'] = pd.to_numeric(a.value, errors='coerce', downcast='float')
a['date'] = to_date (a['date'])
a['stamp'] = year_qtr(a['date'])
a['qtrs'] = to_qtrs(a['qtrs'])
a = a.assign(stmt="IS", ticker="xxx", report="xxx", uom="USD", cik="xxx", tag="xxx", fisqtr="xxx")

########### Real all financials
url_to_all_filing_by_form_and_quarter = "https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/form.idx"
url_to_latest_filing = "https://www.sec.gov/Archives/edgar/full-index/form.idx"
a = pd.read_fwf(url_to_latest_filing, usecols=[0,4], names=["form","url"], skiprows=11)
a = a.query('form == ["10-K", "10-Q"]')
a['url'] = a['url'].str.replace("-", "")
a['url'] = a['url'].str.replace(".txt", "/Financial_Report.xlsx")
a['url'] = "https://www.sec.gov/Archives/"+a['url']

for i in a:
    read excel tables and stack them and clean them

###############################################
def to_qtrs (periods): # -> quarters as a pd.Series 
    ''' extracts the number of quarters that a period covers,
    for intance "9 months ends" to 3 qtrs'''
    import re
    conversion = pd.Series([.25, 1, 3, 13, 91], index=["yea", "qua", "mon", "wee", "day"], name="perQtr")
    periods = ( periods
        .str.lower().str.extract('(\d) *(\w{3})', expand=True)
        .rename(columns={0:"duration", 1:"unit"})
        .join(conversion, on="unit")
    )
    qtrs = periods['duration'].astype('float').divide(periods['perQtr'])
    return (qtrs.round())
###############################################
def to_date (dates):
    ''' converts input string dates to our format of dates that is integer '''
    return (
        pd.to_datetime(dates, infer_datetime_format=True, errors='coerce')
        .dt.strftime("%Y%m%d")
        .astype(int)
    )
###############################################
def year_qtr (dates):
    ''' converts input string dates to our year-quarter format of stamp as integer'''
    dates = pd.to_datetime(dates, infer_datetime_format=True, errors='coerce')
    return (dates.dt.year*10 + dates.dt.quarter)
###############################################

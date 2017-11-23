import pandas as pd
from dateutil import parser
import re

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

########### Real all financials
url_to_all_filing_by_form_and_quarter = "https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/form.idx"
url_to_latest_filing = "https://www.sec.gov/Archives/edgar/full-index/form.idx"
a = pd.read_fwf(url_to_latest_filing, usecols=[0,1,4], names=["form","company","url"], skiprows=11) #Modified to get company name
a = a.query('form == ["10-K", "10-Q"]')
a['url'] = a['url'].str.replace("-", "")
a['url'] = a['url'].str.replace(".txt", "/Financial_Report.xlsx")
a['url'] = "https://www.sec.gov/Archives/"+a['url']
#Start of Adding below 2 lines, to adjust the index
a = a.reset_index()
a = a.drop('index',axis=1)
#End

######### Read General Information
def read_gi(url,i):
    xl = pd.ExcelFile(url)
    sheetn = re.findall('document and entity information',str(xl.sheet_names),re.IGNORECASE)[0]    
    GI = pd.read_excel(url, sheetname=sheetn, index_col=0, header=[0,1])
    b = GI.stack(dropna=True, level=[0,1]).reset_index()
    b.columns = ["item", "qtrs", "date", "value"]
    #b['value'] = pd.to_numeric(b.value, errors='coerce', downcast='float')
    b['stamp'] = year_qtr(b['date']) #moved the stamp statement up, to pass it as datetime for year_qtr - fixed 19703 to correct year
    b['date'] = to_date(b['date'])
    b['qtrs'] = to_qtrs(b['qtrs'])
    b = b.assign(company = a['company'][i], stmt="GI", ticker="xxx", report="xxx", uom="xxx", cik="xxx", tag="xxx", fisqtr="xxx") #added company column
    return b
    
######### Read Income Statement
def read_is(url,i):  
    xl = pd.ExcelFile(url)
    sheetn = re.findall('consolidated statements of oper',str(xl.sheet_names),re.IGNORECASE)[0]
    IS = pd.read_excel(url, sheetname=sheetn, index_col=0, header=[0,1])
    c = IS.stack(dropna=True, level=[0,1]).reset_index()
    c.columns = ["item", "qtrs", "date", "value"]
    #c['value'] = pd.to_numeric(b.value, errors='coerce', downcast='float')
    c['stamp'] = year_qtr(c['date']) #moved the stamp statement up, to pass it as datetime for year_qtr
    c['date'] = to_date(c['date'])
    c['qtrs'] = to_qtrs(c['qtrs'])
    c = c.assign(company = a['company'][i],stmt="IS", ticker="xxx", report="xxx", uom="USD", cik="xxx", tag="xxx", fisqtr="xxx") #added company column
    return c

#Loop to read all the financial excels with General Information
i = 0
while i < a.shape[0]:
    try:
        df_gi_temp = read_gi(a['url'][i],i)
        if i == 0:
            df_gi = df_gi_temp
        else:
            df_gi = df_gi.append(df_gi_temp,ignore_index=True)
        i=i+1
        del df_gi_temp
    except:
        i=i+1
        pass

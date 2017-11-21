import pandas as pd 
 
url_to_excel_file_of_financial_statements = "https://www.sec.gov/Archives/edgar/data/1416697/000112785517000297/Financial_Report.xlsx"

IS = pd.read_excel(url, sheet_name=3, index_col=0, header=[0,1])
pd.to_datetime(IS.columns.levels[1])
a = IS.stack(dropna=True).reset_index()
a.columns = ["item", "date", "value"]
a.value=pd.to_numeric(a.value, errors='coerce', downcast='float')
a = a.dropna()
pd.to_datetime(a.date)
a.assign(report, stmt, qtrs, stamp, date)



url_to_all_filing_by_form_and_quarter = "https://www.sec.gov/Archives/edgar/full-index/2017/QTR4/form.idx"
url_to_latest_filing = "https://www.sec.gov/Archives/edgar/full-index/form.idx"
a = pd.read_fwf(url_to_latest_filing, usecols=[0,4], names=["form","url"], skiprows=11)
a = a.query('form == ["10-K", "10-Q"]')
a['url'] = a['url'].str.replace("-", "")
a['url'] = a['url'].str.replace(".txt", "/Financial_Report.xlsx")
a['url'] = "https://www.sec.gov/Archives/"+a['url']

for i in a:
    read excel tables and stack them and clean them

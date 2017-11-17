import pandas as pd
cik2ticker = pd.read_csv ("cik2ticker.csv")[['cik', 'ticker']]
#################################################################
''' read financial data submitted to SEC by corporations for each quarters
and acleans and re-creates 10-K and 10-Q datasets'''
def read_sec(path="C:\\Github\\HFaaS\\temp\\2017q3\\", cik2ticker=None, encoding="latin"): #-> pd.DataFrame
    ##### read num, pre, sub, cik2ticker; 
    num = (
        pd.read_table(path+"num.txt", encoding=encoding) 
        .query('value.notnull()')
        #.query('coreg.notnull()') # filter submitted as a coregistrant
        #num[num['ddate']<=int(dt.now().strftime('%Y%m%d'))] # filter values for future date
    )
    pre = (
        pd.read_table(path+"pre.txt", encoding=encoding)
        #.query(('stmt==["BS", "IS", "CF", "EQ", "CI"]')
    )
    #tag = pd.read_table (secPath+"tag.txt", encoding=encode)
    sub = (
        pd.read_table(path+"sub.txt", encoding=encoding) 
        #.query('form==["10-K", "10-Q", "10-K/A", "10-Q/A"]')
        .merge(cik2ticker, on="cik", how='left')
    )
    ##### merge all to df; create stamp and fiscal; select columns; 
    df = (num 
        .merge(pre, on=["adsh", "tag", "version"], how="left") 
        .merge(sub, on="adsh", how="left") 
        .rename(columns={'plabel':'item', 'ddate':'date'}) 
        .assign(fisQtr = lambda x: fqtr(x.date, x.fye)) 
    )
    ##### create and concat 10-K and 10-Q reports; return dataframe 
    Q10 = (df
        .query('qtrs == [0,1]')
        .assign(report="10-Q")
        .assign(stamp = lambda x: year_qtr(x.date))
    )
    K10 = (df
        .query('qtrs == [0,4] & fisQtr == 4')
        .assign(report="10-K")
        .assign(stamp = lambda x: year_qtr(x.date))
    )
    return (
        pd.concat([K10, Q10], join='outer')
        .filter(['ticker', 'report', 'stmt', 'item', 'uom', 'stamp', 'value', 'cik', 'tag', 'fisqtr', 'date', 'qtrs'])
    )
#################################################################
''' Converts dates of int type to year-quarter integer 20170931 -> 20173'''
 def year_qtr (dates, digits=8):
    year = dates // 10**(digits-4)
    month = dates // 10**(digits-6) % 100
    qtr = (month-1) // 3 + 1
    return year*10+qtr
#################################################################
'''calculates the fiscal quarter for each date given the endyear'''
def fqtr (dates, fYearEnd):
    month = dates // 100 % 100
    fmonth = fYearEnd // 100
    fquarter = (11 + month - fmonth) // 3 % 4 + 1
    return fquarter


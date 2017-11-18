import pandas as pd
#################################################################
def read_sec(path, cik2ticker, encoding="latin"): #-> pd.DataFrame
    ''' reads financial data submitted to SEC by firms for each quarter
    and re-creates 10-K and 10-Q datasets'''
    ##### read num, pre, sub, cik2ticker; 
    num = (
        pd.read_table(path+"num.txt", encoding=encoding) 
        .query('value.notnull() & value != 0')
        #.query('coreg.notnull()') # filter submitted as a coregistrant
        #num[num['ddate']<=int(dt.now().strftime('%Y%m%d'))] # filter values for future date
    )
    pre = (
        pd.read_table(path+"pre.txt", encoding=encoding)
        .query('plabel.notnull()')
        #.query('stmt==["BS", "IS", "CF", "EQ", "CI"]')
    )
    #tag = pd.read_table (secPath+"tag.txt", encoding=encode)
    sub = (
        pd.read_table(path+"sub.txt", encoding=encoding) 
        #.query('form==["10-K", "10-Q", "10-K/A", "10-Q/A"]')
        .merge(cik2ticker, on="cik", how='left')
    )
    ##### merge all to df; create stamp and fiscal; select columns; 
    df = (num 
        .merge(pre, on=["adsh", "tag", "version"], how="inner") 
        .merge(sub, on="adsh", how="inner") 
        .assign(fisQtr = lambda x: fqtr(x.ddate, x.fye)) 
    )
    ##### create and concat 10-K and 10-Q reports; return dataframe 
    Q10 = (df
        .query('qtrs == [0,1]')
        .assign(report="10-Q")
        .assign(stamp = lambda x: year_qtr(x.ddate))
    )
    K10 = (df
        .query('qtrs == [0,4] & fisQtr == 4')
        .assign(report="10-K")
        .assign(stamp = lambda x: year_qtr(x.ddate))
    )
    return (
        pd.concat([K10, Q10], join='outer')
        .rename(columns={'plabel':'item', 'ddate':'date'}) 
        .filter(['ticker', 'report', 'stmt', 'item', 'stamp', 'value', 'uom', 'cik', 'tag', 'fisqtr', 'date', 'qtrs'])
    )
#################################################################
def year_qtr(dates, digits=8):
    ''' Converts dates of int type to year-quarter integer 20170931 -> 20173'''
    year = dates // 10**(digits-4)
    month = dates // 10**(digits-6) % 100
    qtr = (month-1) // 3 + 1
    return year*10+qtr
#################################################################
def fqtr (dates, fYearEnd):
    ''' Calculates the fiscal quarter for each date given the endyear'''
    month = dates // 100 % 100
    fmonth = fYearEnd // 100
    fquarter = (11 + month - fmonth) // 3 % 4 + 1
    return fquarter
#################################################################
def updateSECs (df=pd.DataFrame(), path="C:/Github/HFaaS/Data/SEC/", keep='last'):
    ''' updates existing df of sec data (10-Q and 10_K) from zip files in path
    then archives the added zip files. If you want to add older files use keep="first" '''
    import zipfile, os, shutil
    ### list all zipFiles, for each file, unzip it, read_sec to create sec file, and clean up
    newSecZipFiles = [f for f in sorted(os.listdir(path)) if f.endswith(".zip")]
    for zip in newSecZipFiles:
        print(zip)
        try:
            with zipfile.ZipFile(path+zip) as z:
                z.extractall(path+"temp/")
            new = read_sec(path+"temp/", cik2ticker)
            df = df.append(new)
            df = df.drop_duplicates(subset=['cik', 'report', 'stmt', 'item', 'stamp'], keep=keep)
            shutil.rmtree(path+"temp/")
            shutil.move(path+zip, path+'Archive/'+zip)
        except Exception as e:
            print(zip, e)
    return df
###################################################################




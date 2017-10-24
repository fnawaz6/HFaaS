'''
convention: variable names all small letters, content usual English
The core data structure is map[ticker string]map[report string]dataframe{index:stamp, cols=(stmt, item, unit, value), xtra=...}
'''
##############################
    """ Gets SEC Edgar data from file path, merge, sort, set index by date, and return dataframe
    Args: file path 
    Returns: dataframe
    Raises: nothing """ 

def sec2df (secPath, encode="ISO-8859-1"): ## returns dataframe num
    ticker = pd.read_csv('C:\\Github\\Firms\\cik.csv', index_col='cik')['ticker']
    num = pd.read_table(secPath+"num.txt", encoding=encode).dropna(subset=['value'])
    num = num[num['coreg'].isnull()]
    num = num[num['ddate']<=int(dt.now().strftime('%Y%m%d'))]
    pre = pd.read_table(secPath+"pre.txt", encoding=encode)
    #pre = pre.query('stmt==["BS", "IS", "CF", "EQ", "CI"]')
    #tag = pd.read_table (secPath+"tag.txt", encoding=encode)
    sub = pd.read_table(secPath+"sub.txt", encoding=encode)
    sub = sub.query('form==["10-K", "10-Q", "10-K/A", "10-Q/A"]')
    sub = sub.join(ticker, on='cik', how='inner')[['adsh', 'ticker', 'form', 'fye']]
    # merge all to num
    num = num.merge(sub, how='inner', on='adsh')
    delta = (30*((num.ddate%10000)//100)+num.ddate%100 -  30*((num.fye%10000)//100)-num.fye%100)/90 ## Difference in days divided by 90
    delta = delta.round()
    num['fQuarter'] = np.where(delta>0, delta, delta+4)
    num = num.merge(pre, on=['adsh', 'tag', 'version'], how='left')
    # create report to separate 10-K and 10-Q
    q10 = num.query('qtrs == [0, 1]').assign(report="10-Q")
    k10 = num.query('qtrs == [0, 4] & fQuarter==4').assign(report="10-K")
    num = pd.concat([k10, q10])
    # standardize column names
    num.rename(columns={'plabel':'item', 'ddate':'date'}, inplace=True)
    num = num[['ticker', 'report', 'date', 'stmt', 'item', 'value', 'uom', 'tag', 'line', 'qtrs' , 'fQuarter']]
    return(num)

###########################################
def df2firms (df, firms, nth=0):
    df = df.dropna(subset=['ticker','report','item', 'value'])
    for ticker, reports in df.groupby(["ticker"]):
        print(ticker)
        print(dt.now())
        reports.drop('ticker', axis=1, inplace=True, errors='ignore')
        firm = firms.get(ticker, {})
        for report, data in reports.groupby(['report']):
            data.drop('report', axis=1, inplace=True, errors='ignore')
            data.set_index(stamp(data['date'], report), inplace=True)
            data = pd.concat ([data, firm.get(report)], join='outer', axis=0)
            data = data.groupby(['stamp', 'stmt', 'item'], sort=False, as_index=False).nth(nth)
            #.sort_index(ascending=False)
            firm[report] = data
        firms[ticker] = firm

########################################
def stamp (dates, report): 
    if report in ['Annual', 'A', 'Y']:
        dates = dates.astype(str).str[-10:].values
        return(pd.to_datetime(dates).astype('period[A]').rename('stamp'))
    elif report in ['Quarterly', 'Q']:
        dates = dates.astype(str).str[-10:].values
        return(pd.to_datetime(dates).astype('period[Q]').rename('stamp'))
    elif report in ['M']:
        dates = dates.astype(str).str[-10:].values
        return(pd.to_datetime(dates).astype('period[M]').rename('stamp'))
    elif report in ['D']:
        dates = dates.astype(str).str[-10:].values
        return(pd.to_datetime(dates).astype('period[D]').rename('stamp'))
    else:
        return(pd.to_datetime(dates).rename('stamp'))

############################
def updateSECs (firms, secPath = "C:\\Github\\SEC\\Unused\\", old=False):
    if old:
        nth=-1
    else:
        nth=1
    errFiles=[]
    for file in sorted(os.listdir(secPath), reverse=old):
        try:
            print(file)
            ref = zipfile.ZipFile(secPath+file)
            zipdir = secPath+"zip\\"
            ref.extractall(zipdir)
            ref.close()
            num = sec2df(zipdir)
            df2firms (num, firms, nth=nth)
        except:
            print(file)
            errFiles = errFiles.append(file)
    return(errFiles)

######################################
def do (dfs, f, **args):
    if isinstance(dfs, pd.DataFrame):
        try:
            f(dfs, **args)
        except Exception:
            pass
    elif isinstance(dfs, dict):
        for df in dfs.values():
            do(df, f, **args)

########################################
def update (old, new):
    key = ['stamp', 'item']
    tickers = set().union(old.keys(), new.keys())
    for tic in tickers:
        x = old[tic] = old.get(tic, {})
        y = new.get(tic, {})
        reports = set().union(x.keys(), y.keys())
        for rep in reports:
            z = pd.concat([x.get(rep), y.get(rep)])
            old[tic][rep] = z.groupby(by=key, as_index=False, sort=False).nth(-1)

####################################
def sec2stdItems (firms): ## return tag to item df (tag, item, occurances) and saves for each firm too
    for ticker, firm in firms.items():
        print(ticker)
        matches = []
        for report, freq in {"10-K":"A", "10-Q":"Q"}.items():
            try:
                print(report)
                sec = firm[report][['value', 'item']]
                print(freq)
                std = firm[freq][['value', 'item']]
                sec['value'] = np.where(sec['item'].str.contains(['EPS', 'DPS', 'per Share']), sec['value'], sec['value']/1000000)
                std['value'] = np.where(std['item'].str.contains(['EPS', 'DPS', 'per Share']), sec['value'], sec['value']/1000000)
                sec['value'] = sec['value'].round(1)
                std['value'] = std['value'].round(1)
                std.set_index('value', inplace=True)
                std.set_index('value', inplace=True)
                #sec = sec.assign(value=lambda x: x['value']//1000000)
                #sec = sec[sec['value']!=0].set_index(['value'], append=True) ## trim to millions a
                #std = std.assign(value=lambda x: x['value']//1).set_index(['value'], append=True) ## trim to millions
                match = sec.join(std, how='inner', lsuffix='_sec', rsuffix='_std').groupby(['item_sec', 'item_std'], sort=False).size()
                matches.append(match)
            except Exception:
                pass
        try:
            firms[ticker]['sec2stdItems'] = pd.concat(matches, axis=1).sum(axis=1)
        except Exception:
            pass

##################################
def sec2std (firms):
    sec2std = pd.Series()
    for ticker, firm in firms.items():
        print(ticker)
        try:
            sec2std = pd.concat([firm.get('sec2stdItems'), sec2std], axis=1).sum(axis=1)
        except Exception as e:
            print(e)
    return(sec2std)

#####################################
'''
SEC Financial Data Set contains end of querters. For Financial Reports of the current quarters use this function.
'''
def readSECxls ():
    a = pd.read_fwf("https://www.sec.gov/Archives/edgar/full-index/2017/QTR3/form.idx", header=None, skiprows=10, encoding="ISO-8859-1", index_col=0)
    current =a.loc[["10-K","10-Q","10-K/A","10-Q/A"],4]
    current = 'https://www.sec.gov/Archives/'+current.str.replace(pat='.txt', repl='/Financial_Report.xlsx').str.replace(pat='-',repl='')

    previous = pd.read_csv("C:\\Github\\Firms\\previousXLSX.csv", index_col=0)
    toRead = current[~current.isin.previous]
    ############### HERE
    ###############
    ############## extract data from xlsx
    current.to_csv("C:\\Github\\Firms\\previousXLSX.csv")

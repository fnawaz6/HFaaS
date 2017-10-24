## Change frame to report and make sure it does not conflict with sec
'''
Edgar statements:
https://www.sec.gov/dera/data/financial-statement-data-sets.html
sources
http://rankandfiled.com/#/data/tickers
Edgar Access Policy Page:
https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm

Edgar form-based (10-K, 10-K/A and 10-Q, 10-Q/A) index:
https://www.sec.gov/Archives/edgar/full-index/2017/QTR3/form.idx

Edgar XLXS for financial reports example (aapl):
https://www.sec.gov/Archives/edgar/data/320193/000032019317000009/Financial_Report.xlsx



with open('C:\\Github\\Firms\\firms.pkl', 'rb') as f:
    firms = pickle.load(f)


reproduce firms
update tag2item
'''
import os, pandas as pd, numpy as np, pickle, zipfile, shutil, copy
from datetime import datetime as dt
os.chdir("C:\\Github\\HFaaS\\")

update firms 10-k and 10-q from internet
sec2df(url, files)



class Firms(object):
    def __init__(self):
        secDates = []#string of dates like ['2008q1', '2008q2'] that this object contain the sec info 

        pass
    def fromSEC (url="https://www.sec.gov/files/dera/data/financial-statement-data-sets/", folders=None):
        if folders in ["all", None]:
            folders = pd.date_range(start='2009q1', end=dt.now(), freq='Q').to_period().map(str)
        if folders==None:
            folders = folders.isin(self.secDates)
        folders = url + folders
        import urllib
        testfile = urllib.URLopener()
        testfile.retrieve("http://randomsite.com/file.gz", "file.gz")
        import zipfile
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
        import shutil
        shutil.rmtree('/folder_name')










csv = pd.read_csv ("C:\\Github\\Firms\\financials.csv", index_col=0)
csv2firms = {}


with open('C:\\Github\\Firms\\firms.pkl', 'wb') as output:
    pickle.dump(firms, output, -1)

with open('C:\\Github\\Firms\\sec2firms.pkl', 'rb') as f:
    firms = pickle.load(f)

with open('C:\\Github\\Firms\\csv2firms.pkl', 'wb') as output:
    pickle.dump(csv2firms, output, -1)

with open('C:\\Github\\Firms\\csv2firms.pkl', 'rb') as f:
    csv2firms = pickle.load(f)

with open('C:\\Github\\Firms\\firms.pkl', 'rb') as f:
    firms = pickle.load(f)


################ get cik
import re
from cPickle import dump
from requests import get

DEFAULT_TICKERS = ['goog', 'aapl']
URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
CIK_RE = re.compile(r'.*CIK=(\d{10}).*')

cik_dict = {}
for ticker in DEFAULT_TICKERS:
    results = CIK_RE.findall(get(URL.format(ticker)).content)
    if len(results):
        cik_dict[str(ticker).lower()] = str(results[0])
f = open('cik_dict', 'w')
dump(cik_dict, f)
f.close()
###############


t0=dt.now()
errs = updateSECs(firms, old=True)
print(dt.now()-t0)
print(errs)


import copy
tree = copy.deepcopy({k:v for (k,v) in firms.items() if k in ['F', 'AAPL', 'IBM', 'MSFT']})
########## std to item: replace with items defined
items = pd.read_table ("std2items.tsv").dropna(subset=['line'])[['std_item','item']].set_index('std_item')
for firm in firms.values():
    for report in ['Q', 'A']:
        try:
            firm[report] = firm[report].join(items, on='item', lsuffix='_std', how='inner').drop('item_std', axis=1)
        except Exception:
            pass

###################

csv2firms = {}
df2firms (csv, csv2firms)
del(csv)
with open('C:\\Github\\Firms\\csv2firms.pkl', 'wb') as output:
    pickle.dump(csv2firms, output, -1)

with open('C:\\Github\\Firms\\sec2firms.pkl', 'rb') as f:
    firms = pickle.load(f)

update(firms, csv2firms)
del(csv2firms)

sec2stdItems(firms)

with open('C:\\Github\\Firms\\firms2.pkl', 'wb') as output:
    pickle.dump(firms, output, -1)

sec2std = sec2std(firms)

with open('C:\\Github\\Firms\\sec2item.pkl', 'wb') as f:
    pickle.dump(sec2item, f, -1)

with open('C:\\Github\\Firms\\sec2item.pkl', 'wb') as f:
    pickle.dump(sec2item, f, -1)

sec2item = sec2item[sec2item>400].sort_values()

errs =[]
for ticker, firm in firms.items():
    print(ticker)
    try:
        firm['sec2item'] = firm['sec2stdItems']+sec2item//100
    except Exception as e:
        print(e)
        errs.append(ticker)


########### map
report = '10-Q'
stamp = '2017Q2'

def f (index, report):

for ticker, firm in firms.items():
    print(ticker)
    for report, df in firm.items():
        if report in ['10-K', 'Y', 'A', 'Annual', 'Yearly']:
            df.set_index(df.index.to_timestamp('A'), inplace=True)
        elif report in ['Q', '10-Q', 'Quarterly']:
            df.set_index(df.index.to_timestamp('Q'), inplace=True)
        elif report in ['D']:
            df.set_index(df.index.to_timestamp('D'), inplace=True)

for ticker, firm in firms.items():
    items = firm['sec2stdItems'].rename('size').reset_index('item_std')
    df = firm['10-Q'][['item', 'value', 'uom']]
    df = df.join(items, on='item', how='inner').sort_values(by='size', ascending=False).drop(['item', 'size'], axis=1).rename(columns={'item_std':'item'})
    df2=df.groupby(['stamp', 'item']).head(1)



####### Module Firms.py 
'''
class Firms has methods to read/write data from/to sources, holds data related to current state of all firms,
and holds {ticker:firm} dictionary of data.
''' 
import Pandas as pd, numpy as np, datetime.datetime as dt, typing


######### Interfaces
'''
Reports stores financial data of a firm as a dictionary of dataframe reports such as Repprts['10-Q'] which is 10-Q report in DataFrame format.
Other Reports keys can be 10-K, A (for Annual homogenized DataFrame), Q (Quarterly Homogenized DataFrame), D (Daily DatFrame).
'''
Report = typing.Text
Reports = typing.Dict[Report, pd.DataFrame]

'''
Financials is a dictionry {Ticker ==> Report} to store Reports for all firms.
'''
Ticker = typing.Text
Financials = typing.Dict[Ticker, Reports]

'''
class Firm implements methods and properties to work with a firm's financial Reports.
'''
class Firm(Report): 
    def setIndex (reports: typing.List(str)=[]): -> Firm:
        pass
    def homogenize (fromTo typing.Dict[str, str]={'10-K':'A', '10-Q':Q}): -> Rpt:
        pass
    def tag2itemize ():
        pass
    def push2(oldFirm):
        pass
    def recap (from='D', to='Q'):
        pass

class Firms(Financials):
    def __init__ (self, workingDir = os.getcwdir()):
        tempFolder = workingDir+"\\temp\\"
        secArchiveFolder = workingDir+"\\secArchiveFolder\\"
    tag2items = None # {ticker:Series}
    tag2item = None # {Series}
    def setFolders (wdir=None): # {name:path}
        pass
    def readSecs (self, url, files=None):
        pass

################ Implementation
'''
Download and unzip SEC Edgar financial files and separate them as 10-Q or 10-A reports. 
Dispatch them by Ticker. Set their index.
''' 
def readSECs (firms Firms, url="https://www.sec.gov/files/dera/data/financial-statement-data-sets/", zipfiles typing.List[str]=[]):
    import zipfile, shutil, urllib, os
    # if zipfiles not given, select all files but exclude the archive files in secArchiveFolder
    if zipfiles==[]:
        zipfiles = pd.date_range(start='2009q1', end=dt.now(), freq='Q').to_period().map(str) # all files since 2009
        _,_,secArchives = os.walk(firms.secArchiveFolder) # archived files
        zipfiles = [f for f in zipfiles if f not in secArchives] # exclude archived files
        zipfiles.sort(reverse=True) # sort files from the latest to oldest
    # download and unzip and read in each zipfile
    for f in zipfiles:
        path = urllib.request.urlretrieve(url+f, firms.tempFolder+f) # download file
        with zipfile.ZipFile(path) as z: # unzip
            z.extractall(firms.tempFolder+"zip\\") 
        # read
#################### HEREEEEEEEEEEEEEEEEEEEE
        for ticker, dfs in Firms.sec2df(self.folders['temp']+"zip\\").groupby('ticker'):
            firm = Firm({report:df.drop(['ticker', 'report'], axis=1) for report, df in dfs})
            firm.homogenize({'10-K':'A', '10-Q':'Q'})
            firm.tag2i
            firm
            firm.
        {ticker:Firm(firm) for ticker, firm in dfs.groupby('ticker')}


        shutil.rmtree('/folder_name')













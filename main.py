import os, pandas as pd, numpy as np, pickle, zipfile, shutil, sys
os.chdir("C:\\Github\\HFaaS\\DevCodes\\sample data\\")
sys.path.append("C:\\Github\\HFaaS\\GitHub\\")
import sec2df


cik2ticker = pd.read_csv ("C:\\Github\\HFaaS\\Data\\cik2ticker.csv")[['cik', 'ticker']]
sec = updateSECs()

a = read_sec ("C:\\Github\\HFaaS\\temp\\temp\\", cik2ticker)

a = pd.read_csv("C:\\Github\\HFaaS\\Output\\sec2009_2017q3.csv", encoding='latin', nrows=10)

b = download_Financials_From_Google("MSFT", "NASDAQ")

c = pd.read_csv("C:\\Github\\HFaaS\\Output\\std2items.tsv", sep="\t", nrows=10)

######################### END of main program









from pyquery import PyQuery as pq
import pandas as pd
trans = { # to convert variables
    "inc":"IS",
    "bal":"BS",
    "cas":"CF",
    "annual":"A",
    "interim":"Q"
}
def download_Financials_From_Google(ticker, market=""): #-> pd.DataFrame
    #download page, read financial html table to a dataframe
    #,stack, rename and clean, and append together '''
    dfs = pd.DataFrame() #to gather all tables
    page = pq(url='https://finance.google.com/finance?q={}:{}&fstype=i'.format(market, ticker))
    #testPage = pq(filename="C:\\Github\\HFaaS\\temp\\appl.html")
    for stmt in ["inc", "bal", "cas"]:
        for term in ["annual", "interim"]:
            try:
                tbl = page('div#'+stmt+term+'div').html() # like "incannualdiv"
                df = (
                    pd.read_html(tbl, na_values="-", index_col=0)[0] # convert html table to DataFrame
                    .stack(dropna=True)
                    .reset_index()
                )
                df.columns = ["item", "date", "value"]
                dfs = (df
                    .assign(ticker = ticker, report = trans[term], stmt = trans[stmt], market = market)
                    .append(dfs)
                )
            except Exception as e:
                print(ticker, stmt, term, e)
    return(dfs)


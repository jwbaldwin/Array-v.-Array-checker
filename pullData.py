import urllib2
import pytz
import pandas as pd
import numpy as np
import pandas_datareader.data as web

from bs4 import BeautifulSoup
from datetime import datetime
#from pandas.io.data import DataReader


SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()

def scrape_list(site):
    hdr = {'User-Agent': 'Chrome/41.0.2228.0'}
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = list()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            ticker = str(col[0].string.strip())
            tickers.append(ticker)
   # print tickers
    return tickers

def download_ohlc(ticker, start, end):
    print 'Downloading data from Yahoo for %s' % ticker
    data = web.DataReader(ticker, 'yahoo', start, end)
    data.to_csv('data/'+ticker+'.csv')

    print data.head()
    #sector_ohlc[sector] = data
    print 'Finished downloading data for %s' %ticker
   # return sector_ohlc

def get_snp500():
    tickers = scrape_list(SITE)
    for ticker in tickers:
        stock_ohlc = download_ohlc(ticker, START, END)
    #save to csv

if __name__ == '__main__':
    get_snp500()
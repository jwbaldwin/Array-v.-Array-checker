import urllib2
import time
import datetime
import csv

from bs4 import BeautifulSoup

SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

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

    #print tickers
    return tickers

def writeHeaders(stock):
    headers = ['Timestamp', 'Close', 'High', 'Low', 'Open', 'Volume']
    stockFile = open(stock+'.csv', 'w')
    csvFile = csv.writer(stockFile)
    csvFile.writerow(headers)
    stockFile.close()

def pullData(stock):
    try:
        print 'Currently pulling',stock
        print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10d/csv'
        saveFileLine = stock+'.csv'

        try:
            readExistingData = open(saveFileLine, 'r').read()
            splitExisting = readExistingData.split('\n')
            mostRecentLine = splitExisting[-2] #the last line is actually a blank line
            if mostRecentLine.split(',')[0] == 'Timestamp':
                lastUnix = 0
            else:
                lastUnix = mostRecentLine.split(',')[0]
        except:
            lastUnix = 0

        saveFile = open(saveFileLine, 'a')
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')

        for eachLine in splitSource:
            if 'values' not in eachLine:
                splitLine = eachLine.split(',')
                if len(splitLine) ==6:
                    if int(splitLine[0]) > int(lastUnix):
                        lineToWrite = eachLine+'\n'
                        saveFile.write(lineToWrite)

        saveFile.close()

        print 'Pulled',stock
        print 'Sleeping...'
        print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(10)

    except Exception,e:
        print 'main loop ', str (e)

if __name__ == '__main__':
    stocksToPull = scrape_list(SITE)
    for stock in stocksToPull:
        writeHeaders(stock)
    while True:
        for eachStock in stocksToPull:
            pullData(eachStock)
    
    time.sleep(18000)
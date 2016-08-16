# James Baldwin 7/28/2016
# Program to compare stock movement to index marker and determine CBD
# Let user pick initial and index stock
import numpy as np
import pandas as pd
import csv
from pullData import scrape_list

SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def ticker_exists(ticker):
    tickers = scrape_list(SITE)
    tickers.append('SPINDEX')
    if ticker in tickers:
        return True
    else:
        return False

#grab each csv using the ticker +.csv
def grab_stocks_to_compare(stock_main, stock_index, beta_time):
    print "Gathering data for %s to compare against %s" % (stock_main, stock_index)
    #Here I need to get each adj close of the stocks and slice it so the
    #   days represented are equal in both cases
    
    #ERROR: Soemthign wrong when comparing two different stocks (maybe index?)
    main_df = pd.read_csv('data/'+stock_main+'.csv')
    index_df = pd.read_csv('data/'+stock_index+'.csv')

    #Get both stocks: Columns and amount by time
    #a_adj_close = main_df['Adj Close']
    #a = a_adj_close.tail(beta_time)

    #b_adj_close = index_df['Adj Close']
    #b = b_adj_close.tail(beta_time)


    #covariance = np.cov(a,b)[0][1]
    #variance = np.var(b)

    #beta = covariance / variance
    covmat = np.cov(main_df["Adj Close"].tail(beta_time), index_df["Adj Close"].tail(beta_time))
    beta = covmat[0,1]/covmat[1,1]

    print "The beta for your stock is: " + str(beta)
    print "Using the amount of days: " + str(beta_time)
#get the stocks from the user
def get_stocks():
    prompt= '> '

    print "Please pick a ticker from the S&P 500 -------"
    while True:
        try:
            print "Input the ticker for the stock to compare to an index: "
            stock_main = raw_input(prompt)
            if not ticker_exists(stock_main):
                print "Sorry, that ticker doesn't exist"
                break
            else:
                try:
                    print "Input the ticker for the index: "
                    stock_index = raw_input(prompt)
                    if not ticker_exists(stock_index):
                        print "Sorry, that ticker doesn't exist"
                        break
                    else:
                        print "Enter the amount of days: "
                        beta_time = int(raw_input(prompt))
                        grab_stocks_to_compare(stock_main, stock_index, beta_time)
                        break
                except Exception, e:
                    print e
                    break
        except Exception, e:
            print e
            print 'oops'


get_stocks() 

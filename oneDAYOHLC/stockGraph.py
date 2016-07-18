import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import matplotlib
matplotlib.rcParams.update({'font.size': 9})


eachStock = 'EBAY', 'TSLA', 'AAPL'


def movingaverage(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas



def graphData(stock, MA1, MA2):
    try:
        stockFile = stock+'.txt'

        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',',unpack=True,
                converters={ 0: mdates.strpdate2num('%Y%m%d')})

        ###
        x = 0
        y = len(date)
        candleAr =[]
        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
            candleAr.append(appendLine)
            x+=1

        ###Moving Averages
        Av1 = movingaverage(closep, MA1)
        Av2 = movingaverage(closep, MA2)

        SP = len(date[MA2-1:]) #Starting point

        label1=str(MA1)+' SMA'
        label2=str(MA2)+' SMA'



        ## Plots
        fig = plt.figure(facecolor='#1a1a1a')
        ax1 = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4, axisbg='#1a1a1a')
        candlestick(ax1, candleAr, width=.75, colorup='#9eff15', colordown='#ff1717')

        ax1.plot(date[-SP:], Av1[-SP:], '#5998ff', label = label1, linewidth=1.25)
        ax1.plot(date[-SP:], Av2[-SP:], '#ffab57', label = label2, linewidth=1.25)


        plt.ylabel('Stock Price')
        plt.legend(loc=3, prop={'size':7}, fancybox=True)
        ax1.grid(True, color='#f7f7f7')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#e6e6e6")
        ax1.spines['top'].set_color("#e6e6e6")
        ax1.spines['left'].set_color("#e6e6e6")
        ax1.spines['right'].set_color("#e6e6e6")
        ax1.tick_params(axis='y', colors="w")

        volumeMin = 0

        ax2 = plt.subplot2grid((5,4), (4,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#1a1a1a')
        ax2.plot(date, volume, '#00ffe8', linewidth=.8)
        ax2.fill_between(date, volumeMin, volume, facecolor='#00ffe8', alpha =.5)
        ax2.axes.yaxis.set_ticklabels([])
        plt.ylabel('Volume', color="w")
        ax2.grid(False)
        ax2.spines['bottom'].set_color("#e6e6e6")
        ax2.spines['top'].set_color("#e6e6e6")
        ax2.spines['left'].set_color("#e6e6e6")
        ax2.spines['right'].set_color("#e6e6e6")
        ax2.tick_params(axis='x', colors="w")
        ax2.tick_params(axis='y', colors="w")

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        # Configure the chart
        plt.subplots_adjust(left=.10, bottom=.14, right=.93, top=.93, wspace=.20, hspace=.00)

        plt.suptitle(stock+' Stock Price', color="w")

        # Remove the ax1 date
        plt.setp(ax1.get_xticklabels(), visible = False)

        plt.show()
        fig.savefig(stock+'.png', facecolor=fig.get_facecolor())


    except Exception, e:
        print 'failed main loop', str(e)


for stock in eachStock:
    graphData(stock, 12, 26)
    time.sleep(555)

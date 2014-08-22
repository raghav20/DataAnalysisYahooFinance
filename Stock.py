import pandas as pd
import pandas.io.data
from datetime import timedelta
import datetime as dt
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import urllib.request
import numpy as numpy
from datetime import datetime
from matplotlib.pyplot import *
import matplotlib.dates as mdates

import datetime
import time

class Stock():
  def __init__(self,symbol,lookback_period,window_size,end=datetime.date.today()):
    self.symbol = symbol.upper()
    #get 100 days of prices or lookback period prices
    start = end - timedelta(days=lookback_period)
    #convert the time into req format
    start_date = start.isoformat()
    end_date = end.isoformat()
    start_year,start_month,start_day = start_date.split('-')
    start_month = str(int(start_month)-1)
    end_year,end_month,end_day = end_date.split('-')
    end_month = str(int(end_month)-1)
    #get data from yahoo finance
    url = "http://ichart.finance.yahoo.com/table.csv?s={0}".format(symbol)
    url += "&a={0}&b={1}&c={2}".format(start_month,start_day,start_year)
    url += "&d={0}&e={1}&f={2}".format(end_month,end_day,end_year)
    #parse data
    df = pd.read_csv(urllib.request.urlopen(url))
    #get the adj close from csv
    saved_column = df['Adj Close']
    #get the matching date
    y_data = df['Date']
    #convert list to array
    close = numpy.asarray(saved_column)
    #generate x-date which is date
    x_points = numpy.asarray(y_data)

    x_data = x_points[0:70]
    #get the moving average
    y_av = self.movingaverage(saved_column,window_size)
    #generate graph
    figure("Plot of stocks")
    x = [dt.datetime.strptime(d,"%Y-%m-%d").date() for d in x_data]
    gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    gca().xaxis.set_major_locator(mdates.DayLocator())
    plot(x,y_av,'r')
    plot(x,close,'g')
    gcf().autofmt_xdate()
    xlabel("Date")
    ylabel("adjusted close")
    show()

  def movingaverage(self,interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')


#The way to call the function
#note since in last 100 days some days are not there in csv from yahoo so the number of items in the graph are not 91 but less then that
#customisable function any company symbol,startdate and window size can be specified
Stock('MSFT',100,10)

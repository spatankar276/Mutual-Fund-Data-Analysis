import pandas as pd
import numpy as np
import requests
import json
import re
import seaborn as sns
import time
from scipy.stats import norm
from matplotlib import pyplot as plt
import random
import datetime


def managed(expense_ratio):
    if expense_ratio < 0.007:
        return 'passive'
    else:
        return 'active'
    
    

def managed_turn(turnover_ratio):
    if turnover_ratio > .2:
        return 'active'
    else:
        return 'passive'
       

def get_yahoo_prices(ticker, stdt, enddt):
    ''' Download price history for a single ticker symbol from Yahoo! Finance
    
    Arguments
    ---------
        ticker : must be a stock ticker (FX not supported)
        stdt   : start date for series, as a datetime object
        enddt  : end date for series, as a datetime object
        
    Returns
    -------
        pandas DataFrame
    '''
    
    stdt = int(time.mktime(stdt.timetuple()))
    enddt = int(time.mktime(enddt.timetuple()))
    
    url = 'https://finance.yahoo.com/quote/{}/history?'.format(ticker)
    params = {'interval':'1d', 
              'filter':'history', 
              'frequency':'1d', 
              'period1':stdt, 
              'period2':enddt}

    r = requests.get(url, params=params)

    # Grab the JSON and create a pandas dataframe
    try:
        txt = re.search(r'root\.App\.main = (.*?);\n}\(this\)\);', r.text, re.DOTALL).group(1)
        jsn = json.loads(txt)
        prcs = pd.DataFrame(jsn['context']['dispatcher']['stores']['HistoricalPriceStore']['prices'])
        prcs['date'] = pd.to_datetime(prcs['date'], unit='s')
        prcs['date'] = pd.DatetimeIndex(prcs['date']).normalize()
    
        prcs = prcs.set_index('date')
        prcs = prcs[['open', 'high', 'low', 'close', 'adjclose', 'volume']]
        prcs = prcs.dropna(how='all').sort_index()
    except:
        prcs = pd.DataFrame(columns=['open', 'high', 'low', 'close', 
                                     'adjclose', 'volume'])
    
    return prcs



def merged(dfa, price_dictionary):
    for k in price_dictionary:
        temp = price_dictionary.get(k)
        to_merge = pd.DataFrame({'date' : temp['date'], k : temp['close']})
        dfa = dfa.merge(to_merge, on = 'date', how = 'outer')
    
    return dfa
        








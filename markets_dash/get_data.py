import pandas as pd
import numpy as np
import pandas_datareader as pdr

####################################
# GET FUNCTIONS
####################################

# GETTING S&P 500 constituents from Wikipedia - Save to csv
def get_rates():
    '''
   Import Monthly US rates since 1982 from FRED St Louis
    '''
    start = '2000-01-01'
    tickers = ['GS30','GS10','GS5','GS3','GS2','GS1','GS6m','GS3m']
    df = pdr.get_data_fred(tickers,start)
    df.columns=['30Y','10Y','5Y','3Y','2Y','1Y','6M','3M']
    df.dropna(inplace=True)
    return df

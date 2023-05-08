import pandas as pd
import numpy as np
import pandas_datareader as pdr
import yfinance as yf

####################################
############## RATES ###############
####################################

def get_rates():
    '''
   Import Monthly US rates since 1982 from FRED St Louis
    '''
    start = '2000-01-01'
    tickers = ['GS30','GS10','GS5','GS3','GS2','GS1','GS6m','GS3m']
    df = pdr.get_data_fred(tickers,start)
    df.columns=['30Y','10Y','5Y','3Y','2Y','1Y','6M','3M']
    df.dropna(inplace=True)
    # Changing format from 1st day of the month to last day of the month
    df.index = df.index + pd.offsets.MonthEnd(0)
    print(df)
    return df



####################################
########### EQUITIES ###############
####################################

####################################
# GET FUNCTIONS
####################################

# GETTING S&P 500 constituents from Wikipedia - Save to csv
def get_spx_cons(csv_path):
    '''
    Extract S&P 500 companies from wikipedia and store tickers and Sectors / Industries as df
    Then store as csv.
    '''
    URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df = pd.read_html(URL)[0]
    df['Symbol'] = df['Symbol'].str.replace('.','-')
    df = df.drop(['Headquarters Location','Date added','CIK','Founded'],axis=1)
    df = df.sort_values(by=['GICS Sector','GICS Sub-Industry'])
    df = df.set_index('Symbol')
    df.dropna(inplace=True)
    return df.to_csv(csv_path)

# GETTING S&P prices from yfinance - Save to csv
def get_prices(df):
    '''
    Dowload prices from yfinance from a list of tickers. returns df of prices written to a csv
    '''
    # local_path linked to drive via sinology
    local_path = '/Users/chloeguillaume/SynologyDrive/Google Drive/DATA_PUBLIC/us_markets_dash_data/spx.csv'
    # url public on google drive
    file_id = '1SoheVoh79lEo5HhVxR_p_XdLewRAgWdh'
    url_open = f'https://drive.google.com/uc?id={file_id}&export=download'
    url_save = f'https://drive.google.com/u/0/uc?id={file_id}&export=download'

    #file = pd.read_csv(local_path)

    tickers_list = df.index.tolist()
    start= '2020-12-31'
    prices_df = yf.download(tickers_list, start=start,interval='1d',)
    file = prices_df['Adj Close']

    return file.to_csv(local_path)


####################################
# LOAD FUNCTIONS
####################################

# load S&P 500 weights from IVV ETF stored in csv
def load_IVV_weight():
    '''
    Load weights from IVV Holdings csv => df_IVV
    link to IVV page:

    '''
    local_path = 'pages/IVV_holdings.csv'

    df_IVV = pd.read_csv(local_path,skiprows=8,header=1)
    df_IVV = df_IVV[df_IVV['Asset Class']=='Equity']
    df_IVV = df_IVV[['Ticker','Name','Sector','Asset Class','Weight (%)']]
    df_IVV = df_IVV.set_index('Ticker')
    df_IVV.index = df_IVV.index.str.replace('BRKB','BRK-B')
    df_IVV.index = df_IVV.index.str.replace('BFB','BF-B')
    df_IVV['Weight (%)'] = df_IVV['Weight (%)']/100
    return df_IVV

# load S&P 500 weights from IVV ETF stored in csv
def load_wiki_cons(csv_path):
    '''
    Load tickers, sectors, industries etc. from wiki csv file
    => df
    '''
    df = pd.read_csv(csv_path)
    df = df.set_index('Symbol')
    return df

####################################
# COMPUTE FUNCTIONS
####################################

# Computing Daily returns
def get_returns():
    '''
    Load prices from csv and compute daily stock returns.
    output returns_df
    '''
    # google_drive url
    file_id = '1SoheVoh79lEo5HhVxR_p_XdLewRAgWdh'
    url = f'https://drive.google.com/uc?id={file_id}&export=download'
    #local file path
    local_path = 'pages/spx.csv'

    prices_csv = pd.read_csv(url).set_index('Date')
    prices_csv.index = pd.to_datetime(prices_csv.index)
    # fwd fill last prices to missing daily prices (non-trading)
    daily_prices_csv = prices_csv.asfreq('D').ffill()
    returns_df = np.log(daily_prices_csv / daily_prices_csv.shift(1))
    ## EDIT
    last_date = returns_df.index[-1]
    print(last_date)

    #last_month_end = pd.date_range(last_date, periods=1, freq='M').strftime('%Y-%m-%d')[0]
    last_month_end = last_date - pd.offsets.MonthEnd(1)
    print(last_month_end)
    returns_df = returns_df[returns_df.index <= last_month_end]
    print(returns_df.index[-1])
    return returns_df


# Computing stock 1M, 3M, and YTD performance
def get_stock_perf(returns_df,df):
    '''
    Compute per periods from daily returns
    '''
    df_ret_summ = pd.DataFrame(np.exp((returns_df[-30:]).sum())-1,columns=['1M'])
    df_ret_summ['3M'] = np.exp(returns_df[-90:].sum())-1
    df_ret_summ['2022'] = np.exp(returns_df['2022'].sum())-1
    df_ret_summ['YTD'] = np.exp(returns_df['2023'].sum())-1
    df_ret_summ.index.rename('Symbol',inplace=True)
    stock_df = df.join(df_ret_summ)
    return stock_df


# Computing sector ind returns
def get_sector_perf(returns_df,df,period='2022'):
    '''
    from df of daily returns for each stocks compute sector cum performance vs EW
    '''
    # Compute Sector / Industry daily returns - mean of stocks by sectors
    returns = returns_df.T
    returns.index.rename('Symbol',inplace=True)
    returns = df.join(returns)
    returns = returns.drop(columns='Weight')
    sector_returns = returns.groupby('Sector').mean().T
    sector_returns.index = pd.to_datetime(sector_returns.index)

    ind_returns = returns.groupby('Sub-Industry').mean().T
    ind_returns.index = pd.to_datetime(ind_returns.index)

    # Compute cumul sector return for line chart
    sector_cum_perf = (np.exp((sector_returns['2023']).cumsum()))*100
    sector_cum_perf.loc[pd.to_datetime('2022-12-31')]= 100
    sector_cum_perf = sector_cum_perf.sort_index()
    sector_cum_perf


    sector_df = pd.DataFrame(np.exp((sector_returns['2023']).sum())-1,columns=['YTD'])
    sector_df['3M'] = np.exp(sector_returns[-90:].sum())-1
    sector_df['2022'] = np.exp(sector_returns['2022'].sum())-1

    ind_df = pd.DataFrame(np.exp((ind_returns['2023':]).sum())-1,columns=['YTD'])
    ind_df['3M'] = np.exp(ind_returns[-90:].sum())-1
    ind_df['2022'] = np.exp(ind_returns['2022'].sum())-1


    return sector_df, ind_df, sector_cum_perf

####################################
# FEATURE ENGINEERING
####################################
def join_dfs(df,df_IVV):
    df = df.join(df_IVV['Weight (%)'])
    df.sort_values(by='Weight (%)',inplace=True,ascending=False)
    df = df.rename(columns={'GICS Sector':'Sector','GICS Sub-Industry':'Sub-Industry','Weight (%)':'Weight'})
    df.dropna(inplace=True)
    return df

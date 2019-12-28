import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
from tiingo import TiingoClient
import os
import scipy.stats as stats
from pandas.plotting import register_matplotlib_converters
from dateutil.relativedelta import relativedelta
import pantulipy as ti
import io
import math

class Indicators():
    """
    Signal library to provide graphical analysis of various market symbols
    
    Parameters
    ----------
    symbol : str
        str representing stock symbol
        
    Attributes
    ----------
    data : pd.DataFrame:
        DataFrame of historical data of this given symbol using TIINGO
    returns_mean : total mean of the returns for historical data
    returns_std : total standard deviation of the returns for historical data
    normal_returns : lambda function representing PDF(x) where x represents some decimal based daily return
    symbol : str
        str representing stock symbol
    """
    def __init__(self, symbol):
        # Matplotlib Setup
        register_matplotlib_converters()
        
        # TIINGO Setup
        config = {}
        config['api_key'] = os.getenv('TINGO_SECRET')
        client = TiingoClient(config)
        self.symbol = symbol
        resp = client.get_ticker_price(
            self.symbol, 
            fmt='csv', 
            startDate=datetime.datetime.today() - relativedelta(years=5),
            endDate=datetime.datetime.today()
        )
        self.data = pd.read_csv(io.StringIO(resp))
        f = lambda col: datetime.datetime.strptime(col, '%Y-%m-%d')
        self.data['date'] = self.data['date'].apply(f)
        self.data.index = self.data['date']
        
        # Calculate Averages and Returns
        self.data['avg'] = (self.data['close'] + self.data['low'] + self.data['high']) / 3
        self.data['returns'] = (self.data['open'] - self.data['close']) / self.data['open']
        self.lognorm = lambda x: scipy.stats.lognorm(x, loc=self.data['avg'].mean(), scale=self.data['avg'].std())
        
        # Indicators
        self.cci = ti.cci(self.data, 20)
        self.rsi = ti.rsi(self.data, 14)
        self.short_stick = ti.ema(self.data, 12)
        self.long_stick = ti.ema(self.data, 26)
        self.macd, self.macd_signal, self.macd_histogram = ti.macd(self.data, 12, 26, 9)

def plot_indicator(indicator, start_timeframe):
    plt.rcParams['figure.figsize'] = [20, 20]
    show = indicator.data.loc[start_timeframe:datetime.datetime.today()]

    cci = indicator.cci.loc[start_timeframe:datetime.datetime.today()]
    rsi = indicator.rsi.loc[start_timeframe:datetime.datetime.today()]
    short_stick = indicator.short_stick.loc[start_timeframe:datetime.datetime.today()]
    long_stick = indicator.long_stick.loc[start_timeframe:datetime.datetime.today()]
    macd = indicator.macd.loc[start_timeframe:datetime.datetime.today()]
    macd_signal = indicator.macd_signal.loc[start_timeframe:datetime.datetime.today()]
    macd_histogram = indicator.macd_histogram.loc[start_timeframe:datetime.datetime.today()]

    # MACD
    plt.subplot(511)
    plt.title("{0}: {1} vs {2} EMA's".format(indicator.symbol, 12, 26))
    plt.plot(show.loc[long_stick.index]['close'])
    plt.plot(short_stick.loc[long_stick.index], label='12 EMA')
    plt.plot(long_stick, label='26 EMA')
    plt.legend()

    plt.subplot(512)
    plt.title('MACD vs signal line')
    plt.plot(macd, label="macd")
    plt.plot(macd_signal, label="signal line")
    plt.legend()

    plt.subplot(513)
    plt.title('MACD histogram')
    plt.hist(macd_histogram, bins=200)

    # CCI
    plt.subplot(514)
    plt.title('Commodity Channel Index (CCI)')
    plt.plot(cci, label='cci')

    oversold_index = pd.DataFrame({'oversold': [-100]*len(cci), 'index':cci.index}).set_index('index')
    overbought_index = pd.DataFrame({'overbought': [100]*len(cci), 'index':cci.index}).set_index('index')
    plt.plot(overbought_index, linestyle=':', color='blue')
    plt.plot(oversold_index, linestyle=':', color='red')
    plt.legend()

    # # RSI
    oversold_index = pd.DataFrame({'oversold': [30]*len(cci), 'index':cci.index}).set_index('index')
    overbought_index = pd.DataFrame({'overbought': [70]*len(cci), 'index':cci.index}).set_index('index')
    plt.subplot(515)
    plt.title('Relative Strength Index (RSI)')
    plt.plot(rsi, label='rsi')
    plt.plot(overbought_index, linestyle=':', color='blue')
    plt.plot(oversold_index, linestyle=':', color='red')
    plt.legend()

    plt.show()

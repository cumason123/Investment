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
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import copy
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
    def __init__(self, symbol, years=5, nmacd=(12, 26, 9), ncci=20, nrsi=14):
        register_matplotlib_converters()
        self.nmacd = nmacd
        self.ncci = ncci
        self.nrsi = nrsi
        # TIINGO Setup
        config = {}
        config['api_key'] = os.getenv('TINGO_SECRET')
        client = TiingoClient(config)
        self.symbol = symbol
        resp = client.get_ticker_price(
            self.symbol, 
            fmt='csv', 
            startDate=datetime.datetime.today() - relativedelta(years=years),
            endDate=datetime.datetime.today()
        )
        
        self.data = pd.read_csv(io.StringIO(resp))
        if 'date' not in self.data:
            raise ti.InvalidOptionError
        f = lambda col: datetime.datetime.strptime(col, '%Y-%m-%d')
        self.data['date'] = self.data['date'].apply(f)
        self.data.index = self.data['date']
        self.data['avg'] = (self.data['close'] + self.data['low'] + self.data['high']) / 3
        self.data['returns'] = (self.data['open'] - self.data['close']) / self.data['open']
        self.lognorm = lambda x: scipy.stats.lognorm(x, loc=self.data['avg'].mean(), scale=self.data['avg'].std())
        
        # Indicators
        macd, macd_signal, macd_histogram = ti.macd(self.data, *nmacd)
        self.indicators = {
            'cci': ti.cci(self.data, ncci),
            'rsi': ti.rsi(self.data, nrsi),
            'shortema': ti.ema(self.data, nmacd[0]),
            'longema': ti.ema(self.data, nmacd[1]),
            'macd': macd,
            'macd_signal': macd_signal,
            'macd_histogram': macd_histogram,
            'show': self.data
        }

def plot_indicator(indicator, start_timeframe):
    plt.rcParams['figure.figsize'] = [20, 20]
    show = copy.deepcopy(indicator.indicators)

    for key in show:
        show[key] = show[key].loc[start_timeframe:datetime.datetime.today()]

    # Graph 1 -- MACD
    fig, axes = plt.subplots(5, 1)
    ax1, ax2, ax3, ax4, ax5 = axes
    for i, ax in enumerate(axes):
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

    ax1.set_title("{0}: {1} vs {2} EMA's".format(indicator.symbol, *indicator.nmacd[:-1]))
    ohlc = show['show'].loc[show['longema'].index]

    ohlc['Date'] = pd.to_datetime(ohlc.index)
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)

    ohlc = ohlc[['Date', 'open', 'high', 'low', 'close']]
    candlestick_ohlc(ax1, ohlc.values, colorup='green', colordown='red')

    ax1.plot(show['shortema'].loc[show['longema'].index], label='{0} EMA'.format(indicator.nmacd[0]), color='blue')
    ax1.plot(show['longema'], label='{0} EMA'.format(indicator.nmacd[1]), color='orange')
    ax1.legend()

    # Graph 2 -- MACD
    ax2.set_title('MACD vs signal line')
    ax2.plot(show['macd'], label="macd", color='blue', lw=2)
    ax2.plot(show['macd_signal'], label="signal line", color='orange', lw=2)

    x = show['macd'].index
    y1 = show['macd'].values
    y2 = show['macd_signal'].values

    ax2.fill_between(x, y1, y2, where=y2 >= y1, facecolor='red', interpolate=True)
    ax2.fill_between(x, y1, y2, where=y2 < y1, facecolor='green', interpolate=True)
    ax2.legend()

    # Graph 3 -- MACD
    ax3.set_title('MACD - signal line')
    ax3.plot(show['macd_histogram'], color='blue')
    y = show['macd_histogram'].values
    x = show['macd_histogram'].index
    ax3.fill_between(x, 0, y, where=y >= 0, facecolor='green', interpolate=True)
    ax3.fill_between(x, 0, y, where=y < 0, facecolor='red', interpolate=True)
    ax3.axhline(y=0, linestyle=':', color='black')
    
    # Graph 4 -- CCI
    ax4.set_title('Commodity Channel Index ({0} day CCI)'.format(indicator.ncci))
    ax4.plot(show['cci'], label='cci')
    ax4.axhline(y=-100, linestyle=':', color='blue')
    ax4.axhline(y=0, linestyle=':', color='black')
    ax4.axhline(y=100, linestyle=':', color='red')
    ax4.legend()

    # Graph 5 -- RSI
    ax5.set_title('Relative Strength Index ({0} day RSI)'.format(indicator.nrsi))
    ax5.plot(show['rsi'], label='rsi')
    ax5.axhline(y=70, linestyle=':', color='blue')
    ax5.axhline(y=30, linestyle=':', color='red')
    ax5.legend()
    plt.subplots_adjust(hspace=0.5)
    plt.show()

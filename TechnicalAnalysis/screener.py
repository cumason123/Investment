from TechnicalIndicators import Indicators
import os
import pantulipy as ti
from multiprocessing.pool import ThreadPool

pool = ThreadPool()
COMPLEX_SYMBOLS = []
if os.path.exists('symbols.txt'):
	with open('symbols.txt') as file:
		COMPLEX_SYMBOLS = eval(file.read())
elif os.path.exists('TechnicalAnalysis/symbols.txt'):
	with open('TechnicalAnalysis/symbols.txt') as file:
		COMPLEX_SYMBOLS = eval(file.read())

__SIMPLE_SYMBOLS = [
	'PYPL', 'AAPL', 'BB', 'T', 'TSLA', 
	'SPY', 'FB', 'GE', 'BBY', 'INTC', 
	'ETHUSD', 'VZ', 'FIT', 'BTCUSD'
]


def symbols2indicators(symbols_arr, **kwargs):
	indicators = {}

	def f(symbol):
		try:
			return symbol, Indicators(symbol, **kwargs)
		except ti.InvalidOptionError as e:
			return symbol, None	
	symbols = pool.map(f, list(set(symbols_arr)))
	return dict(filter(lambda d: d[1] != None, symbols))


def find_stocks(ruleset, indicator_dict, **kwargs):
	"""
	Takes in a ruleset and filters indicator_dict according to that ruleset

	Parameters
	----------
	ruleset : function Indicators -> bool
		ruleset is a callback function which we use to filter indicator_dict
	indicator_dict : Dict{str : Indicators}
		indicator_dict is keyed by symbols and valued with Indicator objects

	returns : Dict{str : Indicators}"""
	# TODO make oneline with filter
	ret = {}
	def f(symbol):
		if indicator_dict[symbol] != None and ruleset(indicator_dict[symbol], **kwargs):
			return symbol, indicator_dict[symbol]
		else:
			return symbol, None
	stocks = pool.map(f, list(set(indicator_dict.keys())))
	return dict(filter(lambda d: d[1] != None, stocks))

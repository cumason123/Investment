from TechnicalIndicators import Indicators
import os
import pantulipy as ti


__COMPLEX_SYMBOLS = []
if os.path.exists('symbols.txt'):
	with open('symbols.txt') as file:
		__COMPLEX_SYMBOLS = eval(file.read())


__SIMPLE_SYMBOLS = [
	'PYPL', 'AAPL', 'BB', 'T', 'TSLA', 
	'SPY', 'FB', 'GE', 'BBY', 'INTC', 
	'ETHUSD', 'VZ', 'FIT', 'BTCUSD'
]


def symbols2indicators(symbols_arr):
	indicators = {}
	for symbol in symbols_arr:
		try:
			indicators[symbol] = Indicators(symbol)
		except ti.InvalidOptionError as e:
			print('Invalid Symbol {0}'.format(symbol))
	return indicators


def find_stocks(ruleset, indicator_dict):
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
	for symbol in indicator_dict:
		if ruleset(indicator_dict[symbol]):
			ret[symbol] = indicator_dict[symbol]
	return ret

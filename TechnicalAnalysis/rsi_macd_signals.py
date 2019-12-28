from generic_trading import GenericAlgo
class TrendTrading(GenericAlgo):
	"""
	Attributes
	----------
	delta : int
		days before today to use when checking the timeframe for if the indicator crossed
		some threshold. 

	Algorithm
	----------
	If MACD is positive (bullish) and RSI breaks the mark of 30 from the bottom to up, 
	we emit a buy signal.

	If MACD is negative (bearish) and RSI breaks the mark 70 from top to bottom,
	we emit a short signal.
	"""
	def __init__(self, delta=2):
		super().__init__(delta=delta)

	def buy_ruleset(self, ind):
		data = ind.indicators
		macd_bullish = data['macd_histogram'][-1] > 0
		rsi_left_oversold = data['rsi'][-1] > 30 and data['rsi'][-1 - self.delta] < 30
		return macd_bullish and rsi_left_oversold

	def short_ruleset(self, ind):
		data = ind.indicators
		macd_bearish = data['macd_histogram'][-1] < 0
		rsi_left_overbought = data['rsi'][-1] < 70 and data['rsi'][-1 - self.delta] > 70
		return macd_bearish and rsi_left_overbought

class BroadTrendTrading(GenericAlgo):
	"""
	Attributes
	----------
	delta : int
		days before today to use when checking the timeframe for if the indicator crossed
		some threshold. 

	Algorithm
	----------
	If MACD is positive (bullish) and RSI breaks the mark of 30 from the bottom to up, 
	we emit a buy signal.

	If MACD is negative (bearish) and RSI breaks the mark 70 from top to bottom,
	we emit a short signal.
	"""
	def __init__(self, delta=2):
		super().__init__(delta=delta)

	def buy_ruleset(self, ind):
		data = ind.indicators
		macd_bullish = data['macd_histogram'][-1] > 0
		rsi_left_oversold = data['rsi'][-1] > 30 and data['rsi'][-1 - self.delta] < 30
		rsi_crossed_overbought = data['rsi'][-1] > 70 and data['rsi'][-1 - self.delta] < 70
		return macd_bullish and (rsi_left_oversold or rsi_crossed_overbought)

	def short_ruleset(self, ind):
		data = ind.indicators
		macd_bearish = data['macd_histogram'][-1] < 0
		rsi_crossed_oversold = data['rsi'][-1] < 30 and data['rsi'][-1 - self.delta] > 30
		rsi_left_overbought = data['rsi'][-1] < 70 and data['rsi'][-1 - self.delta] > 70
		return macd_bearish and (rsi_left_overbought or rsi_crossed_oversold)

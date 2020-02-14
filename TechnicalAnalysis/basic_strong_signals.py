from generic_trading import GenericAlgo
class StrongTrendTrading(GenericAlgo):
	"""
	Attributes
	----------
	delta : int
		days before today to use when checking the timeframe for if the indicator crossed
		some threshold. 

	Algorithm
	----------
	If MACD and CCI are both bullish and RSI states stock was oversold anytime in last delta,
	(<30) then send buy signal

	If MACD and CCI are both bearish and RSI states stock is overbought anytime in last delta
	(>70) then send short signal
	"""
	def __init__(self, delta=2):
		super().__init__(delta=delta)

	def buy_ruleset(self, ind, use_penny_stocks):
		data = ind.indicators
		if not use_penny_stocks and ind.data['close'][-1] < 5:
			return False
		macd_bullish = data['macd_histogram'][-1] > 0
		cci_bullish = data['cci'][-1] > 0
		rsi_bullish = data['rsi'][-1] > 50
		price_action_value = self.price_action(ind.data)
		#rsi_buy_signal = True in (data['rsi'][-1 - self.delta:-1] < 30).tolist()
		return macd_bullish and cci_bullish and rsi_bullish and price_action_value > 0

	def short_ruleset(self, ind):
		data = ind.indicators
		macd_bearish = data['macd_histogram'][-1] < 0
		cci_bearish = data['cci'][-1] < 0
		rsi_bearish = data['rsi'][-1] < 50
		#rsi_short_signal = True in (data['rsi'][-1 - self.delta:-1] > 70).tolist()
		return macd_bearish and cci_bearish and rsi_bearish

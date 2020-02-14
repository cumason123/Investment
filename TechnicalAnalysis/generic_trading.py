import talib
CANDLE_STICK_FUNCS = [getattr(talib, s) for s in talib.get_function_groups()['Pattern Recognition']]
NUM_FUNCS = len(CANDLE_STICK_FUNCS)
class GenericAlgo():
	def __init__(self, delta):
		assert delta > -1
		self.delta = delta

	@staticmethod
	def price_action(data):
		price_action_vals = 0
		for func in CANDLE_STICK_FUNCS:
			PA = func(
				data['open'], 
				data['high'], 
				data['low'], 
				data['close']
			)[-1]
			price_action_vals += PA
		# normalize
		price_action_vals /= (NUM_FUNCS * 100) if NUM_FUNCS > 0 else 1
		return price_action_vals
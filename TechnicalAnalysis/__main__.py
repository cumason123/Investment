from screener import find_stocks, symbols2indicators, COMPLEX_SYMBOLS, __SIMPLE_SYMBOLS
from flask import Flask, jsonify, request, Response
from basic_strong_signals import StrongTrendTrading, SmallStocksTrendTrading
import simplejson as json
from flask import Flask
from threading import Thread
import time
import alpaca_trade_api as tradeapi
api = tradeapi.REST(api_version='v2') # or use ENV Vars shown below
account = api.get_account()

app = Flask(__name__)
cache = {
	'index': 1,
	'resp': [[], []]
}

@app.route('/bullstocks')
def GetBullishStocks():
	return Response(json.dumps(cache['resp'][cache['index']]), status=200, mimetype='application/json')

@app.route('/buyall')
def BuyAll():
	for symbol in cache['resp'][cache['index']]:
		try:
			api.submit_order(
				symbol=symbol,
				side='buy',
				type='market',
				qty='1',
				time_in_force='day')
		except tradeapi.rest.APIError:
			print('Throwing unknown symbol {0}'.format(symbol))
			continue
	return Response({'success': 200}, status=200, mimetype='application/json')

def swapstock():
	while True:
		now = time.time()
		symbols = symbols2indicators(COMPLEX_SYMBOLS, nmacd=(15, 30, 9), ncci=31, years=1)
		trading_strategy = SmallStocksTrendTrading(delta=6)
		bull_stocks = find_stocks(trading_strategy.buy_ruleset, symbols, use_penny_stocks=False, threshold=20)
		print('Grabbed Stock data in {0}s'.format(time.time() - now))

		resp = list(bull_stocks.keys())
		cache['index'] = 1 - cache['index']
		cache['resp'][cache['index']] = resp
		time.sleep(60 * 60 * 2) # every two hours

if __name__ == '__main__':
	cacheThread = Thread(target=swapstock)
	cacheThread.start()
	app.run('0.0.0.0', port=80)

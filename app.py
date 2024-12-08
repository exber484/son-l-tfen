import os
import numpy as np
import talib
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Crypto Analysis App!"

@app.route('/signal', methods=['GET'])
def get_signal():
    # Example: Let's fetch cryptocurrency data (using CoinGecko as an example)
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {'vs_currency': 'usd', 'days': '1'}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500
    
    data = response.json()
    prices = [item[1] for item in data['prices']]
    
    # Example: Let's use TA-Lib to calculate the RSI (Relative Strength Index)
    rsi = talib.RSI(np.array(prices), timeperiod=14)
    
    # Get the last RSI value
    signal = "BUY" if rsi[-1] < 30 else "SELL" if rsi[-1] > 70 else "HOLD"
    
    return jsonify({'rsi': rsi[-1], 'signal': signal})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

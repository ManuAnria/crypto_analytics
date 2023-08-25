import json
import websocket
import os
import requests
from dotenv import load_dotenv
import pandas as pd
from binance.spot import Spot
import openpyxl
from pprint import pprint

load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
client = Spot(api_key=api_key, api_secret=api_secret)

# Binance API base URL
BASE_URL = 'https://api.binance.com/api/v3'


# Get all symbols
def get_all():
    url = f'{BASE_URL}/exchangeInfo'
    symbols_response = requests.get(url)
    symbols_data = symbols_response.json()
    symbols = [symbol_['symbol'] for symbol_ in symbols_data['symbols']]
    return symbols


all_symbols = list(get_all())

# Parameters
symbol = [sym for sym in all_symbols if sym.endswith('USDT')]
interval = '1m'     # s-> seconds; m -> minutes; h -> hours; d -> days; w -> weeks; M -> months

# Create a WebSocket connection
url = 'wss://stream.binance.com:9443/stream?streams='
streams = '/'.join([f'{sym.lower()}@kline_{interval}' for sym in symbol])
URL = url + streams


# Create a function to handle the open
def on_open(ws):
    print('Opened connection')


# Create a function to handle the messages
info = {}
def on_message(ws, message):
    data = json.loads(message)
    candle = data['data']['k']
    tickr = candle['s']
    is_closed = candle['x']
    close = candle['c']
    open = candle['o']
    high = candle['h']
    low = candle['l']
    volume = candle['v']
    close_time = candle['T']
    interval = candle['i']
    info['symbol'] = tickr
    info['open'] = open
    info['close'] = close
    info['high'] = high
    info['low'] = low
    info['volume'] = volume
    info['close_time'] = close_time
    info['interval'] = interval
    info['is_closed'] = is_closed


# Create a function to handle the error
def on_error(ws, error):
    print(f'Error: {error}')


# Create a function to handle the close
def on_close(ws, close_status_code, close_msg):
    print('Closed connection')

# Create DataFrame with info
    df = pd.DataFrame(info, index=[6])
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    print(df)


if __name__ == '__main__':
    websocket.enableTrace(False)  # Set to True to see the websocket logs
    ws = websocket.WebSocketApp(URL, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()

import os
import requests
from dotenv import load_dotenv
import pandas as pd
from binance.spot import Spot
import openpyxl
import streamlit as st

load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
client = Spot(api_key=api_key, api_secret=api_secret)

# Binance API base URL
BASE_URL = 'https://api.binance.com/api/v3'


# Get all symbols
def get_all_symbols():
    url = f'{BASE_URL}/exchangeInfo'
    symbols_response = requests.get(url)
    symbols_data = symbols_response.json()
    symbols = [symbol_['symbol'] for symbol_ in symbols_data['symbols']]
    return symbols


all_symbols = list(get_all_symbols())


# Create function to get data
def get_data(info):
    smas = ((30, 100), (50, 200), (70, 300))
    sym_df = pd.DataFrame(info, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                         'taker_buy_quote_asset_volume', 'ignore'])

    # Convert timestamp to datetime
    sym_df['timestamp'] = pd.to_datetime(sym_df['timestamp'], unit='ms')
    sym_df['timestamp'] = sym_df['timestamp'].dt.strftime('%Y-%m-%d')

    # Set index
    # sym_df.set_index('timestamp', inplace=True)

    # Convert 'open', 'high', 'low', 'close' to numeric
    sym_df[['open', 'high', 'low', 'close', 'volume']] = sym_df[['open', 'high', 'low', 'close', 'volume']].apply(
        pd.to_numeric)

    # Add a column for the percent change in price
    sym_df['pct_change'] = sym_df['close'].pct_change()
    # Z-score of volatility
    v = sym_df['pct_change'].rolling(50).std() * 50 ** 0.5  # Annualize volatility
    sym_df['volatility_zs'] = (v - v.rolling(50).mean()) / v.rolling(50).std()  # Z-score of volatility

    # EMA cross
    c1 = f'cross_{smas[0][0]}_{smas[0][1]}'
    c2 = f'cross_{smas[1][0]}_{smas[1][1]}'
    c3 = f'cross_{smas[2][0]}_{smas[2][1]}'
    sym_df[c1] = sym_df['close'].rolling(smas[0][0]).mean() / sym_df['close'].rolling(smas[0][1]).mean() - 1
    sym_df[c2] = sym_df['close'].rolling(smas[1][0]).mean() / sym_df['close'].rolling(smas[1][1]).mean() - 1
    sym_df[c3] = sym_df['close'].rolling(smas[2][0]).mean() / sym_df['close'].rolling(smas[2][1]).mean() - 1

    # Adjust volume
    sym_df['volume'] = sym_df['volume'] / 1000000

    # Drop columns
    sym_df.drop(['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)

    return sym_df


# Parameters
symbol = [sym for sym in all_symbols if sym.endswith('USDT')]
interval = '1d'
limit = 3

print(symbol)


@st.cache_data
def load_and_process_data():
    # klines
    endpoint = f'{BASE_URL}/klines'
    # Loop through all symbols and include them in one variable
    data = {}
    for sym in symbol:
        params = {'symbol': sym, 'interval': interval, 'limit': limit}
        response = requests.get(endpoint, params)
        klines = response.json()
        data[sym] = klines
    # Process klines data and create a DataFrame
    all_data = {sym: get_data(data) for sym, data in data.items()}
    df = pd.concat(all_data.values(), keys=all_data.keys())
    return df


# Load the cached df variable
df = load_and_process_data()

#
# # Export to csv
# df.to_excel('C:/Users/manu_/Downloads/symbols.xlsx')

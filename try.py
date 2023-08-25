import yfinance as yf, numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import math
import openpyxl

smas = ((30, 100), (50, 200), (70, 300))
ventana = 250

tickers = ['LMT', 'SO', 'BAC', 'ABT', 'IBM', 'MCD', 'TMO', 'WFC', 'COST', 'TSLA', 'NFLX', 'BA', 'AMAT', 'UNH', 'EXC', 'T',
 'C', 'GD', 'SPG', 'INTU', 'AXP', 'GE', 'HD', 'CVX', 'DHR', 'LUV', 'TXN', 'LLY', 'SBUX', 'CVS', 'TGT', 'PEP',
 'GOOGL', 'HON', 'JPM', 'QCOM', 'CMCSA', 'VZ', 'FDX', 'PG', 'NEM', 'AAPL', 'LOW', 'DIS', 'SLB', 'PM', 'CSX',
 'KO', 'GS', 'MET', 'NSC', 'AMGN', 'MMM', 'META', 'JNJ', 'AMZN', 'INTC', 'V', 'NEE', 'WMT', 'CSCO', 'GM', 'COP',
 'CAT', 'ADBE', 'ORCL', 'CME', 'PFE', 'OXY', 'MA', 'MSFT', 'UPS', 'ADP', 'MS', 'CRM', 'UNP', 'MO', 'EMR', 'NVDA',
 'GILD', 'BMY', 'ABBV', 'NKE', 'XOM', 'MRK', 'MDLZ']

df = yf.download(tickers, start='2000-01-01',auto_adjust=True)
spy = yf.download('SPY', start='2000-01-01', auto_adjust=True)
vix = yf.download('^VIX', start='2000-01-01', auto_adjust=True)

dfs_train, dfs_test = [], []
for ticker in tickers:
    data = df['Close'][ticker].to_frame()
    data.columns = ['Close']
    dif = data['Close'].diff()
    RSI_CONS = 50
    win = pd.DataFrame(np.where(dif > 0, dif, 0))
    loss = pd.DataFrame(np.where(dif < 0, abs(dif), 0))
    ema_win = win.ewm(alpha=1/RSI_CONS).mean()
    ema_loss = loss.ewm(alpha=1/RSI_CONS).mean()
    rs = ema_win / ema_loss
    rsi = 100 - (100 / (1 + rs))
    rsi.index = data.index

    data['pctChange'] = data['Close'].pct_change()
    data['fw'] = data['Close'].shift(-ventana)/data['Close']-1
    data[f'RSI_{RSI_CONS}'] = rsi/100
    v = data['pctChange'].rolling(50).std() * 50**0.5
    data['volatilidad_zs'] = (v - v.rolling(50).mean()) / v.rolling(50).std()
    data['volatilidad_vix'] = v / vix.Close
    data['vix'] = vix.Close

    spy_zs_slow = (spy.Close - spy.Close.rolling(80).mean()) / spy.Close.rolling(80).std()
    spy_zs_fast = (spy.Close - spy.Close.rolling(40).mean()) / spy.Close.rolling(40).std()

    data['SP500_Zscore_fast'] = spy_zs_fast
    data['SP500_Zscore_slow'] = spy_zs_slow
    data['SP500_rel'] = spy_zs_slow / spy_zs_fast

    data['sma_volatilidad'] = data['pctChange'].rolling(50).std() * 50**0.5
    data['ema_volatilidad'] = data['pctChange'].ewm(span=40).std() * 40**0.5
    data['SPY_Corr'] = data.Close.pct_change().rolling(40).corr(spy.Close.pct_change())
    c1 = f'cruce_{smas[0][0]}_{smas[0][1]}'
    c2 = f'cruce_{smas[1][0]}_{smas[1][1]}'
    c3 = f'cruce_{smas[2][0]}_{smas[2][1]}'
    data[c1] = data['Close'].rolling(smas[0][0]).mean()/data['Close'].rolling(smas[0][1]).mean()-1
    data[c2] = data['Close'].rolling(smas[1][0]).mean()/data['Close'].rolling(smas[1][1]).mean()-1
    data[c3] = data['Close'].rolling(smas[2][0]).mean()/data['Close'].rolling(smas[2][1]).mean()-1
    qtrain = int(len(data)*0.85)
    dfs_train.append(data.reset_index(drop=True).iloc[:qtrain])
    dfs_test.append(data.reset_index(drop=True).iloc[qtrain:])

data_train = pd.concat(dfs_train).reset_index(drop=True)
data_test = pd.concat(dfs_test).reset_index(drop=True)
len(data_train.dropna()), len(data_test.dropna())
data.to_excel('C:/Users/manu_/Downloads/try.xlsx')
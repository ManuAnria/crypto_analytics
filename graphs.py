from crypto_analytics import df, symbol
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np


def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data['timestamp'],
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])
    return fig


def create_corr_chart(dfCorr):
    fig = plt.figure(figsize=(12, 8))
    plt.matshow(dfCorr.corr(), fignum=fig.number, cmap='binary')
    plt.xticks(range(dfCorr.shape[1]), dfCorr.columns, fontsize=14, rotation=90)
    plt.yticks(range(dfCorr.shape[1]), dfCorr.columns, fontsize=14)

    cb = plt.colorbar(orientation='vertical', label='correlation coefficient')
    cb.ax.tick_params(labelsize=14)
    plt.title('Correlation Matrix', fontsize=16, y=1.15)

    ax = plt.gca()

    ax.set_xticks(np.arange(-.5, len(dfCorr.columns), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(dfCorr.columns), 1), minor=True)
    ax.grid(which='minor', color='w', linestyle='-', linewidth=3)

    for i in range(dfCorr.shape[0]):
        for j in range(dfCorr.shape[1]):
            if dfCorr.iloc[i, j] > 0.6:
                color = 'white'
            else:
                color = 'black'
            fig.gca().text(i, j, '{:.2f}'.format(dfCorr.iloc[i, j]), ha='center', va='center', color=color,
                           fontsize=14)

    return(plt)

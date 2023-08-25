from crypto_analytics import df, symbol
import plotly.graph_objs as go


def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data['timestamp'],
                                         open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])
    return fig

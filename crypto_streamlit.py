import streamlit as st
from crypto_analytics import df, symbol
import pandas as pd
from graphs import create_candlestick_chart


def main():
    st.title('Crypto Analytics')

    with st.container():
        # Multiselect for symbols to filter and show values only for those symbols
        options = st.multiselect('', symbol, placeholder='Choose symbols')
        if options:
            for option in options:
                st.header(f'Asset Information for : {option}')
                st.write(df.loc[option])
                st.header('Asset Candlestick Chart: ')
                st.plotly_chart(create_candlestick_chart(df.loc[option]))
                st.header('Asset Volume: ')
                st.bar_chart(df.loc[option], x='timestamp', y=['volume'])


if __name__ == '__main__':
    main()

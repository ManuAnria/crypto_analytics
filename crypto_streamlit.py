import streamlit as st
from crypto_analytics import df, symbol
import pandas as pd
from datetime import datetime, timedelta
from graphs import create_candlestick_chart, create_corr_chart


def main():
    st.title('Crypto Analytics')

    with st.container():
        st.header('Asset Details: ')
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

    with st.container():
        # Show assets with the highest pct_change during last 24 hours
        st.header('Assets with highest growth: ')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Last 24 hours
        last_1 = df['timestamp'] >= (datetime.now() - timedelta(days=1))
        df_last1 = df.loc[last_1]
        df_last1['timestamp'] = df_last1['timestamp'].dt.strftime('%Y-%m-%d')
        df_last1.sort_values('pct_change', ascending=False, inplace=True)
        # Last 30 days
        last_30 = df['timestamp'] >= (datetime.now() - timedelta(days=30))
        df_last30 = df.loc[last_30]
        df_last30['timestamp'] = df_last30['timestamp'].dt.strftime('%Y-%m-%d')
        df_last30.sort_values('pct_change', ascending=False, inplace=True)
        # This year
        this_year = df['timestamp'].dt.year == datetime.now().year
        df_this_year = df.loc[this_year]
        df_this_year['timestamp'] = df_this_year['timestamp'].dt.strftime('%Y-%m-%d')
        df_this_year.sort_values('pct_change', ascending=False, inplace=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Last 24 hours')
            st.write(df_last1['pct_change'].head(10))
        with col2:
            st.header('Last 30 days')
            st.write(df_last30['pct_change'].head(10))
        with col3:
            st.header('This year')
            st.write(df_this_year['pct_change'].head(10))







if __name__ == '__main__':
    main()

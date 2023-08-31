# Crypto Analytics

This project is currently composed by 3 files, and will be extended with aditional ones.

# 1. crypto_analytics.py:
This file retrieves data from Biance API of all crypto assets valued in USDT from the last 1000 days and creates a Dataframe with this information.

After that, a function is called to perform transformation and analysis to the Dataframe.
The function does the following:
* Convert timestamp format to date
* Convert numeric columns format to float
* Add a new column with daily variation
* Add columns indicating if the asset is experiencing a bullish/bearish monthly and yearly trend
* Add a new column detailing if a gap was generated between the close of prior day and open of current day
* Add a new column quantifying the gap
* Add columns calculating crosses between some fast and slow SMAs
* Adjust volume value
* Drop unnecessary columns

Finally, in order to prevent the code to be re-runned every time an update is made in other files, the outcome of this program is cached.

# 2. graphs.py:
This file contains function that generate different plots:
* Candlestick chart
* Trend Chart
* Trend Change Chart

# 3. crypto_streamlit.py
This file takes inputs from the other 2 files and proccess and display them in a Streamlit application.
  ### A. Asset Details
  This section allows the user to select an asset, and displays the Dataframe information applicable to that asset, along with a candlestick chart     and a volume bar graph of the same asset
  ### B. Assets with highest grow
  This section allows the user to select from a range of days and retrieves the assets that had grown the most during that range.
  ### C. Trend Information:
  This section asks the user for an asset, and retrieves some trend information in charts.
  The first chart makes a comparisson between monthly and yearly trends, indicating for bullish and bearish yearly trends, how many bearish and        bullish monthly trends are there.
  The second chart indicates the moments where monthly and yearly trends changed.

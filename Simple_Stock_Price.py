$ pip install yfinance --upgrade --no-cache-dir

import yfinance as yf
import streamlit as st
import pandas as pd


# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

#define the ticker symbol
#default is GOOGL (Google)
tickerSymbol = st.text_input("Enter the symbol of the stock you're interested in below.", 'GOOGL')

sym = yf.Ticker(tickerSymbol)

company_name = sym.info['longName']

# Define the timeframe you're interested in oberserving the stock between
# Default is May 31st 2010 to May 31st 2020
start_date = st.text_input("What starting date would you like to observe this stock from?", '2010-5-31')
end_date = st.text_input("What is the end date?", '2020-5-31')


st.write("""
# Simple Stock Price App

""")
st.write('Shown below are the stock **closing price** and ***volume*** of', company_name, 'starting on', start_date, 'and ending on', end_date, '!')

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

# The columns will be: Open High Low Close Volume Dividends Stock Splits

st.write("""

## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)

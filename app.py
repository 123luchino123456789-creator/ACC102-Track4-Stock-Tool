import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="ACC102 Track4 Stock Tool", layout="wide")
st.title("ACC102 US Stock Analysis Tool")
st.subheader("Interactive Data Visualization Product")

ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

data = yf.download(ticker, start=start_date, end=end_date)

if not data.empty:
    close = data["Close"]
    total_return = (close.iloc[-1] / close.iloc[0] - 1) * 100
    daily_ret = close.pct_change()
    vol = daily_ret.std() * (252 ** 0.5) * 100

    st.metric("Total Return", f"{round(total_return, 2)}%")
    st.metric("Annual Volatility", f"{round(vol, 2)}%")

    st.subheader("Historical Price Trend")
    st.line_chart(close)

else:
    st.warning("No data found. Check ticker or date range.")

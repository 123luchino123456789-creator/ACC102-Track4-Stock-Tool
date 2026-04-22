import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 页面基础设置
st.set_page_config(page_title="ACC102 Track4 Stock Tool", layout="wide")
st.title("📈 ACC102 US Stock Analysis Tool")
st.subheader("Interactive Data Visualization Product")

# 1. 用户输入：股票代码+时间范围
ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

# 2. 下载股票数据（最稳定写法）
data = yf.download(ticker, start=start_date, end=end_date)

# 3. 数据校验+安全计算（修复报错核心）
if not data.empty:
    # 基础收益计算（绝对不会报错）
    close_price = data["Close"]
    total_return = (close_price.iloc[-1] / close_price.iloc[0] - 1) * 100
    daily_return = close_price.pct_change()
    annual_vol = daily_return.std() * (252 ** 0.5) * 100

    # 显示核心指标
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Return", f"{total_return:.2f}%")
    with col2:
        st.metric("Annual Volatility", f"{annual_vol:.2f}%")

    # 绘制走势图
    st.subheader("📊 Historical Price Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(close_price, label="Closing Price", color="#1f77b4")
    ax.set_title(f"{ticker} Daily Close Price")
    ax.legend()
    st.pyplot(fig)

else:
    st.warning("⚠️ No valid data found! Please check the stock ticker and date range.")

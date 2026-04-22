import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 页面标题（作业规范）
st.set_page_config(page_title="ACC102 Track4 Stock Tool", layout="wide")
st.title("ACC102 US Stock Analysis Tool")
st.subheader("Interactive Data Visualization Product")

# 1. 用户交互：输入股票代码+选日期
ticker = st.text_input("Enter Stock Ticker", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

# 2. 下载股票数据
data = yf.download(ticker, start=start_date, end=end_date)

# 3. 数据计算 + 展示
if not data.empty:
    # 计算核心指标（会计/金融必考点）
    data["Daily Return"] = data["Close"].pct_change()
    total_return = (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
    annual_volatility = data["Daily Return"].std() * (252 ** 0.5) * 100

    # 指标卡片（Streamlit核心交互）
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Return", f"{total_return:.2f}%")
    with col2:
        st.metric("Annual Volatility", f"{annual_volatility:.2f}%")

    # 4. 可视化图表
    st.subheader(" Price Trend Chart")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data["Close"], label="Closing Price", color="#1f77b4")
    ax.set_title(f"{ticker} Historical Price")
    ax.legend()
    st.pyplot(fig)

else:
    st.warning(" No data found. Please check the ticker or date range.")
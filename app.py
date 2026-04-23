import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="ACC102 Stock Analysis Pro",
    layout="wide"
)

st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 5px 5px 0 0;
        gap: 1rem;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("ACC102 US Stock Analysis Tool")

with st.sidebar:
    st.header("Control Panel")
    
    ticker = st.text_input("Stock Ticker", "AAPL").upper()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=365)
        )
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    st.divider()
    st.subheader("Analysis Options")
    
    show_advanced = st.checkbox("Show Advanced Metrics", value=True)
    show_volume = st.checkbox("Show Volume", value=True)
    ma_periods = st.multiselect(
        "Moving Average Periods",
        [5, 20, 50, 100, 200],
        default=[20, 50]
    )
    
    st.subheader("Technical Indicators")
    show_rsi = st.checkbox("Relative Strength Index (RSI)", value=True)
    show_macd = st.checkbox("MACD", value=True)
    
    st.divider()
    st.subheader("Benchmark Comparison")
    benchmark = st.selectbox(
        "Select Benchmark",
        ["SPY", "QQQ", "DIA", "IWM", "None"]
    )

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Price Analysis", "Technical Indicators", "Data Details"])

@st.cache_data(ttl=3600)
def load_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        info = stock.info
        
        if benchmark != "None":
            benchmark_data = yf.download(benchmark, start=start_date, end=end_date)
            if not benchmark_data.empty:
                data[f'{benchmark}_Return'] = benchmark_data['Close'].pct_change()
        
        return data, info
    except Exception as e:
        st.error(f"Data loading failed: {str(e)}")
        return pd.DataFrame(), {}

try:
    data, info = load_stock_data(ticker, start_date, end_date)
    
    if data.empty:
        st.warning("No data found. Please check ticker symbol or date range.")
    else:
        close = data["Close"]
        returns = close.pct_change()
        
        total_return = (close.iloc[-1] / close.iloc[0] - 1) * 100
        annual_vol = returns.std() * np.sqrt(252) * 100
        sharpe_ratio = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        max_drawdown = (close / close.expanding().max() - 1).min() * 100
        
        for period in ma_periods:
            data[f'MA{period}'] = close.rolling(window=period).mean()
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"{ticker} - {info.get('longName', 'N/A')}")
                st.write(f"**Industry**: {info.get('industry', 'N/A')} | **Sector**: {info.get('sector', 'N/A')}")
                st.write(f"**Market Cap**: ${info.get('marketCap', 0):,.0f}")
                st.write(f"**Forward P/E**: {info.get('forwardPE', 'N/A')}")
            
            with col2:
                st.subheader("Key Metrics")
                
                metric_cols = st.columns(2)
                with metric_cols[0]:
                    st.metric(
                        "Total Return",
                        f"{total_return:+.2f}%",
                        delta=f"{total_return:+.1f}%"
                    )
                with metric_cols[1]:
                    st.metric(
                        "Annual Volatility",
                        f"{annual_vol:.2f}%"
                    )
                
                if show_advanced:
                    metric_cols2 = st.columns(2)
                    with metric_cols2[0]:
                        st.metric(
                            "Sharpe Ratio",
                            f"{sharpe_ratio:.2f}"
                        )
                    with metric_cols2[1]:
                        st.metric(
                            "Max Drawdown",
                            f"{max_drawdown:.2f}%"
                        )
            
            st.divider()
            st.subheader("Price Trend")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=close,
                mode='lines',
                name='Close Price',
                line=dict(color='#3B82F6', width=2)
            ))
            
            for period in ma_periods:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[f'MA{period}'],
                    mode='lines',
                    name=f'{period}-Day MA',
                    line=dict(width=1, dash='dash')
                ))
            
            if show_volume:
                fig.add_trace(go.Bar(
                    x=data.index,
                    y=data['Volume'],
                    name='Volume',
                    yaxis='y2',
                    opacity=0.3,
                    marker_color='#94A3B8'
                ))
                
                fig.update_layout(
                    yaxis2=dict(
                        title="Volume",
                        overlaying="y",
                        side="right",
                        showgrid=False
                    )
                )
            
            fig.update_layout(
                title=f"{ticker} Price Chart",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                hovermode="x unified",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Daily Returns Distribution")
                
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(
                    x=returns.dropna() * 100,
                    nbinsx=50,
                    name='Daily Returns',
                    marker_color='#3B82F6',
                    opacity=0.7
                ))
                
                fig_hist.update_layout(
                    title="Daily Returns Distribution",
                    xaxis_title="Daily Return (%)",
                    yaxis_title="Frequency",
                    height=400,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                st.subheader("Statistics")
                
                stats_data = {
                    "Mean (%)": f"{returns.mean() * 100:.4f}",
                    "Std Dev (%)": f"{returns.std() * 100:.4f}",
                    "Skewness": f"{returns.skew():.4f}",
                    "Kurtosis": f"{returns.kurtosis():.4f}",
                    "Min (%)": f"{returns.min() * 100:.4f}",
                    "Max (%)": f"{returns.max() * 100:.4f}",
                    "Positive Days": f"{(returns > 0).sum()}",
                    "Negative Days": f"{(returns < 0).sum()}"
                }
                
                for key, value in stats_data.items():
                    st.metric(key, value)
            
            if benchmark != "None" and f'{benchmark}_Return' in data.columns:
                st.divider()
                st.subheader(f"vs {benchmark} Comparison")
                
                cum_stock_return = (1 + returns).cumprod() - 1
                cum_bench_return = (1 + data[f'{benchmark}_Return']).cumprod() - 1
                
                fig_compare = go.Figure()
                fig_compare.add_trace(go.Scatter(
                    x=cum_stock_return.index,
                    y=cum_stock_return * 100,
                    mode='lines',
                    name=ticker,
                    line=dict(color='#3B82F6', width=2)
                ))
                fig_compare.add_trace(go.Scatter(
                    x=cum_bench_return.index,
                    y=cum_bench_return * 100,
                    mode='lines',
                    name=benchmark,
                    line=dict(color='#EF4444', width=2)
                ))
                
                fig_compare.update_layout(
                    title="Cumulative Returns Comparison",
                    xaxis_title="Date",
                    yaxis_title="Cumulative Return (%)",
                    height=400,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig_compare, use_container_width=True)
        
        with tab3:
            if show_rsi or show_macd:
                rows = sum([show_rsi, show_macd]) + 1
                fig_tech = make_subplots(
                    rows=rows, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=["Price Chart"] + 
                    (["RSI"] if show_rsi else []) + 
                    (["MACD"] if show_macd else [])
                )
                
                row_idx = 1
                
                fig_tech.add_trace(
                    go.Candlestick(
                        x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name="OHLC"
                    ),
                    row=row_idx, col=1
                )
                
                row_idx += 1
                
                if show_rsi:
                    delta = close.diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    
                    fig_tech.add_trace(
                        go.Scatter(
                            x=data.index,
                            y=rsi,
                            name="RSI",
                            line=dict(color='#8B5CF6', width=2)
                        ),
                        row=row_idx, col=1
                    )
                    
                    fig_tech.add_hline(
                        y=70, line_dash="dash", 
                        line_color="red", opacity=0.5,
                        row=row_idx, col=1
                    )
                    fig_tech.add_hline(
                        y=30, line_dash="dash", 
                        line_color="green", opacity=0.5,
                        row=row_idx, col=1
                    )
                    
                    row_idx += 1
                
                if show_macd:
                    exp1 = close.ewm(span=12, adjust=False).mean()
                    exp2 = close.ewm(span=26, adjust=False).mean()
                    macd = exp1 - exp2
                    signal = macd.ewm(span=9, adjust=False).mean()
                    histogram = macd - signal
                    
                    fig_tech.add_trace(
                        go.Scatter(
                            x=data.index,
                            y=macd,
                            name="MACD",
                            line=dict(color='#3B82F6', width=2)
                        ),
                        row=row_idx, col=1
                    )
                    
                    fig_tech.add_trace(
                        go.Scatter(
                            x=data.index,
                            y=signal,
                            name="Signal",
                            line=dict(color='#EF4444', width=2)
                        ),
                        row=row_idx, col=1
                    )
                    
                    fig_tech.add_trace(
                        go.Bar(
                            x=data.index,
                            y=histogram,
                            name="Histogram",
                            marker_color=np.where(histogram > 0, '#10B981', '#EF4444')
                        ),
                        row=row_idx, col=1
                    )
                
                fig_tech.update_layout(
                    height=200 * rows,
                    showlegend=True,
                    template="plotly_white",
                    xaxis_rangeslider_visible=False
                )
                
                st.plotly_chart(fig_tech, use_container_width=True)
        
        with tab4:
            st.subheader("Raw Data")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                show_rows = st.slider("Display Rows", 10, 100, 20)
            with col2:
                show_all = st.checkbox("Show All Columns", value=False)
            with col3:
                data_format = st.selectbox("Data Format", ["Raw Data", "Descriptive Statistics"])
            
            if data_format == "Raw Data":
                if not show_all:
                    display_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                    display_data = data[display_cols].tail(show_rows)
                else:
                    display_data = data.tail(show_rows)
                
                st.dataframe(
                    display_data.style.format({
                        'Open': '{:.2f}',
                        'High': '{:.2f}',
                        'Low': '{:.2f}',
                        'Close': '{:.2f}',
                        'Volume': '{:,.0f}'
                    }),
                    use_container_width=True
                )
                
                csv = data.to_csv().encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{ticker}_stock_data.csv",
                    mime="text/csv"
                )
            
            else:
                st.dataframe(
                    data[['Open', 'High', 'Low', 'Close', 'Volume']].describe().round(2),
                    use_container_width=True
                )
            
            if len(ma_periods) >= 2:
                st.divider()
                st.subheader("Moving Averages Correlation")
                
                ma_data = pd.DataFrame()
                for period in ma_periods:
                    ma_data[f'MA{period}'] = data[f'MA{period}']
                
                corr_matrix = ma_data.corr()
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=np.round(corr_matrix.values, 2),
                    texttemplate='%{text}',
                    textfont={"size": 10}
                ))
                
                fig_corr.update_layout(
                    title="Moving Averages Correlation Matrix",
                    height=400
                )
                
                st.plotly_chart(fig_corr, use_container_width=True)

except Exception as e:
    st.error(f"Error occurred: {str(e)}")
    st.info("Please try:")
    st.info("1. Check internet connection")
    st.info("2. Verify stock ticker is correct")
    st.info("3. Adjust date range")

st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748B; padding: 1rem;">
    <p>ACC102 Stock Analysis Tool | Data Source: Yahoo Finance | Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    <p style="font-size: 0.8rem;">Disclaimer: Data provided for reference only, not investment advice</p>
</div>
""", unsafe_allow_html=True)

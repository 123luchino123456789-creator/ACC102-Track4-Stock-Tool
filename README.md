Project Overview

This repository contains the complete code and documentation for the ACC102 Mini Assignment (Track 4: Interactive Data Analysis Tool). The project implements an interactive web application for financial data analysis using Streamlit and Yahoo Finance API, designed specifically for finance students and individual investors.

Features

Interactive Dashboard: Multi-tab interface with real-time data visualization
Comprehensive Analysis:

·Price trends with customizable moving averages

·Technical indicators (RSI, MACD)

·Statistical metrics and performance analysis

·Benchmark comparison against major ETFs

Data Exploration:

·Raw data inspection with filtering options

·Descriptive statistics

·CSV export functionality

User-Friendly Design:

·Responsive sidebar controls

·Interactive Plotly charts

·Clear metric displays

·Error handling and user guidance

Installation

Prerequisites

·Python 3.7.0 or higher

·pip package manager

Step-by-Step Setup

1.Clone the repository
git clone <repository-url>
cd acc102-stock-analysis

2.Create virtual environment (recommended)
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3.Install dependencies
pip install -r requirements.txt

4.Run the application
streamlit run app.py
The application will open automatically in your default browser at http://localhost:8501.

Usage Guide
1. Basic Operations

·Stock Selection: Enter a valid US stock ticker (e.g., AAPL, MSFT, GOOGL) in the sidebar

·Date Range: Select analysis period using date pickers

·Configuration: Adjust analysis options in the sidebar controls

2. Dashboard Navigation
The application provides four main tabs:
Overview Tab

·Company information display

·Key performance metrics

·Interactive price chart with volume overlay

·Moving average overlays

Price Analysis Tab

·Daily returns distribution histogram

·Statistical summary table

·Benchmark comparison chart (optional)

·Cumulative returns visualization

Technical Indicators Tab

·RSI (Relative Strength Index) with overbought/oversold levels

·MACD (Moving Average Convergence Divergence) with signal line

·Multi-panel chart layout for comprehensive analysis

Data Details Tab

·Raw data table with customizable view

·Descriptive statistics

·Moving averages correlation matrix

·CSV export functionality

3. Advanced Features

·Moving Averages: Select from 5, 20, 50, 100, or 200-day periods

·Technical Indicators: Toggle RSI and MACD calculations

·Benchmark Comparison: Compare against SPY, QQQ, DIA, or IWM ETFs

·Data Export: Download filtered data as CSV files

Project Structure

acc102-stock-analysis/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
├── ACC102_Mini_Assignment.ipynb  # Jupyter notebook with complete analysis
├── ACC102_Stock_Analysis_AAPL.csv  # Example output data
├── AAPL_analysis_summary.txt      # Example analysis report
└── AAPL_analysis_charts.png       # Example visualization output

Data Source

All financial data is sourced from Yahoo Finance
via the yfinancePython library (version 0.2.28), providing:

·Real-time and historical stock prices

·Trading volume data

·Company fundamental information

·ETF data for benchmark comparisons

Dependencies

The project is optimized for Python 3.7.0 compatibility with the following specific versions:

·streamlit==1.28.0- Web application framework

·yfinance==0.2.28- Yahoo Finance data API

·pandas==1.5.3- Data manipulation and analysis

·numpy==1.21.6- Numerical computations

·plotly==5.17.0- Interactive visualizations

Error Handling

The application includes comprehensive error handling for:

·Invalid stock tickers

·Network connectivity issues

·Date range conflicts

·Data availability problems

·Users receive clear guidance for resolving common issues.

Limitations and Future Enhancements
Current Limitations

·Data Source: Dependent on Yahoo Finance API availability

·Real-time Data: 15-minute delay for free tier data

·Coverage: Primarily focused on US-listed securities

·Advanced Features: Limited to basic technical analysis

Planned Enhancements

·Portfolio analysis with multiple assets

·Additional technical indicators (Bollinger Bands, Ichimoku Cloud)

·Fundamental ratio calculations

·Alert system for price thresholds

·Machine learning predictions

·Mobile-responsive design

Academic Integrity

This project follows XJTLU Academic Integrity Policy:

·AI Tool Usage: Any AI assistance is documented in the reflection report

·Code Attribution: All external code is properly cited

·Data Sources: All data sources are clearly acknowledged

·Original Work: Core analysis and implementation represent personal contribution

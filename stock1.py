import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start_date')
end_date = st.sidebar.date_input('End_date')
data = yf.download(ticker, start=start_date,end=end_date)
data

news = st.tabs(["Top 10 News"])

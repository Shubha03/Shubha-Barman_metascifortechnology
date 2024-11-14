 
import streamlit as st  
import yfinance as yf  
import pandas as pd  
import plotly.graph_objs as go  
import plotly.express as px  
from datetime import datetime, timedelta 
# Set up the Streamlit page configuration  
st.set_page_config(page_title='Stock Market Dashboard', layout='wide')  

 


# Title of the Dashboard  
st.markdown('<h1 class="main-title">Stock Market Dashboard</h1>', unsafe_allow_html=True)  

# Sidebar for user inputs  
st.sidebar.markdown('<h2 class="sidebar-header">Stock Selection</h2>', unsafe_allow_html=True)  

indian_stocks = [  
    'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'TCS.NS', 'ICICIBANK.NS',   
    'HINDUNILVR.NS', 'AXISBANK.NS', 'TATAMOTORS.NS', 'MARUTI.NS', 'WIPRO.NS'  
]  

# Multi-select stocks  
selected_stocks = st.sidebar.multiselect(  
    'Choose Stocks to Analyze',   
    indian_stocks,   
    default=['RELIANCE.NS', 'HDFCBANK.NS']  
)  

# Date range selection  
st.sidebar.markdown('<h2 class="sidebar-header">Date Range</h2>', unsafe_allow_html=True)  
start_date = st.sidebar.date_input('Start Date', datetime.now() - timedelta(days=365))  
end_date = st.sidebar.date_input('End Date', datetime.now())  

# Function to fetch stock data  
@st.cache_data  
def fetch_stock_data(tickers, start, end):  
    data = yf.download(tickers, start=start, end=end)['Close']  
    return data  

# Fetch stock data  
if selected_stocks:  
    stock_data = fetch_stock_data(selected_stocks, start_date, end_date)  
    

    
    # Line Chart for Stock Prices  
    fig_prices = go.Figure()  
    for stock in selected_stocks:  
        fig_prices.add_trace(go.Scatter(  
            x=stock_data.index,   
            y=stock_data[stock],   
            mode='lines',   
            name=stock  
        ))  
    
    fig_prices.update_layout(  
        title='Stock Prices Over Time',  
        xaxis_title='Date',  
        yaxis_title='Price (INR)',  
        height=600  
    )  
    st.plotly_chart(fig_prices, use_container_width=True)  
    
    
    # Downloadable Data  
    st.subheader('Download Stock Data')  
    
    # Convert data to CSV  
    csv_data = stock_data.reset_index()  
    csv_data.to_csv('stock_data.csv', index=False)  
    
    with open('stock_data.csv', 'rb') as file:  
        st.download_button(  
            label='Download Stock Data (CSV)',  
            data=file,  
            file_name='stock_data.csv',  
            mime='text/csv'  
        )  

else:  
    st.warning('Please select at least one stock to analyze.')  

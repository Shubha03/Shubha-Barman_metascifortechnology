import streamlit as st  
import yfinance as yf  
import pandas as pd  
import plotly.graph_objects as plt  
import plotly.express as px  
from datetime import datetime, timedelta  

# Set up the Streamlit page configuration  
st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")  

# Custom CSS for enhanced styling  
def local_css():  
    st.markdown("""  
    <style>  
    .big-font {  
        font-size:20px !important;  
        font-weight:bold;  
        color:#2c3e50;  
    }  
    .metric-container {  
        background-color:#f0f2f6;  
        padding:15px;  
        border-radius:10px;  
    }  
    </style>  
    """, unsafe_allow_html=True)  

# Function to fetch stock data  
def fetch_stock_data(ticker, period='1y'):  
    try:  
        stock = yf.Ticker(ticker)  
        df = stock.history(period=period)  
        
        # Calculate moving averages  
        df['MA50'] = df['Close'].rolling(window=50).mean()  
        df['MA200'] = df['Close'].rolling(window=200).mean()  
        
        return df, stock.info  
    except Exception as e:  
        st.error(f"Error fetching data for {ticker}: {e}")  
        return None, None  

# Function to create stock price chart  
def create_stock_chart(df, ticker):  
    fig = plt.Figure()  
    
    # Close price line  
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['Close'],   
        mode='lines',   
        name='Close Price',  
        line=dict(color='blue', width=2)  
    ))  
    
    # 50-day Moving Average  
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['MA50'],   
        mode='lines',   
        name='50-Day MA',  
        line=dict(color='green', width=2, dash='dot')  
    ))  
    
    # 200-day Moving Average  
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['MA200'],   
        mode='lines',   
        name='200-Day MA',  
        line=dict(color='red', width=2, dash='dot')  
    ))  
    
    # Customize layout  
    fig.update_layout(  
        title=f'{ticker} Stock Price Analysis',  
        xaxis_title='Date',  
        yaxis_title='Price (INR)',  
        hovermode='x unified'  
    )  
    
    return fig  

# Main dashboard function  
def stock_dashboard():  
    # Apply custom CSS  
    local_css()  
    
    # Dashboard Title  
    st.title("Stock Market Dashboard")  
    st.markdown("---")  
    
    # Sidebar for user inputs  
    st.sidebar.header("Stock Analysis Parameters")  
    
    # Stock ticker input  
    default_tickers = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS']  
    selected_tickers = st.sidebar.multiselect(  
        "Select Stock Tickers",   
        default_tickers,   
        default=default_tickers  
    )  
    
    # Time period selection  
    period = st.sidebar.selectbox(  
        "Select Analysis Period",   
        ['1mo', '3mo', '6mo', '1y', '2y', '5y']  
    )  
    
    # Fetch and display stock data  
    if selected_tickers:  
        # Create columns for stock metrics  
        columns = st.columns(len(selected_tickers))  
        
        # Store fetched data for comparison  
        stock_data = {}  
        
        # Fetch and display data for each selected ticker  
        for i, ticker in enumerate(selected_tickers):  
            with columns[i]:  
                # Fetch stock data  
                df, stock_info = fetch_stock_data(ticker, period)  
                
                if df is not None and stock_info is not None:  
                    # Store data for later use  
                    stock_data[ticker] = {'df': df, 'info': stock_info}  
                    
                    # Display stock card  
                    st.markdown(f"<div class='metric-container'>", unsafe_allow_html=True)  
                    st.markdown(f"<h3 class='big-font'>{ticker}</h3>", unsafe_allow_html=True)  
                    
                    # Current price and change  
                    current_price = df['Close'][-1]  
                    price_change = df['Close'][-1] - df['Close'][-2]  
                    change_percent = (price_change / df['Close'][-2]) * 100  
                    
                    st.metric(  
                        label="Current Price (INR)",   
                        value=f"₹{current_price:.2f}",  
                        delta=f"{price_change:.2f} ({change_percent:.2f}%)"  
                    )  
                    
                    st.markdown("</div>", unsafe_allow_html=True)  
        
        # Create stock price comparison chart  
        if len(stock_data) > 0:  
            st.header("Stock Price Comparison")  
            comparison_data = pd.DataFrame({  
                ticker: data['df']['Close'] for ticker, data in stock_data.items()  
            })  
            
            # Normalize prices for better comparison  
            normalized_data = comparison_data / comparison_data.iloc[0] * 100  
            
            # Create comparison chart  
            fig_comparison = px.line(  
                normalized_data,   
                title='Normalized Stock Price Comparison',  
                labels={'value': 'Normalized Price (%)', 'index': 'Date'}  
            )  
            st.plotly_chart(fig_comparison, use_container_width=True)  
        
        # Individual stock charts  
        st.header("Detailed Stock Analysis")  
        for ticker, data in stock_data.items():  
            st.subheader(f"{ticker} Detailed Chart")  
            fig = create_stock_chart(data['df'], ticker)  
            st.plotly_chart(fig, use_container_width=True)  
            
            # Additional stock information  
            st.subheader("Stock Details")  
            col1, col2 = st.columns(2)  
            with col1:  
                st.write(f"**Market Cap:** ₹{data['info'].get('marketCap', 'N/A'):,}")  
                st.write(f"**Sector:** {data['info'].get('sector', 'N/A')}")  
            with col2:  
                st.write(f"**52 Week High:** ₹{data['info'].get('fiftyTwoWeekHigh', 'N/A')}")  
                st.write(f"**52 Week Low:** ₹{data['info'].get('fiftyTwoWeekLow', 'N/A')}")  
    
    else:  
        st.warning("Please select at least one stock ticker")  

# Run the dashboard  
if __name__ == "__main__":  
    stock_dashboard()
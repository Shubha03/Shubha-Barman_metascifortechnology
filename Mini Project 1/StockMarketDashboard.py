import streamlit as st  
import yfinance as yf  
import pandas as pd  
import plotly.graph_objects as plt  
import plotly.express as px  
from datetime import datetime, timedelta  

st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")  
 
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

def fetch_stock_data(ticker, period='1y'):  
    try:  
        stock = yf.Ticker(ticker)  
        df = stock.history(period=period)  
         
        df['MA50'] = df['Close'].rolling(window=50).mean()  
        df['MA200'] = df['Close'].rolling(window=200).mean()  
        
        return df, stock.info  
    except Exception as e:  
        st.error(f"Error fetching data for {ticker}: {e}")  
        return None, None  

def create_stock_chart(df, ticker):  
    fig = plt.Figure()  
    
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['Close'],   
        mode='lines',   
        name='Close Price',  
        line=dict(color='blue', width=2)  
    ))  
    
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['MA50'],   
        mode='lines',   
        name='50-Day MA',  
        line=dict(color='green', width=2, dash='dot')  
    ))  
    
    fig.add_trace(plt.Scatter(  
        x=df.index,   
        y=df['MA200'],   
        mode='lines',   
        name='200-Day MA',  
        line=dict(color='red', width=2, dash='dot')  
    ))  
    
    fig.update_layout(  
        title=f'{ticker} Stock Price Analysis',  
        xaxis_title='Date',  
        yaxis_title='Price (INR)',  
        hovermode='x unified'  
    )  
    
    return fig  

def stock_dashboard():  
    local_css()  
    

    st.title("Stock Market Dashboard")  
    st.markdown("---")  
    
    st.sidebar.header("Stock Analysis Parameters")  
    
    default_tickers = ['RELIANCE.NS', 'INFY.NS', 'TCS.NS']  
    selected_tickers = st.sidebar.multiselect(  
        "Select Stock Tickers",   
        default_tickers,   
        default=default_tickers  
    )  
    
    period = st.sidebar.selectbox(  
        "Select Analysis Period",   
        ['1mo', '3mo', '6mo', '1y', '2y', '5y']  
    )  
    
    if selected_tickers:  

        columns = st.columns(len(selected_tickers))  

        stock_data = {}  
        
 
        for i, ticker in enumerate(selected_tickers):  
            with columns[i]:  

                df, stock_info = fetch_stock_data(ticker, period)  
                
                if df is not None and stock_info is not None:  

                    stock_data[ticker] = {'df': df, 'info': stock_info}  
                    
                    st.markdown(f"<div class='metric-container'>", unsafe_allow_html=True)  
                    st.markdown(f"<h3 class='big-font'>{ticker}</h3>", unsafe_allow_html=True)  
                    
                    current_price = df['Close'][-1]  
                    price_change = df['Close'][-1] - df['Close'][-2]  
                    change_percent = (price_change / df['Close'][-2]) * 100  
                    
                    st.metric(  
                        label="Current Price (INR)",   
                        value=f"₹{current_price:.2f}",  
                        delta=f"{price_change:.2f} ({change_percent:.2f}%)"  
                    )  
                    
                    st.markdown("</div>", unsafe_allow_html=True)  
        
        if len(stock_data) > 0:  
            st.header("Stock Price Comparison")  
            comparison_data = pd.DataFrame({  
                ticker: data['df']['Close'] for ticker, data in stock_data.items()  
            })  
            
            normalized_data = comparison_data / comparison_data.iloc[0] * 100  
            
            fig_comparison = px.line(  
                normalized_data,   
                title='Normalized Stock Price Comparison',  
                labels={'value': 'Normalized Price (%)', 'index': 'Date'}  
            )  
            st.plotly_chart(fig_comparison, use_container_width=True)  
         
        st.header("Detailed Stock Analysis")  
        for ticker, data in stock_data.items():  
            st.subheader(f"{ticker} Detailed Chart")  
            fig = create_stock_chart(data['df'], ticker)  
            st.plotly_chart(fig, use_container_width=True)  
            
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

if __name__ == "__main__":  
    stock_dashboard()

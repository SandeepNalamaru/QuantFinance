import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import datetime


st.markdown(
    """
    <style>
    h1 {
        margin-top: -80px;
        font-size: 200%;
    }
    
    h3 {
        font-size: 65%;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)    
    

st.title('Stock Research')
st.subheader('~ Made by Sandeep Nalamaru')
st.subheader('Site under re-construction (yfinance is not free anymore) :(')
tabs = st.tabs(['Technicals', 'Fundamentals', 'Options', 'Backtesting'])

with st.sidebar:
    ticker = st.text_input('Enter Ticker')
    #rfr = st.number_input('Enter Risk Free Rate', value = 0.03)
    


with tabs[0]:
    bench = st.text_input('Input Benchmark/Company', value = 'SPY')    
    if ticker and bench:
        
        start_date = st.date_input('Enter Start Date', value=datetime.date.today()-datetime.timedelta(days=365))
        data = yf.download(ticker, start=start_date, end=datetime.date.today())['Adj Close']
        ret = data.pct_change()
        
        cumret = (ret+1).cumprod()-1
        
        avgret = round((np.mean(ret)*100),2)
        avgret_text = f"Mean Daily Return of {ticker}: {avgret}%"
        std = round((np.std(ret)*100),2)
        std_text =  f"Standard Deviation of {ticker}: {std}%"
        col1, col2 = st.columns(2)
        with col1:
            st.write(avgret_text)
            st.write(std_text)
        
        
        benchmark = yf.download(bench, start=start_date)['Adj Close']
        benchr = benchmark.pct_change()
        bench_ret = (1+benchr).cumprod()-1
        
        marketretavg = round(np.mean(benchr)*100,2)
        marketretavg_text = f"Mean Daily Return of {bench}: {marketretavg}%"
        
        
        with col2:
            marketvaravg = round((np.std(benchr)*100),2)
            std_text =  f"Variance of {bench}: {marketvaravg}%"
            st.write(marketretavg_text)
            st.write(std_text)
        
        tog = pd.concat([cumret, bench_ret], axis=1)
        tog.columns = ['Stock Return', 'Index Return']
        
        covariance = tog['Stock Return'].cov(tog['Index Return'])
        beta = round(covariance/(np.var(bench_ret)),2)
        beta_text = f"Beta: {beta}"
        st.write(beta_text)
        
        #plt.plot(tog.index, tog['Stock Return'], label = 'Stock Returns (Cum)')
        #plt.plot(tog.index, tog['Index Return'], label = 'Index Returns (Cum)')
        st.line_chart(tog)
        
with tabs[1]:
    if ticker:
        ticker1 = st.text_input('Enter company ticker to compare')
        col3, col4 = st.columns(2)
        with col3:
            marketcap = format(round((yf.Ticker(ticker).info['marketCap'])/1000000000,2), ',')
            marketcap_text = f"Market Cap of {ticker}: {marketcap}B"
            st.write(marketcap_text)
            # Company Description:
            #des = yf.Ticker(ticker).info['longBusinessSummary']
            #st.write(des)
            
            pmargin = round((yf.Ticker(ticker).info['profitMargins'])*100,2)
            pmargin_text = f"Profit Margin of {ticker}: {pmargin}%"
            st.write(pmargin_text)
            
            eps = yf.Ticker(ticker).info['trailingEps']
            eps_text = f"EPS of {ticker}: {eps}"
            st.write(eps_text)
            
            de = yf.Ticker(ticker).info['debtToEquity']
            de_text = f"Debt/Equity Ratio of {ticker}: {de}"
            st.write(de_text)
            
            roe = yf.Ticker(ticker).info['returnOnEquity']
            roe_text = f"Return on Equity of {ticker}: {roe}"
            st.write(roe_text)
            
            shorted = round((yf.Ticker(ticker).info['shortPercentOfFloat']),4)
            shorted_text = f"Percentage of total shares shorted: {shorted}%"
            st.write(shorted_text)
            
            
        if ticker1:
            with col4:
                marketcap1 = format(round((yf.Ticker(ticker1).info['marketCap'])/1000000000,2), ',')
                marketcap1_text = f"Market Cap of {ticker1}: {marketcap1}B"
                st.write(marketcap1_text)
                # Company Description:
                #des = yf.Ticker(ticker).info['longBusinessSummary']
                #st.write(des)
                
                pmargin1 = round((yf.Ticker(ticker1).info['profitMargins'])*100,2)
                pmargin1_text = f"Profit Margin of {ticker1}: {pmargin1}%"
                st.write(pmargin1_text)
                
                eps1 = yf.Ticker(ticker1).info['trailingEps']
                eps_text1 = f"EPS of {ticker1}: {eps1}"
                st.write(eps_text1)
                
                de1 = yf.Ticker(ticker1).info['debtToEquity']
                de_text1 = f"Debt/Equity Ratio of {ticker1}: {de1}"
                st.write(de_text1)
                
                roe1 = yf.Ticker(ticker1).info['returnOnEquity']
                roe_text1 = f"Return on Equity of {ticker1}: {roe1}"
                st.write(roe_text1)
                
                shorted1 = round((yf.Ticker(ticker1).info['shortPercentOfFloat']),4)
                shorted_text1 = f"Percentage of total shares shorted: {shorted1}%"
                st.write(shorted_text1)
                
                
                
            
with tabs[2]:
    if ticker:
        price = yf.Ticker(ticker).info['currentPrice']
        price_text = f"Current Price: {price}"
        st.write(price_text)
        
        options_calls = yf.Ticker(ticker).option_chain().calls

        calls = options_calls[['strike','impliedVolatility']].set_index('strike')
        calls.rename(columns={'impliedVolatility': 'IV Calls'}, inplace=True)
        
        options_puts = yf.Ticker(ticker).option_chain().puts
        puts = options_puts[['strike','impliedVolatility']].set_index('strike')
        puts.rename(columns={'impliedVolatility': 'IV Puts'}, inplace=True)
        iv = pd.concat([puts, calls], axis=1)
        st.line_chart(iv)
        
with tabs[3]:
    st.selectbox("Choose your Strat", ['Mean Reversion', 'Momentum'])
    if ticker:
        start_date1 = st.date_input('Please Enter Start Date', value=datetime.date.today()-datetime.timedelta(days=365))
        data1 = yf.download(ticker, start=start_date1, end=datetime.date.today())['Adj Close']
        data_bt = data1.to_frame()
        window = st.number_input('Moving Average Length', value=20)
        data_bt['Moving Average'] = data_bt['Adj Close'].rolling(window=window).mean()
        
        st.line_chart(data_bt)
        data_bt['Signal'] = 0
        data_bt['Signal'][window:] = np.where(data_bt['Adj Close'][window:] < data_bt['Moving Average'][window:], 1, 0)
        data_bt['Position'] = data_bt['Signal'].diff()
        data_bt['Stock Returns'] = data_bt['Adj Close'].pct_change()
        data_bt['Trade Returns'] = data_bt['Position']*data_bt['Stock Returns'].shift(-1)
        total_return = round(((data_bt['Trade Returns'].sum())*100),2)
        number_of_trades = (data_bt['Position']!=0).sum()
        tot_ret_text = f"Trade Returns: {total_return}%"
        trades_text = f"Number of Trades: {number_of_trades}"
        
        
        st.write(tot_ret_text)
        st.write(trades_text)
        st.dataframe(data_bt)

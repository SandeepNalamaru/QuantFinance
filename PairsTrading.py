import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import datetime
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


st.markdown(
    """
    <style>
    h1 {
        margin-top: -80px;
        font-size: 200%;
    }
    
    h3 {
        font-size: 80%;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)    
    

st.title('Pairs Trading')
st.subheader('~ Made by Sandeep Nalamaru')


ticker1 = st.text_input('Enter First Company Ticker')
ticker2 = st.text_input('Enter Second Company Ticker')
start_date = st.date_input('Enter Start Date', value=datetime.date.today()-datetime.timedelta(days=365))
if ticker1 and ticker2:
    data1 = yf.download(ticker1, start=start_date,end=datetime.date.today())['Adj Close']
    ret1 = data1.pct_change()
    
    data2 = yf.download(ticker2, start=start_date,end=datetime.date.today())['Adj Close']
    ret2 = data2.pct_change()
    df = pd.DataFrame({ticker1:ret1, ticker2:ret2})
    df.dropna(inplace=True)
    
    X = sm.add_constant(df[ticker1])  # Add a constant term for the intercept
    model = sm.OLS(df[ticker2], X).fit()  # Fit the OLS model
    residuals = model.resid
    pvalue = adfuller(residuals)
    st.write(pvalue)
    if pvalue[1]<0.05:
        st.write('P-value<0.05 Null hypothesis rejected, Pairs are co-integrated')
    else:
        st.write('P-value>0.05 Null hypothesis accepted, Pairs are not co-integrated')
    st.line_chart(df)
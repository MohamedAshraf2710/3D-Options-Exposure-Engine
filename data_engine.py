import yfinance as yf
import pandas as pd
import numpy as np

def get_real_options_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    
    expiries = ticker.options
    if not expiries:
        return None, None, None
    
    all_calls = []
    current_price = ticker.history(period="1d")['Close'].iloc[-1]
    

    for date in expiries[:5]:
        opt = ticker.option_chain(date)
        calls = opt.calls
        calls['expiry'] = date
        
        calls['days_to_expiry'] = (pd.to_datetime(date) - pd.Timestamp.today()).days
        all_calls.append(calls)
    
    df = pd.concat(all_calls)
    
    df = df[(df['strike'] > current_price * 0.8) & (df['strike'] < current_price * 1.2)]
    
    return df, current_price, expiries[:5]
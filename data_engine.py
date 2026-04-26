import yfinance as yf
import pandas as pd
import numpy as np

def get_real_options_data(ticker_symbol):
    """
    Fetches options data letting yfinance handle the session internally
    to avoid curl_cffi compatibility issues on Cloud servers.
    """
    
    ticker = yf.Ticker(ticker_symbol)
    
    try:
        expiries = ticker.options
        if not expiries:
            return None, None, None
        
        history = ticker.history(period="1d")
        if history.empty:
            return None, None, None
        S = history['Close'].iloc[-1]
        
        all_calls = []
        for date in expiries[:3]:
            opt = ticker.option_chain(date)
            calls = opt.calls
            calls['expiry'] = date
            calls['days_to_expiry'] = (pd.to_datetime(date) - pd.Timestamp.today()).days
            all_calls.append(calls)
        
        df = pd.concat(all_calls)
        df = df[(df['strike'] > S * 0.9) & (df['strike'] < S * 1.1)]
        
        return df, S, expiries[:3]
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
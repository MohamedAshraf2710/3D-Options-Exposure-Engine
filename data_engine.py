import yfinance as yf
import pandas as pd
import numpy as np
import requests

def get_real_options_data(ticker_symbol):
    """
    Fetches options data using a custom header to avoid API restrictions.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    
    ticker = yf.Ticker(ticker_symbol, session=session)
    
    try:
        expiries = ticker.options
        if not expiries:
            return None, None, None
        
        history = ticker.history(period="1d")
        if history.empty:
            return None, None, None
        S = history['Close'].iloc[-1]
        
        all_calls = []
       # We will only use the first 3 dates to ensure server stability
        for date in expiries[:3]:
            opt = ticker.option_chain(date)
            calls = opt.calls
            calls['expiry'] = date
            calls['days_to_expiry'] = (pd.to_datetime(date) - pd.Timestamp.today()).days
            all_calls.append(calls)
        
        df = pd.concat(all_calls)
       # Filtering data about the current price to focus on the most relevant contracts
        df = df[(df['strike'] > S * 0.9) & (df['strike'] < S * 1.1)]
        
        return df, S, expiries[:3]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None, None
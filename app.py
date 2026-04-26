import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from data_engine import get_real_options_data
from greeks_engine import calculate_gamma

# Page configuration for a wide-screen immersive experience
st.set_page_config(page_title="3D Options Surface Engine", layout="wide")

st.title("Real-Time 3D Options Exposure Engine")
st.markdown(f"**Engineering Lead:** Mohamed Ashraf | **Focus:** Quant Finance & AI")

# Sidebar for user configuration
st.sidebar.header("Market Configuration")
# --- Professional Ticker Selection ---
popular_tickers = ["NVDA", "AAPL", "TSLA", "AMD", "MSFT", "GOOGL", "AMZN", "META", "Custom"]

selected_asset = st.sidebar.selectbox("Select Asset", popular_tickers)

# Logic to handle custom ticker input
if selected_asset == "Custom":
    ticker_input = st.sidebar.text_input("Enter Ticker Symbol (e.g., NFLX)", "SPY")
else:
    ticker_input = selected_asset
risk_free_rate = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 5.0, 4.3) / 100

if st.button("Generate Real Surface"):
    with st.spinner(f"Computing risk surfaces for {ticker_input}..."):
        df, S, expiries = get_real_options_data(ticker_input)
        
        if df is None:
            st.error("No valid options data found. Please check the ticker symbol.")
        else:
            # Apply Black-Scholes model to calculate Gamma for each contract
            df['gamma'] = df.apply(lambda row: calculate_gamma(
                S=S, 
                K=row['strike'], 
                T=row['days_to_expiry']/365, 
                r=risk_free_rate, 
                sigma=row['impliedVolatility']
            ), axis=1)

            st.success(f"Successfully modeled {len(df)} contracts for {ticker_input}")
            # Pivot data and handle missing values for a smooth surface
            surface_data = df.pivot_table(values='gamma', index='days_to_expiry', columns='strike').interpolate(axis=1).fillna(0)
            
            X = surface_data.columns # Strikes
            Y = surface_data.index   # Days to Expiry
            Z = surface_data.values  # Gamma values

            # Construct the interactive 3D Surface using Plotly
            fig = go.Figure(data=[go.Surface(
                z=Z, x=X, y=Y, 
                colorscale='Viridis',
                hovertemplate='Strike: %{x}<br>Days: %{y}<br>Gamma: %{z:.4f}<extra></extra>'
            )])

            fig.update_layout(
                title=f"Live Gamma Surface: {ticker_input}",
                scene=dict(
                    xaxis_title='Strike Price',
                    yaxis_title='Days to Maturity',
                    zaxis_title='Gamma Exposure',
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=0.5)
                ),
                margin=dict(l=0, r=0, b=0, t=40),
                height=700
            )

            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed data table for transparency
            st.subheader("Quantitative Data Overview")
            st.write(df[['strike', 'expiry', 'impliedVolatility', 'gamma']].head(10))
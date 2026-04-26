#  3D Options Exposure Engine (Gamma Surface)

**Developed by:** [Mohamed Ashraf](https://github.com/MohamedAshraf2710)  
**Domain:** Financial Engineering | Quantitative Analysis | 3D Visualization

##  Project Overview
This engine provides a real-time 3D visualization of **Option Gamma Surfaces**. Unlike static models, this tool fetches live market data to calculate risk exposures using the **Black-Scholes-Merton** mathematical framework. It helps traders identify "Gamma Peaks"—areas where the underlying asset price is likely to experience high sensitivity or magnetic attraction.

##  Quantitative Framework
- **Model:** Black-Scholes-Merton (1973).
- **Metric:** Gamma ($\Gamma$) - The second-order derivative of the option price with respect to the underlying price.
- **Data Engine:** Asynchronous fetching of live Options Chains including Implied Volatility (IV).

##  Key Features
- **Live Market Injection:** Connects to Yahoo Finance for real-time Strike prices and IV.
- **Interactive 3D Rendering:** Built with `Plotly` to allow 360-degree rotation and inspection of risk clusters.
- **Dynamic Risk-Free Rate:** Adjustable BSM parameters via a sidebar dashboard.
- **Smart Data Interpolation:** Handles sparse market data to create a continuous and smooth risk surface.

##  Tech Stack
* **Mathematics:** Scipy (Normal Distribution functions)
* **API:** yfinance
* **UI:** Streamlit
* **Graphics:** Plotly (3D Mesh Geometry)
* **Data:** Pandas & NumPy

##  Installation
1. Clone: `git clone https://github.com/MohamedAshraf2710/3D-Options-Exposure-Engine.git`
2. Dependencies: `pip install streamlit yfinance scipy plotly pandas numpy`
3. Run: `streamlit run app.py`

## 🔍 How to Interpret the Surface
- **Gamma Peak (The Summit):** Indicates the strike price where the underlying asset's price sensitivity is highest. Large peaks often act as "magnets" for the stock price near expiration.
- **Time Decay (The Slope):** Observe how Gamma increases or decreases as we move from 60 days to 5 days until maturity.
- **Volatility Smile Effect:** See how Implied Volatility (IV) affects the curvature and height of the risk surface.


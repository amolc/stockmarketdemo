# get data for nse stock reliance using a python library
import yfinance as yf
import pandas as pd
import numpy as np

def get_reliance_data():
    """
    Fetches historical data for Reliance Industries (RELIANCE.NS) from Yahoo Finance.
    # """
    # print("--- Fetching Reliance Industries (NSE: RELIANCE) Data ---")
    
    # # RELIANCE.NS is the ticker symbol for Reliance on the National Stock Exchange of India
    ticker_symbol = "RELIANCE.NS"
    
    # # Initialize the Ticker object
    reliance = yf.Ticker(ticker_symbol)
    
    # # 1. Fetch historical market data (last 5 days)
    # print("\n1. Recent Historical Data (Last 5 Days):")
    hist = reliance.history(period="180d")
    print(hist[['Open', 'High', 'Low', 'Close', 'Volume']])
    

    # # generate the moving average using numpy 
    hist['MA9'] = hist['Close'].rolling(window=9).mean()
    hist['MA21'] = hist['Close'].rolling(window=21).mean()
    hist['uptrend'] = np.where(hist['Close'] > hist['MA21'], 1, 0)
    hist['upcross'] = np.where((hist['uptrend'] == 1) & (hist['uptrend'].shift(1) == 0), hist['Close'], 0)
    hist['downtrend'] = np.where(hist['Close'] < hist['MA21'], 1, 0)
    hist['downcross'] = np.where((hist['downtrend'] == 1) & (hist['downtrend'].shift(1) == 0), hist['Close'], 0)

    total = 0 

    for i in range(1, len(hist)):
        if hist['upcross'].iloc[i] != 0:
            start_price = hist['upcross'].iloc[i]
            print(f"Buy on {hist.index[i]} at {hist['upcross'].iloc[i]}")
        if hist['downcross'].iloc[i] != 0:
            print(f"Sell on {hist.index[i]} at {hist['downcross'].iloc[i]}")
            end_price = hist['downcross'].iloc[i]
            profit = end_price - start_price
            total += profit
            print(f"Profit: {end_price - start_price}")
            print(f"Profit %: {(end_price - start_price) / start_price * 100:.2f}%")
    print(f"Total Profit: {total}")
    print(f"Total Profit %: {(total / start_price) * 100:.2f}%")



    hist.to_csv("reliance.csv")
    # print("\n50-Day and 200-Day Moving Averages:")
    # print(hist[['Close', 'MA50', 'MA200']].tail())
    
    # plot plotly graph between close price and moving averages
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close Price'))
    # fig.add_trace(go.Scatter(x=hist.index, y=hist['MA9'], mode='lines', name='MA9'))
    # fig.add_trace(go.Scatter(x=hist.index, y=hist['MA21'], mode='lines', name='MA21'))
    fig.update_layout(title='Close Price and Moving Averages', xaxis_title='Date', yaxis_title='Price')
    
    
    # Save as HTML and show
    # output_path = "reliance_plot.html"
    # fig.write_html(output_path)
    # print(f"\nPlot saved to: {output_path}")
    fig.show()

    # # generate a csv file for the data
    # hist.to_csv("reliance_historical_data.csv")

    
    # 2. Fetch Stock Info (Company Profile, Sector, etc.)
    # Note: info can sometimes be slow or return empty if API is limited
    try:
        # info = reliance.info
        print(f"\n2. Company Info:")
        # print(f"Name: {info.get('longName')}")
        # print(f"Sector: {info.get('sector')}")
        # print(f"Current Price: {info.get('currentPrice')} {info.get('currency')}")
        # print(f"Market Cap: {info.get('marketCap')}")
    except Exception as e:
        print(f"\nCould not fetch detailed info: {e}")

    # 3. Fetch Dividends and Splits
    print("\n3. Recent Actions (Dividends/Splits):")
    # print(reliance.actions)

    # # 4. Fetch Quarterly Financials
    # print("\n4. Quarterly Financials (Snippet):")
    # financials = reliance.quarterly_financials
    # if not financials.empty:
    #     print(financials.iloc[:, :2]) # Show first two columns
    # else:
    #     print("Financials not available.")

if __name__ == "__main__":
    get_reliance_data()
import yfinance as yf

def get_top_stocks_nyse():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V"]  # Example top stocks
    stocks_data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            continue
        pct_change = ((hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]) * 100

        stocks_data.append({
            "symbol": ticker,
            "name": stock.info.get("shortName", ticker),
            "price": round(hist["Close"][-1], 2),
            "change": round(pct_change, 2)
        })

    # Sort by best performing
    stocks_data.sort(key=lambda x: x["change"], reverse=True)

    return stocks_data[:10]
    
# Example Indian stocks (NSE symbols)
def get_top_indian_stocks_nse():    
        tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "SBIN.NS", "KOTAKBANK.NS", "LT.NS"]
        stocks_data = []

        for ticker in tickers:  
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            if hist.empty:
                continue
            pct_change = ((hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]) * 100

            stocks_data.append({
                "symbol": ticker,
                "name": stock.info.get("shortName", ticker),
                "price": round(hist["Close"][-1], 2),
                "change": round(pct_change, 2)
            })

        stocks_data.sort(key=lambda x: x["change"], reverse=True)
        return stocks_data[:10]

# Example Indian stocks (BSE symbols)
def get_top_indian_stocks_bse():
    tickers = ["RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO", "BHARTIARTL.BO", "HINDUNILVR.BO", "SBIN.BO", "KOTAKBANK.BO", "LT.BO"]
    stocks_data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        if hist.empty:
            continue
        pct_change = ((hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]) * 100

        stocks_data.append({
            "symbol": ticker,
            "name": stock.info.get("shortName", ticker),
            "price": round(hist["Close"][-1], 2),
            "change": round(pct_change, 2)
        })

    stocks_data.sort(key=lambda x: x["change"], reverse=True)
    return stocks_data[:10]

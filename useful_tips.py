import yfinance as yf

def get_value_buys():
    """
    Returns value buys (low P/E ratio) using yfinance data.
    """
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V",
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "SBIN.NS", "KOTAKBANK.NS", "LT.NS",
        "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO", "BHARTIARTL.BO", "HINDUNILVR.BO", "SBIN.BO", "KOTAKBANK.BO", "LT.BO"
    ]
    stocks_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe_ratio = info.get("trailingPE")
        price = info.get("regularMarketPrice")
        name = info.get("shortName", ticker)
        if pe_ratio and pe_ratio > 0:
            stocks_data.append({
                "name": name,
                "symbol": ticker,
                "price": price,
                "pe_ratio": round(pe_ratio, 2)
            })
    stocks_data.sort(key=lambda x: x["pe_ratio"])
    return stocks_data[:10]

def get_top_growth_picks():
    """
    Returns top growth stocks (highest % price change over 1 year) from a combined list of NYSE, NSE, and BSE tickers.
    """
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V",
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "SBIN.NS", "KOTAKBANK.NS", "LT.NS",
        "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO", "BHARTIARTL.BO", "HINDUNILVR.BO", "SBIN.BO", "KOTAKBANK.BO", "LT.BO"
    ]
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

def get_hidden_gems():
    """
    Returns hidden gems (high growth, low market cap) using yfinance data.
    """
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V",
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "SBIN.NS", "KOTAKBANK.NS", "LT.NS",
        "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO", "BHARTIARTL.BO", "HINDUNILVR.BO", "SBIN.BO", "KOTAKBANK.BO", "LT.BO"
    ]
    stocks_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        info = stock.info
        market_cap = info.get("marketCap")
        name = info.get("shortName", ticker)
        if hist.empty or not market_cap:
            continue
        pct_change = ((hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]) * 100
        # Consider market cap below $5B as "hidden gem"
        if market_cap < 5e9 and pct_change > 0:
            stocks_data.append({
                "name": name,
                "symbol": ticker,
                "price": round(hist["Close"][-1], 2),
                "change": round(pct_change, 2),
                "market_cap": market_cap
            })
    stocks_data.sort(key=lambda x: x["change"], reverse=True)
    return stocks_data[:10]
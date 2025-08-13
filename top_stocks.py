import yfinance as yf
import pickle
import os
import time

CACHE_DIR = "cache"
CACHE_TIMEOUT = 60 * 60  # 1 hour

def cache_load(key):
    path = os.path.join(CACHE_DIR, key + ".pkl")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data, timestamp = pickle.load(f)
    if time.time() - timestamp > CACHE_TIMEOUT:
        return None
    return data

def cache_save(key, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, key + ".pkl")
    with open(path, "wb") as f:
        pickle.dump((data, time.time()), f)

def get_top_stocks_nyse():
    cache_key = "nyse"
    cached = cache_load(cache_key)
    if cached:
        return cached

    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V"]
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
    result = stocks_data[:10]
    cache_save(cache_key, result)
    return result

def get_top_indian_stocks_nse():
    cache_key = "nse"
    cached = cache_load(cache_key)
    if cached:
        return cached

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
    result = stocks_data[:10]
    cache_save(cache_key, result)
    return result

def get_top_indian_stocks_bse():
    cache_key = "bse"
    cached = cache_load(cache_key)
    if cached:
        return cached

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
    result = stocks_data[:10]
    cache_save(cache_key, result)
    return result

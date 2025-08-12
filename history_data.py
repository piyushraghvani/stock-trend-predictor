import yfinance as yf

def get_history_data(symbol):
    ticker = yf.Ticker(symbol)
    history_data = ticker.history(period="1y")
    if history_data.empty:
        history_data = None
    return history_data

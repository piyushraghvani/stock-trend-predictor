import yfinance as yf

stock = yf.Ticker("MRF.BO")

# Fetch historical market data for last six months
hist = stock.history(period="6mo")


# Display the historical data
print(hist.head())  # Display the first few rows of the historical data
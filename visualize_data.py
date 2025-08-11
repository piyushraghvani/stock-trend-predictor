import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Set stock and period
ticker = "AAPL"
start = "2023-01-01"
end = "2024-01-01"

# Fetch data
data = yf.download(ticker, start=start, end=end)

# Calculate moving averages
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

# Plot closing price and moving averages
plt.figure(figsize=(14, 6))
plt.plot(data["Close"], label="Close Price", color="blue")
plt.plot(data["MA20"], label="20-Day MA", color="orange")
plt.plot(data["MA50"], label="50-Day MA", color="green")
plt.title(f"{ticker} Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Optional: Volume
plt.figure(figsize=(14, 4))
plt.bar(data.index, data["Volume"], color="purple")
plt.title(f"{ticker} Trading Volume")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.tight_layout()
plt.show()
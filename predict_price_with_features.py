import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Download stock data
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

# Feature Engineering
data["SMA_5"] = data["Close"].rolling(window=5).mean()
data["EMA_5"] = data["Close"].ewm(span=5, adjust=False).mean()
data["Returns"] = data["Close"].pct_change()
delta = data["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data["RSI"] = 100 - (100 / (1 + rs))

# Previous day's close
data["Prev_Close"] = data["Close"].shift(1)

# Drop rows with NaN
data.dropna(inplace=True)

# Features and target
features = ["Prev_Close", "SMA_5", "EMA_5", "RSI", "Returns", "Volume"]
X = data[features]
y = data["Close"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Plotting
plt.figure(figsize=(14, 6))
plt.plot(y_test.index, y_test, label="Actual", color="blue")
plt.plot(y_test.index, y_pred, label="Predicted", color="orange")
plt.title(f"{ticker} Stock Price Prediction with Indicators")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

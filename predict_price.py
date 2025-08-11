import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Fetch stock data
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")
data = data[["Close"]].dropna()

# Create a feature: Previous day's closing price
data["Prev_Close"] = data["Close"].shift(1)
data.dropna(inplace=True)

# Features (X) and Labels (y)
X = data[["Prev_Close"]]
y = data["Close"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Plot results
plt.figure(figsize=(14, 6))
plt.plot(y_test.index, y_test, label="Actual", color="blue")
plt.plot(y_test.index, y_pred, label="Predicted", color="orange")
plt.title(f"{ticker} Price Prediction (Linear Regression)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

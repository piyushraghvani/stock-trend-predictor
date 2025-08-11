import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import os

def predict_stock(ticker):
    # Step 1: Fetch data
    df = yf.download(ticker, start="2025-01-01", end="2025-01-01")
    df = df[['Close']].dropna()

    # Step 2: Preprocess
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)

    sequence_length = 60
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i])

    X, y = np.array(X), np.array(y)

    # Step 3: Train/test split
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Step 4: LSTM model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # Step 5: Prediction
    predicted = model.predict(X_test)
    predicted = scaler.inverse_transform(predicted)
    actual = scaler.inverse_transform(y_test)

    # Step 6: Save plot
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(12, 6))
    plt.plot(actual, label="Actual")
    plt.plot(predicted, label="Predicted")
    plt.title(f"{ticker} Stock Price Prediction")
    plt.legend()
    path = f"static/{ticker}_plot.png"
    plt.savefig(path)
    plt.close()

    # Step 7: Decision Suggestion
    last_real = actual[-1][0]
    last_pred = predicted[-1][0]
    suggestion = "Up ✅" if last_pred > last_real else "Down ❌"

    return suggestion, path

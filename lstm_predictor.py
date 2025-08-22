# lstm_predictor.py

import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler


def predict_stock(ticker):
    try:
        # Fetch stock data (max available history)
        data = yf.download(ticker, period="max", interval="1d")
        if data.empty or "Close" not in data.columns:
            return {
                "prediction": None,
                "confidence": None,
                "chart_json": None,
                "last_price": None,
                "predicted_price": None,
                "volatility": None,
                "trend": None,
                "support": None,
                "resistance": None,
                "explanation": "No data available.",
                "error": f"No data found for {ticker}"
            }

        close_prices = data["Close"].dropna().values.reshape(-1, 1)
        last_price = float(close_prices[-1][0])

        # Scale prices
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(close_prices)

        # Sequence length (fallback to shorter if not enough history)
        seq_len = 60 if len(scaled) > 60 else len(scaled) - 1
        if seq_len < 2:
            return {
                "prediction": None,
                "confidence": None,
                "chart_json": None,
                "last_price": float(last_price),
                "predicted_price": None,
                "volatility": None,
                "trend": None,
                "support": None,
                "resistance": None,
                "explanation": "Not enough historical data to build model.",
                "error": "Not enough historical data."
            }

        # Prepare training data
        X, y = [], []
        for i in range(seq_len, len(scaled)):
            X.append(scaled[i - seq_len:i, 0])
            y.append(scaled[i, 0])
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Build LSTM model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(X, y, epochs=3, batch_size=16, verbose=0)

        # Predict next price
        last_seq = scaled[-seq_len:]
        X_test = np.reshape(last_seq, (1, seq_len, 1))
        pred_scaled = model.predict(X_test, verbose=0)

        # Ensure numpy array before inverse transform
        pred_scaled = np.array(pred_scaled).reshape(-1, 1)
        predicted_price = float(scaler.inverse_transform(pred_scaled)[0][0])

        # Direction
        if predicted_price > last_price:
            prediction = "Up"
        elif predicted_price < last_price:
            prediction = "Down"
        else:
            prediction = "Stable"

        # Confidence interval (±2%)
        confidence = round(abs((predicted_price - last_price) / last_price) * 100, 2)
        confidence_low = round(predicted_price * 0.98, 2)
        confidence_high = round(predicted_price * 1.02, 2)

        # Volatility
        returns = data["Close"].pct_change().dropna()
        volatility = float(np.std(returns) * np.sqrt(252))
        volatility_label = "High Risk" if volatility > 0.3 else "Stable"

        # Trend (force scalars)
        short_ma = float(data["Close"].rolling(window=7).mean().iloc[-1])
        long_ma = float(data["Close"].rolling(window=30).mean().iloc[-1])
        if np.isnan(short_ma) or np.isnan(long_ma):
            trend = "Insufficient Data"
        elif short_ma > long_ma:
            trend = "Short-term Bullish"
        else:
            trend = "Short-term Bearish"

        # Support & resistance (convert to scalar floats)
        support = float(round(data["Close"].tail(30).min(), 2))
        resistance = float(round(data["Close"].tail(30).max(), 2))

        # Plotly chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data["Close"],
                                 mode='lines', name='Historical Price'))
        fig.add_hline(y=last_price, line_dash="dot", line_color="blue",
                      annotation_text=f"Last: {last_price}")
        fig.add_hline(y=predicted_price, line_dash="dot",
                      line_color="green" if prediction == "Up" else "red",
                      annotation_text=f"Predicted: {predicted_price}")
        fig.update_layout(title=f"{ticker.upper()} Stock Prediction",
                          xaxis_title="Date", yaxis_title="Price")

        chart_json = fig.to_json()

        # Explanation
        explanation = (
            f"Prediction is based on the last {seq_len} days. "
            f"The model found a {'rising' if prediction == 'Up' else 'falling' if prediction == 'Down' else 'neutral'} "
            f"pattern in recent prices. Volatility suggests {volatility_label}. "
            f"Trend is {trend}. Support at {support}, resistance at {resistance}."
        )

        return {
            "prediction": prediction,
            "confidence": confidence,
            "confidence_low": confidence_low,
            "confidence_high": confidence_high,
            "chart_json": chart_json,
            "last_price": round(last_price, 2),
            "predicted_price": round(predicted_price, 2),
            "volatility": volatility_label,
            "trend": trend,
            "support": support,
            "resistance": resistance,
            "explanation": explanation,
            "error": None
        }

    except Exception as e:
        return {
            "prediction": None,
            "confidence": None,
            "chart_json": None,
            "last_price": None,
            "predicted_price": None,
            "volatility": None,
            "trend": None,
            "support": None,
            "resistance": None,
            "explanation": None,
            "error": str(e)
        }

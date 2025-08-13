# from flask import Flask, render_template, request
# import yfinance as yf
# import matplotlib.pyplot as plt
# import pandas as pd
# from statsmodels.tsa.holtwinters import ExponentialSmoothing

# def predict_stock(ticker):
#     stock = yf.download(ticker, period="1y", interval="1d")
#     stock.reset_index(inplace=True)

#     df = stock[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
#     df.set_index('ds', inplace=True)

#     # Use Exponential Smoothing (Holt-Winters)
#     model = ExponentialSmoothing(df['y'], trend='add', seasonal=None)
#     fit = model.fit()

#     # Forecast next 30 days
#     forecast = fit.forecast(30)
#     forecast_index = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')
#     forecast_df = pd.DataFrame({'ds': forecast_index, 'yhat': forecast.values})

#     plt.figure(figsize=(8, 4))
#     plt.plot(df.index, df['y'], label="Historical", color="blue")
#     plt.plot(forecast_df['ds'], forecast_df['yhat'], label="Prediction", color="orange")
#     plt.legend()
#     plt.grid(True)
#     plt.title(f"{ticker} - 30 Day Prediction")
#     plt.savefig("static/prediction_chart.png")
#     plt.close()

#     return {
#         "current_price": df['y'].iloc[-1],
#         "predicted_price": forecast.values[-1],
#         "forecast": forecast_df
#     }
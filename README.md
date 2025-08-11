
# Stock Trend Predictor

This application fetches historical stock data, applies machine learning models (including LSTM), and predicts future price trends to assist users in making investment decisions. It also provides data visualization for selected stocks.

## Prerequisites

- Python 3.8 or higher
- Git
- Internet connection (required for fetching stock data)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd stock-trend-predictor
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   *(On Mac/Linux, use `source venv/bin/activate`)*

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```powershell
   python app.py
   ```

## Project Structure

```
stock-trend-predictor/
│
├── app.py                        # Main application (entry point)
├── fetch_data.py                 # Fetches historical stock data using yfinance
├── lstm_predictor.py             # LSTM model for stock price prediction
├── predict_price.py              # Predicts stock price using basic features
├── predict_price_with_features.py# Predicts price using additional features
├── visualize_data.py             # Data visualization utilities
├── static/                       # Contains generated plots (PNG images)
├── Templates/                    # HTML templates for the web app
└── README.md                     # Project documentation
```

## Usage

1. Open the app in your browser (if running as a web app).
2. Select a stock symbol to view historical data, predictions, and visualizations.
3. Review generated plots in the `static/` folder.

## Notes

- The application uses [yfinance](https://github.com/ranaroussi/yfinance) for data fetching.
- Plots are saved in the `static/` directory and displayed via the web interface.
- HTML templates are located in the `Templates/` folder.

## License

MIT License
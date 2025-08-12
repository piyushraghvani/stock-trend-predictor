from flask import Flask, render_template, request
from lstm_predictor import predict_stock

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"]
        prediction, chart_path = predict_stock(ticker)
        return render_template("index.html", prediction=prediction, chart=chart_path, ticker=ticker)
    return render_template("index.html")

#create new route for getting top 10 stocks
@app.route("/top_stocks", methods=["GET"])
def top_stocks():
    # Logic to get top 10 stocks with name symbol price and change
    top_stocks = [
        {"name": "Apple Inc.", "symbol": "AAPL", "price": 150.00, "change": "+1.5%"},
        {"name": "Microsoft Corp.", "symbol": "MSFT", "price": 250.00, "change": "+2.0%"},
        {"name": "Alphabet Inc.", "symbol": "GOOGL", "price": 2800.00, "change": "+1.2%"},
        {"name": "Amazon.com Inc.", "symbol": "AMZN", "price": 3400.00, "change": "+1.8%"},
        {"name": "Tesla Inc.", "symbol": "TSLA", "price": 700.00, "change": "+2.5%"},
        {"name": "Meta Platforms Inc.", "symbol": "FB", "price": 350.00, "change": "+1.0%"},
        {"name": "Berkshire Hathaway Inc.", "symbol": "BRK.A", "price": 420000.00, "change": "+0.5%"},
        {"name": "Johnson & Johnson", "symbol": "JNJ", "price": 170.00, "change": "+0.8%"},
        {"name": "Visa Inc.", "symbol": "V", "price": 220.00, "change": "+1.3%"},
        {"name": "Walmart Inc.", "symbol": "WMT", "price": 140.00, "change": "+0.6%"},
    ]
    return render_template("top_stocks.html", stocks=top_stocks)


if __name__ == "__main__":
    app.run(debug=True)

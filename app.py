from flask import Flask, render_template, request, redirect, url_for
from top_stocks import get_top_stocks_nyse
from top_stocks import get_top_indian_stocks_nse
from top_stocks import get_top_indian_stocks_bse
from history_data import get_history_data
# from lstm_predictor import predict_stock  # Assuming you have a predict function in predict.py
from useful_tips import get_top_growth_picks, get_value_buys, get_hidden_gems
from sentiment_analysis_blob import get_news_and_sentiment

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    chart = None
    ticker = None

    # Always fetch stock data here
    top_stocks_nyse = get_top_stocks_nyse()
    top_stocks_bse = get_top_indian_stocks_bse()
    top_stocks_nse = get_top_indian_stocks_nse()

    if request.method == "POST":
        ticker = request.form.get("ticker")
        prediction, chart = predict_stock(ticker)

    return render_template(
        "index.html",
        prediction=prediction,
        chart=chart,
        ticker=ticker,
        top_stocks_nyse=top_stocks_nyse,
        top_stocks_bse=top_stocks_bse,
        top_stocks_nse=top_stocks_nse
    )


@app.route('/history', methods=['GET', 'POST'])
def history():
    symbol = request.args.get("symbol", "AAPL")
    page = int(request.args.get("page", 1))
    page_size = 20
    history_data = get_history_data(symbol, page, page_size)
    return render_template("history.html", symbol=symbol, history_data=history_data)

@app.route("/tips")
def tips():
    tips = get_useful_tips()
    return render_template("tips.html", tips=tips)

@app.route("/predict_stock", methods=["GET", "POST"])
def predict_stock_route():
    prediction = None
    chart = None
    ticker = None

    if request.method == "POST":
        ticker = request.form.get("ticker")
        prediction, chart = predict_stock(ticker)

    return render_template("predict_stock.html", prediction=prediction, chart=chart, ticker=ticker)

@app.route("/top_stocks")
def top_stocks():
    top_stocks_nyse = get_top_stocks_nyse()
    top_stocks_nse = get_top_indian_stocks_nse()
    top_stocks_bse = get_top_indian_stocks_bse()
    return render_template("top_stocks.html", top_stocks_nyse=top_stocks_nyse, top_stocks_nse=top_stocks_nse, top_stocks_bse=top_stocks_bse)


@app.route("/dashboard")
def dashboard():
    top_growth = get_top_growth_picks()
    value_buys = get_value_buys()
    hidden_gems = get_hidden_gems()
    return render_template("dashboard.html", top_growth=top_growth, value_buys=value_buys, hidden_gems=hidden_gems)

@app.route("/sentiment_analysis", methods=["GET", "POST"])
def sentiment_analysis():
    stock_name = 'None'
    overall_sentiment = None
    news_list = []

    if request.method == "POST":
        stock_name = request.form.get("symbol")
        overall_sentiment, news_list = get_news_and_sentiment(stock_name)

    return render_template("sentiment_analysis.html", stock_name=stock_name, overall_sentiment=overall_sentiment, news_list=news_list)

if __name__ == "__main__":
    app.run(debug=True)

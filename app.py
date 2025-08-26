from flask import Flask, render_template, request, redirect, url_for
from top_stocks import get_top_stocks_nyse
from top_stocks import get_top_indian_stocks_nse
from top_stocks import get_top_indian_stocks_bse
from history_data import get_history_data
from lstm_predictor import predict_stock  # Assuming you have a predict function in predict.py
from useful_tips import get_top_growth_picks, get_value_buys, get_hidden_gems
#from ask_bot import ask_bot  # Assuming you have an AI bot function in ai_bot.py
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


@app.route("/history", methods=["GET", "POST"])
def history():
    symbol = request.args.get("symbol") or request.form.get("symbol")
    page = int(request.args.get("page", 1))

    history_data = None
    summary = None
    chart_json = None

    if symbol:
        result = get_history_data(symbol, page=page, page_size=50)
        history_data = result
        summary = result.get("summary")
        chart_json = result.get("chart_json")

    return render_template(
        "history.html",
        symbol=symbol,
        history_data=history_data,
        summary=summary,
        chart_json=chart_json
    )

@app.route("/tips")
def tips():
    tips = get_useful_tips()
    return render_template("tips.html", tips=tips)

@app.route("/predict_stock", methods=["GET", "POST"])
def predict_stock_route():
    if request.method == "POST":
        ticker = request.form.get("ticker")
        result = predict_stock(ticker)

        # Convert pandas/numpy objects to native Python types for template safety
        def to_native(val):
            import numpy as np
            import pandas as pd
            if isinstance(val, (np.generic, np.ndarray)):
                return val.item() if val.size == 1 else val.tolist()
            if isinstance(val, pd.Series):
                return val.tolist()
            return val

        confidence_range = [to_native(result.get("confidence_low")), to_native(result.get("confidence_high"))]

        return render_template(
            "predict_stock.html",
            ticker=ticker,
            prediction=to_native(result.get("prediction")),
            confidence=to_native(result.get("confidence")),
            chart=None,  # No static chart, use interactive
            last_price=to_native(result.get("last_price")),
            predicted_price=to_native(result.get("predicted_price")),
            volatility=to_native(result.get("volatility")),
            trend=to_native(result.get("trend")),
            support=to_native(result.get("support")),
            resistance=to_native(result.get("resistance")),
            explanation=to_native(result.get("explanation")),
            confidence_range=confidence_range,
            error=result.get("error"),
            chart_json=result.get("chart_json")
        )

    return render_template("predict_stock.html")

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

@app.route("/ai_bot")
def aibot():
    return render_template("ai_bot.html")

@app.route("/ask_bot", methods=["POST"])
def ask_bot_route():
    user_query = request.json.get("query")
    # answer = ask_bot(user_query)
    # return {"answer": answer}
    return render_template("ai_bot.html")
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

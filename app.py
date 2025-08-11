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

if __name__ == "__main__":
    app.run(debug=True)

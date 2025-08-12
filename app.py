from flask import Flask, render_template, request, redirect, url_for
from top_stocks import get_top_stocks_nyse
from top_stocks import get_top_indian_stocks_nse
from top_stocks import get_top_indian_stocks_bse
from useful_tips import get_useful_tips
from history_data import get_history_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        symbol = request.form['symbol']
        return redirect(url_for('history', symbol=symbol))

    symbol = request.args.get('symbol')
    history_data = None
    if symbol:
        history_data = get_history_data(symbol)
    return render_template('history.html', history_data=history_data, stock_symbol=symbol)

@app.route("/tips")
def tips():
    tips = get_useful_tips()
    return render_template("tips.html", tips=tips)

@app.route("/top_stocks")
def top_stocks():
    top_stocks_nyse = get_top_stocks_nyse()
    top_stocks_nse = get_top_indian_stocks_nse()
    top_stocks_bse = get_top_indian_stocks_bse()
    return render_template("top_stocks.html", top_stocks_nyse=top_stocks_nyse, top_stocks_nse=top_stocks_nse, top_stocks_bse=top_stocks_bse)

if __name__ == "__main__":
    app.run(debug=True)

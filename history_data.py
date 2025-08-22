import yfinance as yf
from math import ceil
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json

def get_history_data(symbol, page=1, page_size=50, sort_desc=True):
    ticker = yf.Ticker(symbol)
    history_data = ticker.history(period="1y")

    if history_data is not None and not history_data.empty:
        history_data = history_data.reset_index()
        history_data = history_data.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })

        # Sort by date
        history_data = history_data.sort_values(by="date", ascending=not sort_desc)

        records = history_data[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict(orient='records')
        total = len(records)

        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated = records[start:end]

        # ---- Summary Metrics ----
        latest_close = round(history_data['close'].iloc[-1], 2)
        return_pct = round(((history_data['close'].iloc[-1] / history_data['close'].iloc[0]) - 1) * 100, 2)
        highest = round(history_data['high'].max(), 2)
        lowest = round(history_data['low'].min(), 2)

        summary = {
            "latest_close": latest_close,
            "return_pct": return_pct,
            "highest": highest,
            "lowest": lowest
        }

        # ---- Plotly Chart ----
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history_data['date'], 
            y=history_data['close'],
            mode='lines',
            name='Close Price'
        ))
        fig.update_layout(
            title=f"{symbol.upper()} Stock Performance (1Y)",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            height=400
        )
        chart_json = json.dumps(fig, cls=PlotlyJSONEncoder)
        
        return {
            "data": paginated,
            "page": page,
            "page_size": page_size,
            "total_pages": ceil(total / page_size),
            "total_items": total,
            "start_date": history_data['date'].min().strftime("%Y-%m-%d"),
            "end_date": history_data['date'].max().strftime("%Y-%m-%d"),
            "summary": summary,
            "chart_json": chart_json
        }

    return {
        "data": [],
        "page": page,
        "page_size": page_size,
        "total_pages": 0,
        "total_items": 0,
        "start_date": None,
        "end_date": None,
        "summary": None,
        "chart_json": None
    }

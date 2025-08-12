import yfinance as yf
from math import ceil

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

        return {
            "data": paginated,
            "page": page,
            "page_size": page_size,
            "total_pages": ceil(total / page_size),
            "total_items": total,
            "start_date": history_data['date'].min().strftime("%Y-%m-%d"),
            "end_date": history_data['date'].max().strftime("%Y-%m-%d")
        }

    return {
        "data": [],
        "page": page,
        "page_size": page_size,
        "total_pages": 0,
        "total_items": 0,
        "start_date": None,
        "end_date": None
    }

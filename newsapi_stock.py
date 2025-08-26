import requests
import pandas as pd
import yfinance as yf
from datetime import datetime



def fetch_news_headlines(stock_symbol, from_date, to_date, api_key):
    news_url = (
        'https://newsapi.org/v2/everything?'
        f'q={stock_symbol}&'
        f'from={from_date}&'
        f'to={to_date}&'
        'sortBy=publishedAt&'
        f'apiKey={api_key}'
    )
    response = requests.get(news_url)
    data = response.json()
    if 'articles' not in data:
        print('Error: "articles" key not found in NewsAPI response.')
        return [], []
    headlines = [article['title'] for article in data['articles']]
    dates = [article['publishedAt'][:10] for article in data['articles']]
    return headlines, dates





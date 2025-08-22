dates = []

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_yahoo_finance_headlines(stock_symbol):
    url = f"https://finance.yahoo.com/quote/{stock_symbol}/news?p={stock_symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    dates = []
    source = "Yahoo Finance"
    for item in soup.find_all('li', {'class': 'js-stream-content'}):
        headline_tag = item.find('h3')
        date_tag = item.find('span', {'class': 'C(#959595) Fz(11px) D(ib) Mb(6px)'})
        if headline_tag and date_tag:
            headlines.append(headline_tag.text.strip())
            # Try to parse the date, fallback to today if not found
            try:
                date = date_tag.text.strip()
                # Yahoo Finance often shows relative dates (e.g., '2 hours ago'), so use today for demo
                dates.append(datetime.today().date())
            except:
                dates.append(datetime.today().date())
    return headlines, dates, source

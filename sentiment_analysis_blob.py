
# from textblob import TextBlob
# import pandas as pd
# import matplotlib.pyplot as plt
# import yfinance as yf
# # from sklearn.model_selection import train_test_split
# # from sklearn.linear_model import LinearRegression
# # from sklearn.metrics import mean_absolute_error

# def get_sentiment(text):
#     blob = TextBlob(text)
#     return blob.sentiment.polarity

# def categorize_sentiment(polarity):
#     if polarity > 0:
#         return 'Positive'
#     elif polarity < 0:
#         return 'Negative'
#     else:
#         return 'Neutral'

# if __name__ == "__main__":




#     # Import fetch_yahoo_finance_headlines from yahoo_finance_news_scrape
#     from yahoo_finance_news_scrape import fetch_yahoo_finance_headlines

#     # Fetch NewsAPI headlines and dates
#     from newsapi_stock import fetch_news_headlines
#     API_KEY = '9bdfba7f8a9540f08e48c564f4512c2f'  # Replace with your NewsAPI key
#     stock_symbol = 'AAPL'
#     from_date = '2025-07-19'
#     to_date = '2025-08-19'
#     headlines, dates = fetch_news_headlines(stock_symbol, from_date, to_date, API_KEY)

#     # Fetch Yahoo Finance headlines and dates
#     yahoo_headlines, yahoo_dates = fetch_yahoo_finance_headlines(stock_symbol)

#     # Combine NewsAPI and Yahoo Finance results
#     all_headlines = headlines + yahoo_headlines
#     all_dates = list(dates) + list(yahoo_dates)

#     financial_texts = {
#         'headline': all_headlines,
#         'date': all_dates
#     }
#     print('Sample financial texts:', financial_texts)
#     df = pd.DataFrame(financial_texts)
#     df['date'] = pd.to_datetime(df['date']).dt.date
#     df['polarity'] = df['headline'].apply(get_sentiment)
#     overall_sentiment = df['polarity'].apply(categorize_sentiment)


#     # Plot sentiment distribution
#     sentiment_counts = overall_sentiment.value_counts()
#     plt.figure(figsize=(6,4))
#     plt.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'blue'])
#     plt.title('Sentiment Distribution of Financial News Headlines')
#     plt.xlabel('Sentiment')
#     plt.ylabel('Number of Headlines')
#     plt.show()

#     # Commented out: rest of the code for stock analysis and regression
#     # ...existing code...




# # # Define the stock symbol (e.g., Apple - AAPL)
# # stock_symbol = "AAPL"

# # # Fetch historical stock data for the last 90 days
# # stock_data =yf.download(stock_symbol, start=from_date, end=to_date, interval='1d')

# # # Reset index so that Date becomes a column
# # stock_data = stock_data.reset_index()


# # # Convert the 'Date' column to match the news sentiment data
# # stock_data['Date'] = stock_data['Date'].dt.date


# # # Flatten columns to single level (use first level, e.g., 'Date', 'Close', ...)
# # stock_data.columns = stock_data.columns.get_level_values(0)


# # # Shift sentiment dates by one day to match tomorrow's stock movement
# # df['date'] = pd.to_datetime(df['date']) + pd.Timedelta(days=1)
# # df['date'] = df['date'].dt.date


# # # Merge the stock data with sentiment data
# # merged_df = pd.merge(stock_data, df, left_on='Date', right_on='date', how='inner')


# # # Drop unnecessary columns for a cleaner DataFrame
# # merged_df = merged_df[['Date', 'Close', 'polarity', 'sentiment']]


# # # Print columns to debug merge issue
# # # print('stock_data columns:', stock_data.columns)

# # # Display the merged DataFrame
# # # print(merged_df.head())

# # # Define the features (X) and target (y)
# # X = merged_df[['polarity']]  # Sentiment polarity
# # y = merged_df['Close']  # Stock closing prices

# # # Split the data into training and testing sets
# # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # # Train the linear regression model
# # model = LinearRegression()
# # model.fit(X_train, y_train)

# # # Make predictions on the test data
# # y_pred = model.predict(X_test)

# # # Calculate the Mean Absolute Error (MAE) to evaluate the model
# # mae = mean_absolute_error(y_test, y_pred)
# # # print(f"Mean Absolute Error: {mae}")

# # # Plot actual vs predicted stock prices
# # plt.scatter(y_test, y_pred)
# # plt.xlabel("Actual Prices")
# # plt.ylabel("Predicted Prices")
# # plt.title("Actual vs Predicted Stock Prices")
# # plt.show()

from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def categorize_sentiment(polarity):
    if polarity > 0.2:
        return 'Bullish'
    elif polarity < -0.2:
        return 'Bearish'
    else:
        return 'Neutral'

def build_news_list(df):
    """
    Returns a list of dicts: [{'title': ..., 'date': ..., 'sentiment': ...}, ...]
    """
    news_list = []
    for _, row in df.iterrows():
        news_list.append({
            "title": row['headline'],
            "date": row['date'],
            "sentiment": row['polarity'],
            "source": row.get('source', 'Unknown')  # Add source if available
        })
    return news_list

def get_overall_sentiment(df):
    """
    Returns overall sentiment string for the DataFrame.
    """
    if df['polarity'].empty:
        return "N/A"
    avg = df['polarity'].mean()
    return categorize_sentiment(avg)

def get_news_and_sentiment(stock_name):
    from yahoo_finance_news_scrape import fetch_yahoo_finance_headlines
    from newsapi_stock import fetch_news_headlines
    API_KEY = '9bdfba7f8a9540f08e48c564f4512c2f'  # Replace with your NewsAPI key
    stock_symbol = stock_name
    to_date = datetime.today()
    from_date = to_date - timedelta(days=7)

    # Get news headlines and dates
    headlines, dates = fetch_news_headlines(stock_symbol, from_date, to_date, API_KEY)
    yahoo_headlines, yahoo_dates, yahoo_source = fetch_yahoo_finance_headlines(stock_symbol)

    # Combine all news
    all_headlines = headlines + yahoo_headlines
    all_dates = list(dates) + list(yahoo_dates)
    all_sources = ['Unknown'] * len(headlines) + [yahoo_source] * len(yahoo_headlines)

    df = pd.DataFrame({'headline': all_headlines, 'date': all_dates,'source':all_sources})
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['polarity'] = df['headline'].apply(get_sentiment)

    news_list = build_news_list(df)
    overall_sentiment = get_overall_sentiment(df)

    return overall_sentiment, news_list
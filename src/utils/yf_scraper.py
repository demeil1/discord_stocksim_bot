import yfinance as yf

def scrape(ticker):

    try:
        # create a ticker object for the stock you want to retrieve data for
        ticker = yf.Ticker(ticker)

        # get the real-time stock price
        current_price = ticker.history(period="1d")["Close"].iloc[0]

        return current_price
    except Exception as e:
        print(e) # remove
        return None

def getValue(tickers):

    prices = [scrape(ticker) for ticker in tickers]
    if len(prices) == 1:
        return prices[0]
    return prices

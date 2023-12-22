import yfinance as yf
from scipy.stats import norm
import numpy as np
from datetime import datetime, timedelta

def scrape(ticker):
    try:
        # create a ticker object for the stock you want to retrieve data for
        ticker = yf.Ticker(ticker)

        # get the real-time stock price
        current_price = ticker.history(period="1d")["Close"].iloc[0]

        return current_price
    except:
        return None

def getValue(tickers):
    return [scrape(ticker) for ticker in tickers]

def calculateOptionPremium(ticker, strike_price, expiration_days, interest_rate):
    try:
        # Determine the start and end dates dynamically
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

        # Get historical stock prices
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Calculate historical daily returns
        daily_returns = stock_data['Close'].pct_change().dropna()

        # Calculate annualized volatility
        annualized_volatility = np.std(daily_returns) * np.sqrt(252)

        # Calculate d1 and d2 for the Black-Scholes formula
        d1 = (np.log(stock_data['Close'].iloc[-1] / strike_price) + (interest_rate + (annualized_volatility ** 2) / 2) * expiration_days) / (annualized_volatility * np.sqrt(expiration_days))
        d2 = d1 - annualized_volatility * np.sqrt(expiration_days)

        # Use Black-Scholes formula to calculate the call option premium
        option_premium = stock_data['Close'].iloc[-1] * norm.cdf(d1) - strike_price * np.exp(-interest_rate * expiration_days / 252) * norm.cdf(d2)

        return option_premium
    except:
        return None


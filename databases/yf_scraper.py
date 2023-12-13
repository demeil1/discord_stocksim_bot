import time # remove
import asyncio
import yfinance as yf

async def scrape(ticker):

    try:
        # Create a Tickerdd object for the stock you want to retrieve data for
        ticker = yf.Ticker(ticker)

        # Get the real-time stock price
        current_price = ticker.history(period="1d")["Close"].iloc[0]

        return current_price
    except:
        return None

async def getValue(tickers):

    tasks = [scrape(ticker) for ticker in tickers]
    prices = await asyncio.gather(*tasks)
    # results = zip(tickers, prices)
    return prices
   
# def nascrape(ticker):
#
#     try:
#         # Create a Tickerdd object for the stock you want to retrieve data for
#         ticker = yf.Ticker(ticker)
#
#         # Get the real-time stock price
#         current_price = ticker.history(period="1d")["Close"].iloc[0]
#
#         return current_price
#     except:
#         return None
#
# def nagetValue(tickers):
#
#     prices = [nascrape(ticker) for ticker in tickers]
#     return prices
#
# async def main():
#     t_old = time.time()
#     v = await getValue(['AAPL'])
#     t_new = time.time()
#     print(v, t_new - t_old)
#
#     t_old = time.time()
#     v = await getValue(['AAPL', "MSFT", "GOOG", "BRK-B", "BRK-A", "AMZN" "sgkjs"])
#     t_new = time.time()
#     print(v, t_new - t_old)
#
#     t_old = time.time()
#     v = nagetValue(['AAPL'])
#     t_new = time.time()
#     print(v, t_new - t_old)
#
#     t_old = time.time()
#     v = await getValue(['AAPL', "MSFT", "GOOG", "BRK-B", "BRK-A", "AMZN" "sgkjs"])
#     t_new = time.time()
#     print(v, t_new - t_old)


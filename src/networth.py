from .utils.yf_scraper import getValue
from .tables.users_table import queryUserBalance
from .tables.stocks_table import queryDistinctUserStock, queryUserStockAmount
from .tables.shorts_table import queryUserShorts
from .tables.options_table import queryUserOptions


def calculateUserNetWorth(user_id):
    networth = queryUserBalance(user_id)

    distinct_stocks = queryDistinctUserStock(user_id)
    user_stocks = []
    if distinct_stocks:
        user_stocks = [ticker[0] for ticker in distinct_stocks]
    if user_stocks:
        stock_shares = []
        for stock in user_stocks:
            stock_shares.append(queryUserStockAmount(user_id, stock))
        share_values = getValue(user_stocks)

        stock_share_value_zip = zip(user_stocks, stock_shares, share_values)
        for tkr, ns, val in stock_share_value_zip:
            networth += ns * val

    user_shorts = queryUserShorts(user_id)
    if user_shorts:
        TICKER = 2
        NUM_SHARES = 3
        INITIAL_PRICE = 4
        tickers = [transac[TICKER] for transac in user_shorts]
        share_values = getValue(tickers)
        for short in range(len(user_shorts)):
            networth += (
                user_shorts[short][INITIAL_PRICE] - share_values[short]
            ) * user_shorts[short][NUM_SHARES]

    user_options = queryUserOptions(user_id)
    if user_options:
        TICKER = 2
        NUM_SHARES = 3
        STRIKE_PRICE = 4
        PREMIUM = 5
        TYPE = 7
        tickers = [transac[TICKER] for transac in user_options]
        share_values = getValue(tickers)
        for option in range(len(user_options)):
            if user_options[option][TYPE].lower() == "call":
                networth += (
                    (share_values[option] - user_options[option][STRIKE_PRICE])
                    * user_options[option][NUM_SHARES]
                ) - user_options[option][PREMIUM]
            else:
                networth += (
                    (user_options[option][STRIKE_PRICE] - share_values[option])
                    * user_options[option][NUM_SHARES]
                ) - user_options[option][PREMIUM]
    return networth

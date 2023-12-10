from databases.users_table import queryUserBalance
from databases.yf_scraper import getValue
from databases.stocks_table import queryDistinctUserStock, queryUserStockAmount
from databases.shorts_table import queryUserShorts

async def calculateUserNetWorth(user_id):

    networth = queryUserBalance(user_id)

    user_stocks = queryDistinctUserStock(user_id)
    if user_stocks:
        stock_shares = []
        for stock in user_stocks:
            stock_shares.append(queryUserStockAmount(user_id, stock))
        share_values = await getValue(user_stocks)

        stock_share_value_zip = zip(user_stocks, stock_shares, share_values)
        for tkr, ns, val in stock_share_value_zip:
            networth += (ns * val)
    
    user_shorts = queryUserShorts(user_id) 
    if user_shorts:
        TICKER = 2
        NUM_SHARES = 3
        INITIAL_PRICE = 4
            
        tickers = [transac[TICKER] for transac in user_shorts]
        share_values = await getValue(tickers)
        for short in range(len(user_shorts)):
            networth += ((user_shorts[short][INITIAL_PRICE] - share_values[short]) * user_shorts[short][NUM_SHARES])

    # also have to add options here eventually

    return networth 


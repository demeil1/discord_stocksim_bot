from .utils.yf_scraper import getValue
from .utils.ids import getTransacId 
from .utils.timing import getTransacTime, getTransacDate
from .tables.shorts_table import appendToShortTable, removeFromUserShort, queryShortById, queryDistinctShorts, queryShortsByTicker
from .tables.users_table import queryUserBalance, updateUserBalance
from .networth import calculateUserNetWorth

def shortStock(user_id, command):
    TICKER = 0
    NUM_SHARES = 1
    STOP_LOSS = 2
    try:
        num_shares = command[NUM_SHARES]

        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"

        ticker = command[TICKER].upper()
        share_price = getValue([ticker])
        if share_price == None:
            return f"{command} Task Terminated: Ticker wasn't found"
        
        stop_loss = command[STOP_LOSS]
        if stop_loss <= share_price:
            return f"{command} Task Terminated: Stop loss ({stop_loss:.2f}) < or = current {ticker} share price ({share_price:.2f})"

        networth = calculateUserNetWorth(user_id)
        potential_loss = (stop_loss - share_price) * num_shares
        if potential_loss > networth:
            return f"{command} Task Terminated: Potential loss > current networth. Potential loss: {potential_loss:.2f}. Networth: {networth:.2f}"

        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id = getTransacId()
        transac_type = "short" 
        appendToShortTable(user_id,
                           transac_id,
                           ticker,
                           num_shares,
                           share_price,
                           stop_loss,
                           transac_type,
                           transac_date,
                           transac_time)
        
        return f"{command} Task Completed: Cover your position, or it will be done for you when the stop loss is hit."

    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

def coverShort(user_id, command):
    TRANSAC_ID = 0
    TICKER = 2
    NUM_SHARES = 3 
    INITIAL_PRICE = 4    
    try:
        transac_id = command[TRANSAC_ID]
        balance = queryUserBalance(user_id)
        
        transaction = queryShortById(user_id, transac_id)
        if transaction == None:
            return f"{command} Task Terminated: Couldn't pinpoint transaction by ID"

        num_shares = transaction[NUM_SHARES]
        initial_price = transaction[INITIAL_PRICE]
        ticker = transaction[TICKER]

        cur_price = getValue([ticker])

        profit = (initial_price - cur_price) * num_shares
        new_balance = balance + profit
        updateUserBalance(user_id, new_balance)
        removeFromUserShort(user_id, transac_id)
        return f"{command} Task Completed: Ran without error. Profit: {profit:.2f}. Balance: {new_balance:.2f}"

    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

def checkShortPositions():

    results = queryDistinctShorts() 
    if not results:
        return

    distinct_tickers = [ticker[0] for ticker in results]
    if not distinct_tickers:
        return

    ticker_val_dict = {}
    ticker_vals = getValue(distinct_tickers)
    if not (ticker_vals is list):
        ticker_vals = [ticker_vals]
    for ticker in range(len(distinct_tickers)):
        ticker_val_dict[distinct_tickers[ticker]] = ticker_vals[ticker]

    USER_ID = 0
    TRANSAC_ID = 1
    TICKER = 2
    STOP_LOSS = 5
    transac_list = [queryShortsByTicker(ticker) for ticker in distinct_tickers]
    transac_list = [transac[0] for transac in transac_list]
    for transac in transac_list:
        if transac[STOP_LOSS] <= ticker_val_dict[transac[TICKER]]:
            coverShort(transac[USER_ID], [transac[TRANSAC_ID]])

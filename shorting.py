from databases.yf_scraper import getValue
from databases.ids import getTransacId, userIdToString
from databses.timing import marketHours, getTimeSinceEpoch
from databases.shorts_table import appendToShortsTable, querySpecificUserShorts, removeFromUserShort
from databases.users_table import queryUserBalance, updateUserBalance

async def shortStock(user_id, command):
    CURRENT_VALUE = 0
    TICKER = 0
    NUM_SHARES = 1
    STOP_LOSS = 2
    try:
        user_id = userIdToString(user_id)
        num_shares = command[NUM_SHARES]

        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"

        ticker = command[TICKER].upper()
        share_price = (await getValue([ticker]))[CURRENT_VALUE]
        if share_price == None:
            return f"{command} Task Terminated: Ticker wasn't found"
        
        stop_loss = command[STOP_LOSS]
        if stop_loss <= share_price:
            return f"{command} Task Terminated: Stop loss < or = current {ticker} share price"

        balance = queryUserBalance(user_id)
        potential_loss = (stop_loss - share_price) * num_shares
        if potential_loss < balance:
            return f"{command} Task Terminated: Potential loss > Current balance. Potential loss {potential_loss:.2f}. Balance = {balance}"

        transac_time = getTimeSinceEpoch()
        transac_id = getTransacId()
        transac_type = "short" 
        appendToShortsTable(user_id,
                            transac_id,
                            ticker,
                            num_shares,
                            share_price,
                            stop_loss,
                            transac_type,
                            transac_time)
        
        return f"{command} Task Completed: Cover your position, or it will be done for you when the stop loss is hit."

    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

async def coverShort(user_id, command):
    CURRENT_VALUE = 0
    TRANSAC_ID = 0
    NUM_SHARES = 3 
    INITIAL_PRICE = 4    
    try:
        user_id = userIdToString(user_id)
        transac_id = command[TRANSAC_ID]
        balance = queryUserBalance(user_id)
        
        transaction = querySpecificUserShorts(user_id, transac_id)
        if transaction == None:
            return f"{command} Task Terminated: Couldn't pinpoint transaction by ID"

        num_shares = transaction[NUM_SHARES]
        initial_price = transaction[INITIAL_PRICE]

        cur_price = (await getValue([ticker]))[CURRENT_VALUE]

        profit = (initial_price - cur_price) * num_shares
        if profit == 0:
            removeFromUserShort(user_id, transac_id)
            return f"{command} Task Completed: Ran without error. Profit: 0. Balance: {balance}"
        elif profit > 0:
            new_balance = balance + profit
            updateUserBalance(user_id, new_balance)
            removeFromUserShort(user_id, transac_id)
            return f"{command} Task Completed: Ran without error. Profit: {profit}. Balance: {balance}"
        else: 
            while profit < 0:
                # sell stocks to recoup loss
                # query distinct tickers owned by individual queryDistinctUserStock
                # get values of distinct stock getValue
                # calculate how much of each stock to sell to get money to cover loss
                # created a command and pass the user_id and command sellStock
                # update user balance if we sell to much and end up going a bit positive
            removeFromUserShort(user_id, transac_id)

    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

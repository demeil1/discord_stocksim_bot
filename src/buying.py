# if result from getValue is None we have to return
# also have to do error checking
# print an error message
# for delayed buying we want to stop the function
# at the end of the trading day
# and sent a message to inform the user
from .utils.yf_scraper import getValue
from .utils.ids import getTransacId
from .utils.timing import marketHours, getTransacTime, getTransacDate
from .tables.stocks_table import appendToStockTable
from .tables.users_table import queryUserBalance, updateUserBalance

def buyStock(user_id, command):
    CURR_VALUE = 0
    TICKER = 0
    AMOUNT = 1
    try:
        num_shares = command[AMOUNT]
        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"

        ticker = command[TICKER].upper()
        share_price = getValue([ticker])
        if not share_price:
            return f"{command} Task Terminated: Ticker wasn't found"
        share_price = share_price[CURR_VALUE]

        total_transac_cost = share_price * num_shares
        balance = queryUserBalance(user_id)
        if total_transac_cost > balance:
            return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"

        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id = getTransacId()
        transac_type = "buy"
        appendToStockTable(
            user_id,
            transac_id,
            ticker,
            num_shares,
            share_price,
            transac_type,
            transac_date,
            transac_time,
        )
        new_balance = balance - total_transac_cost
        updateUserBalance(user_id, new_balance)
        return f"{command} Task Completed: Ran without error. Cost: {total_transac_cost:.2f}. Balance: {new_balance:.2f}"
    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

def delBuyStock(user_id, command):
    CURR_VALUE = 0
    TICKER = 0
    AMOUNT = 1
    TP_LOW = 2
    TP_HIGH = 3
    try:
        num_shares = command[AMOUNT]
        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"

        target_price_low = command[TP_LOW]
        target_price_high = command[TP_HIGH]
        if target_price_low > target_price_high:
            return f"{command} Task Terminated: Flip flopped target prices"

        ticker = command[TICKER].upper()
        share_price = getValue([ticker])
        if not share_price:
            return f"{command} Task Terminated: Ticker wasn't found"
        share_price = share_price[CURR_VALUE]

        max_transac_cost = target_price_high * num_shares
        balance = queryUserBalance(user_id)
        if max_transac_cost > balance:
            return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"

        while (share_price < target_price_low) or (share_price > target_price_high):
            if not marketHours():
                return f"{command} Task Terminated: Ran into after hours"
            balance = queryUserBalance(user_id)
            if max_transac_cost > balance:
                return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"
            share_price = getValue([ticker])
            if not share_price:
                return f"{command} Task Terminated: Ran into unexpected error"
            share_price = share_price[CURR_VALUE]

        transac_cost = num_shares * share_price

        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id = getTransacId()
        transac_type = "delbuy"
        appendToStockTable(
            user_id,
            transac_id,
            ticker,
            num_shares,
            share_price,
            transac_type,
            transac_date,
            transac_time,
        )
        new_balance = balance - transac_cost
        updateUserBalance(user_id, new_balance)
        return f"{command} Task Completed: Ran without error. Cost: {transac_cost:.2f} Balance: {new_balance:.2f}"
    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad paramaters passed"
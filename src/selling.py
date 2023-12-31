# if result from getValue is None we have to returning
# also have to do error check
# print an error message
# for delayed selling we want to stop the function
# at the end of the trading day
# and sent a message to inform the user
from .utils.yf_scraper import getValue
from .utils.timing import marketHours
from .tables.stocks_table import (
    updateUserStockAmount,
    querySpecificUserStock,
    removeFromUserStock,
)
from .tables.users_table import queryUserBalance, updateUserBalance

def sellStock(user_id, command):
    CURR_VALUE = 0
    TICKER = 0
    AMOUNT = 1
    try:
        num_shares_to_sell = command[AMOUNT]
        if num_shares_to_sell <= 0:
            return f"{command} Task Terminated: Can't sell negative or zero shares"

        ticker = command[TICKER].upper()
        share_price = getValue([ticker])
        if not share_price:
            return f"{command} Task Terminated: Ticker wasn't found"
        share_price = share_price[CURR_VALUE]

        transac_instances = querySpecificUserStock(user_id, ticker)
        if transac_instances == None:
            return f"{command} Task Terminated: No {ticker} stock owned"

        balance = queryUserBalance(user_id)
        new_balance = balance
        total_profit = 0

        TRANSAC_ID = 1
        TRANSAC_NUM_SHARES = 3
        TRANSAC_INITIAL_PRICE = 4

        for transac in transac_instances:
            transac_id = transac[TRANSAC_ID]
            transac_num_shares = transac[TRANSAC_NUM_SHARES]
            transac_initial_price = transac[TRANSAC_INITIAL_PRICE]

            transac_profit = (share_price * transac_num_shares) - (
                transac_initial_price * transac_num_shares
            )
            total_profit += transac_profit

            if num_shares_to_sell >= transac_num_shares:
                new_balance = (
                    new_balance
                    + (transac_initial_price * transac_num_shares)
                    + transac_profit
                )

                num_shares_to_sell -= transac_num_shares
                removeFromUserStock(user_id, transac_id)
            else:
                new_balance = (
                    new_balance
                    + (transac_initial_price * num_shares_to_sell)
                    + transac_profit
                )

                transac_num_shares -= num_shares_to_sell
                num_shares_to_sell = 0
                updateUserStockAmount(user_id, transac_id, transac_num_shares)
                break
        updateUserBalance(user_id, new_balance)
        if num_shares_to_sell == 0:
            return f"{command} Task Completed: Ran without error. Profit: {total_profit:.2f}. Balance: {new_balance:.2f}"
        else:
            return f"{command} Task Completed: Warning: '# to sell > # owned'. Profit: {total_profit:.2f}. Balance: {new_balance:.2f}"
    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad paramaters passed."

def delSellStock(user_id, command):
    CURR_VALUE = 0
    TICKER = 0
    AMOUNT = 1
    TP_LOW = 2
    TP_HIGH = 3
    try:
        num_shares_to_sell = command[AMOUNT]
        if num_shares_to_sell <= 0:
            return f"{command} Task Terminated: Can't sell negative or zero shares"

        target_price_low = command[TP_LOW]
        target_price_high = command[TP_HIGH]
        if target_price_low > target_price_high:
            return f"{command} Task Terminated: Flip flopped target prices"

        ticker = command[TICKER].upper()
        share_price = getValue([ticker])
        if not share_price:
            return f"{command} Task Terminated: Ticker wasn't ticker"
        share_price = share_price[CURR_VALUE]

        transac_instances = querySpecificUserStock(user_id, ticker)
        if transac_instances == None:
            return f"{command} Task Terminated: No {ticker} stock owned"

        while (share_price < target_price_low) or (share_price > target_price_high):
            if not marketHours():
                return f"{command} Task Terminated: Ran into after hours"

            share_price = getValue([ticker])
            if not share_price:
                return f"{command} Task Terminated: Ran into unexpected error"
            share_price = share_price[CURR_VALUE]

        balance = queryUserBalance(user_id)
        new_balance = balance
        total_profit = 0

        TRANSAC_ID = 1
        TRANSAC_NUM_SHARES = 3
        TRANSAC_INITIAL_PRICE = 4

        transac_instances = querySpecificUserStock(user_id, ticker)
        for transac in transac_instances:
            transac_id = transac[TRANSAC_ID]
            transac_num_shares = transac[TRANSAC_NUM_SHARES]
            transac_initial_price = transac[TRANSAC_INITIAL_PRICE]

            transac_profit = (share_price * transac_num_shares) - (
                transac_initial_price * transac_num_shares
            )
            total_profit += transac_profit

            if num_shares_to_sell >= transac_num_shares:
                new_balance = (
                    new_balance
                    + (transac_initial_price * transac_num_shares)
                    + transac_profit
                )
                num_shares_to_sell -= transac_num_shares
                removeFromUserStock(user_id, transac_id)
            else:
                new_balance = (
                    new_balance
                    + (transac_initial_price * num_shares_to_sell)
                    + transac_profit
                )
                transac_num_shares -= num_shares_to_sell
                num_shares_to_sell = 0
                updateUserStockAmount(user_id, transac_id, transac_num_shares)
                break
        updateUserBalance(user_id, new_balance)
        if num_shares_to_sell == 0:
            return f"{command} Task Completed: Ran without error. Profit: {total_profit:.2f}. Balance: {new_balance:.2f}"
        else:
            return f"{command} Task Completed: Warning: '# to sell > # owned'. Profit: {total_profit:.2f}. Balance: {new_balance:.2f}"
    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad paramaters passed."

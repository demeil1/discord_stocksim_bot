# if result from getValue is None we have to return
# also have to do error checking
# print an error message
# for delayed buying we want to stop the function
# at the end of the trading day 
# and sent a message to inform the user
from databases.yf_scraper import getValue
from databases.ids import getTransacId 
from databases.timing import marketHours, getTransacTime, getTransacDate
from databases.stocks_table import appendToStockTable
from databases.users_table import queryUserBalance, updateUserBalance


async def buyStock(user_id, command):
    CURRENT_VALUE = 0
    TICKER = 0
    AMOUNT = 1
    try:
        num_shares = command[AMOUNT]

        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"
        
        ticker = command[TICKER].upper()
        share_price = (await getValue([ticker]))[CURRENT_VALUE]

        if share_price == None:
            return f"{command} Task Terminated: Ticker wasn't found"

        total_transac_cost = share_price * num_shares
        
        # need to check balance from user database
        balance = queryUserBalance(user_id)
        if total_transac_cost > balance:
            return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"
        
        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id   = getTransacId()
        transac_type = "buy"

        appendToStockTable(user_id,
                          transac_id,
                          ticker,
                          num_shares,
                          share_price,
                          transac_type,
                          transac_date,
                          transac_time)
        
        new_balance = balance - total_transac_cost
        updateUserBalance(user_id, new_balance)

        return f"{command} Task Completed: Ran without error. Cost: {total_transac_cost:.2f}. Balance: {new_balance:.2f}"

    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."
    
async def delBuyStock(user_id, command):
    CURRENT_VALUE = 0
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
        cur_value = (await getValue([ticker]))[CURRENT_VALUE]

        if cur_value == None:
            return f"{command} Task Terminated: Ticker wasn't found"

        max_transac_cost = target_price_high * num_shares
        
        balance = queryUserBalance(user_id)
        if max_transac_cost > balance:
            return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"
        
        while (cur_value < target_price_low) or (cur_value > target_price_high):
            
            if not marketHours():
                return f"{command} Task Terminated: Ran into after hours"

            balance = queryUserBalance(user_id)
            if max_transac_cost > balance:
                return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"
            
            cur_value = (await getValue([ticker]))[CURRENT_VALUE]

            if cur_value == None:
                return f"{command} Task Terminated: Ran into unexpected error"
                
            cur_value = cur_value
                
        transac_cost = num_shares * cur_value
        
        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id = getTransacId()
        transac_type = "delbuy"

        appendToStockTable(user_id,
                           transac_id,
                           ticker,
                           num_shares,
                           cur_value,
                           transac_type,
                           transac_date,
                           transac_time)

        new_balance = balance - transac_cost
        updateUserBalance(user_id, new_balance)

        return f"{command} Task Completed: Ran without error. Cost: {transac_cost:.2f} Balance: {new_balance:.2f}"

    except (IndexError, TypeError, ValueError):

        return f"{command} Task Terminated: Bad paramaters passed"
    

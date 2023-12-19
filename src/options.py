from .utils.yf_scraper import getValue, calculateOptionPremium
from .utils.ids import getTransacId
from .utils.timing import getTransacTime, getTransacDate, getTimeSinceEpoch
from .tables.options_table import appendToOptionTable, queryOptions, queryOptionById, removeFromUserOption
from .tables.users_table import queryUserBalance, updateUserBalance

def optionStock(user_id, command):
    TICKER = 0
    NUM_SHARES = 1
    EXPIRATION_DAYS = 2
    INTEREST_RATE = 3
    TRANSAC_TYPE = 4
    try:
        num_shares = command[NUM_SHARES]
        if num_shares <= 0:
            return f"{command} Task Terminated: Can't purchase negative or zero shares"

        expiration_days = command[EXPIRATION_DAYS]
        if expiration_days <= 0:
            return f"{command} Task Terminated: Days until contract expires can't be < or = 0"

        ticker = command[TICKER].upper()
        strike_price = getValue([ticker])
        if not strike_price:
            return f"{command} Task Terminated: Ticker wasn't found"
        
        interest_rate = command[INTEREST_RATE]
        premium = calculateOptionPremium(ticker, strike_price, expiration_days, interest_rate)
        if not premium:
            return f"{command} Task Terminated: Couldn't get premium"

        balance = queryUserBalance(user_id)
        if premium > balance:
            return f"{command} Task Terminated: Account balance too low. Balance: {balance:.2f}"

        transac_time_since_epoch = getTimeSinceEpoch()
        transac_time = getTransacTime()
        transac_date = getTransacDate()
        transac_id   = getTransacId()
        transac_type = command[TRANSAC_TYPE]

        appendToOptionTable(user_id,
                            transac_id,
                            ticker,
                            num_shares,
                            strike_price,
                            premium,
                            expiration_days,
                            transac_type,
                            transac_date,
                            transac_time,
                            transac_time_since_epoch)

        return f"{command} Task Completed: Ran without error. Premium: {premium:.2f} will be deducted after exercising option"
    
    except (IndexError, TypeError, ValueError):
        return f"{command} Task Terminated: Bad parameters passed."

def exerciseOption(user_id, command):
    TRANSAC_ID = 0
    TICKER = 2
    NUM_SHARES = 3
    STRIKE_PRICE = 4
    PREMIUM = 5
    TYPE = 7
    try:
        transac_id = command[TRANSAC_ID]
        transac = queryOptionById(user_id, transac_id)
        if not transac:
            return f"{command} Task Terminated: Couldn't pinpoint transaction by ID"

        ticker = transac[TICKER]
        num_shares = transac[NUM_SHARES]
        premium = transac[PREMIUM]
        current_price = getValue([ticker])
        strike_price = transac[STRIKE_PRICE]
        balance = queryUserBalance(user_id)

        transac_type = transac[TYPE]
        if transac_type.lower() == "call":
            profit = ((current_price - strike_price) * num_shares) - premium
        else: 
            profit = ((strike_price - current_price) * num_shares) - premium
        
        new_balance = balance + profit
        updateUserBalance(user_id, new_balance) 
        return f"{command} Task Completed: Ran without error. Profit: {profit:.2f}. Balance: {new_balance:.2f}"

    except:
        return f"{command} Task Terminated: Bad parameters passed."

def checkOptionPositions():

    USER_ID = 0
    TRANSAC_ID = 1
    PREMIUM = 5
    EXPIRATION_DAYS = 6
    TIME_SINCE_EPOCH = 10

    transacs = queryOptions()
    if not transacs:
        return

    for transac in transacs:
        days = transac[EXPIRATION_DAYS]
        time_since_epoch = transac[TIME_SINCE_EPOCH]

        # 86400 = seconds in a day if expiration_time > current_time
        if ((days * 86400) + time_since_epoch) < getTimeSinceEpoch():
            user_id = transac[USER_ID]
            transac_id = transac[TRANSAC_ID]
            premium = transac[PREMIUM]
            removeFromUserOption(user_id, transac_id)
            updateUserBalance(user_id, queryUserBalance(user_id) - premium)


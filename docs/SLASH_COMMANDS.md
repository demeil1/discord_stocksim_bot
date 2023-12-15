### discord_stocksim_bot

A stock simulator bot for discord!

# Functionality

* buying
* target price buying 
* selling
* target price selling
* shorting

# TODOs

* options

# /balance
* description: returns your balance

# /networth
* description: returns you netwroth

# /query
* description: returns transactions of ticker(s)
* parameters: 
    - ticker(s): string (text) seperated by space
* example:
    - "/query *" returns the transaction history of all tickers owned
    - "/query AAPL" returns the transaction history of your AAPL share purchases only
        
# /buy
* description: purchases an amount of shares 
* paramaters: 
    - ticker: string (text)
    - number of shares: int (whole number)
* example:
    - "/buy AAPL 5" purchases 5 shares of Apple at the current market price
* success ("Task Completed: "):
    - "Ran without error. Cost: {transaction_cost} Balance: {new_balance}"
* errors ("Task Terminated: "):
    - "Can't purchase negative or zero shares":
        - Solution: enter a share amount to purchase greater than 0
    - "Ticker wasn't found":
        - Solution: make sure that the ticker is spelled correctly and exists
    - "Account balance too low. Balance: {your_balance}":
        - Solution: use the /balance command to get your current balance
    - "Bad parameters passed":
        - Troubleshooting: check that you have the correct amount and type of parameters

# /sell 
* description: sell an amount of shares 
* paramaters: 
    - ticker: string (text)
    - number of shares: int (whole number)
* example:
    - "/sell AAPL 5" sells 5 shares of Apple at the current market price
* success ("Task Completed: "):
    - "Ran without error. Profit: {transaction_profit} Balance: {new_balance}"
* warning ("Task Completed: Warning: "):
    - "# to sell > # owned":
        - Solution: no solution needed; however, if you dont want to see this warning you 
        can use the /query command to see transaction history and amount of stocks owned
* errors ("Task Terminated: "):
    - "Can't sell negative or zero shares":
        - Solution: enter a share amount to purchase greater than 0
    - "Ticker wasn't found":
        - Solution: make sure that the ticker is spelled correctly and exists
    - "No {ticker} stock owned":
        - Solution: ensure that the stock is bough before selling (can use /query command)
    - "Bad parameters passed":
        - Troubleshooting: check that you have the correct amount and type of parameters

# /delbuy 
* description: purchases an amount of shares within a cost range
* protection:
    - To protect against malicious commands, threads are returned if they exceed the time 
    the market is open.
* paramaters: 
    - ticker: string (text)
    - number of shares: int (whole number)
    - low target price: float (decimal)
    - high target price: float (decimal)
* example:
    - "/delbuy AAPL 5 100.00 200.00" purchases 5 shares of when the current market value
    lies between [100.00, 200.00]
* success ("Task Completed: "):
    - "Ran without error. Cost: {transaction_cost} Balance: {new_balance}"
* errors ("Task Terminated: "):
    - "Can't purchase negative or zero shares":
        - Solution: enter a share amount to purchase greater than 0
    - "Flip flopped target prices":
        - Solution: swap the target prices 
    - "Ticker wasn't found":
        - Solution: make sure that the ticker is spelled correctly and exists
    - "Ran into after hours":
        - Solution: make your /delbuy command reasonable (see the protection section)
    - "Account balance too low. Balance: {your_balance}":
        - Solution: use the /balance command to get your current balance
    - "Bad parameters passed":
        - Troubleshooting: check that you have the correct amount and type of parameters

# /delsell 
* description: sell an amount of shares within a cost range
* protection:
    - To protect against malicious commands, threads are returned if they exceed the time 
    the market is open.
* parameters: 
    - ticker: string (text)
    - number of shares: int (whole number)
    - low target price: float (decimal)
    - high target price: float (decimal)
* example:
    - "/delsell AAPL 5 100.00 200.00" sells 5 shares of when the current market value
    lies between [100.00, 200.00]
* success ("Task Completed: "):
    - "Ran without error. Profit: {transaction_profit} Balance: {new_balance}"
* warning ("Task Completed: Warning: "):
    - "# to sell > # owned":
        - Solution: no solution needed however if you dont want to see this warning you 
        can use the /query command to see transaction history and amount of stocks owned
* errors ("Task Terminated: "):
    - "Can't sell negative or zero shares":
        - Solution: enter a share amount to purchase greater than 0
    - "Flip flopped target prices":
        - Solution: swap the target prices 
    - "Ticker wasn't found":
        - Solution: make sure that the ticker is spelled correctly and exists
    - "No {ticker} stock owned":
        - Solution: ensure that the stock is bough before selling (can use /query command)
    - "Ran into after hours":
        - Solution: make your /delbuy command reasonable (see the protection section)
    - "Account balance too low. Balance: {your_balance}":
        - Solution: use the /balance command to get your current balance
    - "Bad parameters passed":
        - Troubleshooting: check that you have the correct amount and type of parameters

# /short
* description: short an amount of shares of a ticker
* proctection: 
    - Potential loss is compared to networth. If potential loss > networth, task terminates
    - Short positions covered automatically when stop loss is hit
* parameters:
    - ticker: string (text)
    - number of shares: int (whole number)
    - stop loss: float (decimal)
* example:
    - "/short AAPL 5 200" shorts 5 shares of AAPL and will automatically be covered if AAPL
    share price ever reached 200
* success ("Task Completed: "):
    - "Cover your Position, or it will be done for you when the stop loss is hit"
* errors ("Task Terminated: "):
    - "Can't purchase negative or zero shares":
        - Solution: enter a share amount to purchase greater than 0
    - "Ticker wasn't found":
        - Solution: make sure that the ticker is spelled correctly and exists
    - "Stop loss ({stop_loss}) < or = current {ticker} share price ({share_price})":
        - Solution: stop loss must be > current stock price
    - "Potential loss > current networth. Potential loss: {potential_loss}. 
    Networth: {networth}":
        - Solution: decrease the amount of shares or stop stop_loss
    - "Bad parameters passed":
        - Troubleshooting: check that you have the correct amount and type of parameters

# /cover
* description: cover a short position
* parameters:
    - transaction id: string (text)
* example:
    - "/cover fgn4389dgjn24r1d" covers a short transanction with transaction id 
    "fgn4389dgjn24r1d"
* success ("Task Completed"):
    - "Ran without error. Profit: {profit}. Balance: {balance}"
* errors ("Task Terminated: "):
    - "Couldn't pinpoint transaction by ID":
        - Solution: make sure the transaction id you are using is from a transaction that 
        used the /short command (use /query to see transaction types) and that it was 
        copied correctly
    - "Bad parameters passed":
        - Troubleshoorting: check that you have the correct amount and type of parameters

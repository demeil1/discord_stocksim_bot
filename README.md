### discord_stocksim_bot

A stock simulator bot for discord!
Created by Demeil Khoshaba and Andy Mai
==================================================

**Functionality**

* buying
* target price buying 
* selling
* target price selling
==================================================

**TODOs**

* shorting
* options
==================================================

## Bot Slash Commands

# /balance
    * description: returns your Balance

# /query
    * description: returns transaction history of ticker(s)
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
            - Wrong: "/buy AAPL -1"
            - Correct: "/buy AAPL 5"
            - Solution: enter a share amount to purchase greater than 0
        - "Ticker wasn't found":
            - Wrong: "/buy APPL 5"
            - Correct "/buy AAPL 5"
            - Solution: make sure that the ticker is spelled correctly and exists
        - "Account balance too low. Balance: {your_balance}":
            - Wrong: "/buy AAPL 5" when /balance returns $1
            - Correct: "/buy AAPL 5" when /balance command returns $10,000
            - Solution: use the /balance command to get your current balance
        - "Bad parameters passed":
            - Wrong: "/buy AAPL"
            - Correct: "/buy AAPL 5"
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
            - Wrong: "buy AAPL -1 0.00 1000.00"
            - Correct: "buy AAPL 5 0.00 1000.00"
            - Solution: enter a share amount to purchase greater than 0
        - "Flip flopped target prices":
            - Wrong: "buy AAPL 5 1000.00 0.00"
            - Correct: "buy AAPL 5 0.00 1000.00"
            - Solution: swap the target prices 
        - "Ticker wasn't found":
            - Wrong: "buy APPL 5 0.00 1000.00"
            - Correct "buy AAPL 5 0.00 1000.00"
            - Solution: make sure that the ticker is spelled correctly and exists
        - "Ran into after hours":
            - Solution: make your /delbuy command reasonable (see the protection section)
        - "Account balance too low. Balance: {your_balance}":
            - Wrong: "buy AAPL 5 0.00 1000.00" when /balance returns $1
            - Correct: "buy AAPL 5 0.00 1000.00" when /balance command returns $10,000
            - Solution: use the /balance command to get your current balance
        - "Bad parameters passed":
            - Wrong: "buy AAPL 5"
            - Correct: "buy AAPL 5 0.00 1000.00"
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
            - Example: "/sell AAPL 5" when you only own 4 shares of AAPL
            - Solution: no solution needed however if you dont want to see this warning you 
            can use the /query command to see transaction history and amount of stocks owned
    * errors ("Task Terminated: "):
        - "Can't sell negative or zero shares":
            - Wrong: "/sell AAPL -1"
            - Correct: "/sell AAPL 5"
            - Solution: enter a share amount to purchase greater than 0
        - "Ticker wasn't found":
            - Wrong: "/sell APPL 5"
            - Correct "/sell AAPL 5"
            - Solution: make sure that the ticker is spelled correctly and exists
        - "No {ticker} stock owned":
            - Solution: ensure that the stock is bough before selling (can use /query command)
        - "Bad parameters passed":
            - Wrong: "/sell AAPL"
            - Correct: "/sell AAPL 5"
            - Troubleshooting: check that you have the correct amount and type of parameters

# /delsell 
    * description: sell an amount of shares within a cost range
    * protection:
        - To protect against malicious commands, threads are returned if they exceed the time 
        the market is open.
    * paramaters: 
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
            - Example: "/delsell AAPL 5" when you only own 4 shares of AAPL
            - Solution: no solution needed however if you dont want to see this warning you 
            can use the /query command to see transaction history and amount of stocks owned
    * errors ("Task Terminated: "):
        - "Can't sell negative or zero shares":
            - Wrong: "/delsell AAPL -1 0.00 1000.00"
            - Correct: "/delsell AAPL 5 0.00 1000.00"
            - Solution: enter a share amount to purchase greater than 0
        - "Flip flopped target prices":
            - Wrong: "/delsell AAPL 5 1000.00 0.00"
            - Correct: "/delsell AAPL 5 0.00 1000.00"
            - Solution: swap the target prices 
        - "Ticker wasn't found":
            - Wrong: "/delsell APPL 5 0.00 1000.00"
            - Correct "/delsell AAPL 5 0.00 1000.00"
            - Solution: make sure that the ticker is spelled correctly and exists
        - "No {ticker} stock owned":
            - Solution: ensure that the stock is bough before selling (can use /query command)
        - "Ran into after hours":
            - Solution: make your /delbuy command reasonable (see the protection section)
        - "Account balance too low. Balance: {your_balance}":
            - Wrong: "/delsell AAPL 5 0.00 1000.00" when /balance returns $1
            - Correct: "/delsell AAPL 5 0.00 1000.00" when /balance command returns $10,000
            - Solution: use the /balance command to get your current balance
        - "Bad parameters passed":
            - Wrong: "/delsell AAPL 5"
            - Correct: "/delsell AAPL 5 0.00 1000.00"
            - Troubleshooting: check that you have the correct amount and type of parameters

# Functionality

* buying
* target price buying 
* selling
* target price selling
* shorting
* options

# TODOs

* dividends 

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

# /sell 
* description: sell an amount of shares 
* paramaters: 
    - ticker: string (text)
    - number of shares: int (whole number)
* example:
    - "/sell AAPL 5" sells 5 shares of Apple at the current market price

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

# /cover
* description: cover a short position
* parameters:
    - transaction id: string (text)
* example:
    - "/cover fgn4389dgjn24r1d" covers a short transanction with transaction id 
    "fgn4389dgjn24r1d"

# /premium
* description: view premium cost for an option contract
* parameters:
    - ticker: string (text)
    - expiration days: int (whole number)

# /call
* description: obtain a call option contract
* parameters: 
    - ticker: string (text)
    - number of shares: int (whole number)
    - expiration days: int (whole number)
* example: 
    - "/call AAPL 5 30" provides a call option contract for 5 shares of AAPL that expires in 30 days

# /put
* description: obtain a put option contract
* parameters: 
    - ticker: string (text)
    - number of shares: int (whole number)
    - expiration days: int (whole number)
* example: 
    - "/put AAPL 5 30" provides a call option contract for 5 shares of AAPL that expires in 30 days

# /exercise
* description: exercise a call or put options
* parameters: 
    - transaction id: string (text)
* example:
    - "/exercise fgn4389dgjn24r1d" exercises the option transaction fgn4389dgjn24r1d whether it be a call or put

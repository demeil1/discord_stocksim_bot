from .database_globals import *
from .yf_scraper import getValue

def createStockTable():

    create_table_statement = f'''CREATE TABLE IF NOT EXISTS STOCKS (
        USER_ID TEXT,
        TRANSAC_ID TEXT,
        TICKER TEXT, 
        NUM_SHARES INTEGER, 
        INITIAL_PRICE INTEGER,
        TRANSAC_TYPE TEXT,
        TRANSAC_DATE TEXT,
        TRANSAC_TIME TEXT
    )'''
    CURSOR.execute(create_table_statement)

def appendToStockTable(user_id,
                       transac_id,
                       ticker,
                       num_shares,
                       initial_price,
                       transac_type,
                       transac_date,
                       transac_time):

    append_statement = f'''INSERT INTO STOCKS (
        USER_ID,
        TRANSAC_ID,
        TICKER, 
        NUM_SHARES, 
        INITIAL_PRICE,
        TRANSAC_TYPE,
        TRANSAC_DATE,
        TRANSAC_TIME
    ) VALUES (?,?,?,?,?,?,?,?)'''

    CURSOR.execute(append_statement, (
        user_id,
        transac_id,
        ticker,
        num_shares,
        initial_price,
        transac_type,
        transac_date,
        transac_time
    )) 

    CONNECTION.commit()

def queryUserStock(user_id):

    query_statement = f"SELECT * FROM STOCKS WHERE USER_ID = ?"
    CURSOR.execute(query_statement, (user_id,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def querySpecificUserStock(user_id, ticker):

    query_statement = f"SELECT * FROM STOCKS WHERE USER_ID = ? AND TICKER = ?"
    CURSOR.execute(query_statement, (user_id, ticker,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def updateUserStockAmount(user_id, transac_id, amount): 

    update_statement = f"UPDATE STOCKS SET NUM_SHARES = ? WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(update_statement, (amount, user_id, transac_id,))
    CONNECTION.commit()

def queryDistinctStock():

    distinct_ticker_statement = f"SELECT DISTINCT TICKER FROM STOCKS"
    CURSOR.execute(distinct_ticker_statement)
    distinct_tickers = CURSOR.fetchall()
    return distinct_tickers
    

def removeFromUserStock(user_id, transac_id):
    
    remove_statement = f"DELETE FROM STOCKS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(remove_statement, (user_id, transac_id,))
    CONNECTION.commit()

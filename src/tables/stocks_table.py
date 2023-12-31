from .database_globals import *

def createStockTable():
    create_table_statement = """CREATE TABLE IF NOT EXISTS STOCKS (
        USER_ID INTEGER,
        TRANSAC_ID TEXT,
        TICKER TEXT, 
        NUM_SHARES INTEGER, 
        INITIAL_PRICE INTEGER,
        TRANSAC_TYPE TEXT,
        TRANSAC_DATE TEXT,
        TRANSAC_TIME TEXT
    )"""
    CURSOR.execute(create_table_statement)

def appendToStockTable(
    user_id,
    transac_id,
    ticker,
    num_shares,
    initial_price,
    transac_type,
    transac_date,
    transac_time,
):
    append_statement = """INSERT INTO STOCKS (
        USER_ID,
        TRANSAC_ID,
        TICKER, 
        NUM_SHARES, 
        INITIAL_PRICE,
        TRANSAC_TYPE,
        TRANSAC_DATE,
        TRANSAC_TIME
    ) VALUES (?,?,?,?,?,?,?,?)"""
    CURSOR.execute(
        append_statement,
        (
            user_id,
            transac_id,
            ticker,
            num_shares,
            initial_price,
            transac_type,
            transac_date,
            transac_time,
        ),
    )
    CONNECTION.commit()

def queryUserStock(user_id):
    query_statement = "SELECT * FROM STOCKS WHERE USER_ID = ?"
    CURSOR.execute(query_statement, (user_id,))
    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def querySpecificUserStock(user_id, ticker):
    query_statement = "SELECT * FROM STOCKS WHERE USER_ID = ? AND TICKER = ?"
    CURSOR.execute(
        query_statement,
        (
            user_id,
            ticker,
        ),
    )
    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def queryDistinctUserStock(user_id):
    query_statement = "SELECT DISTINCT TICKER FROM STOCKS WHERE USER_ID = ?"
    CURSOR.execute(query_statement, (user_id,))
    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def queryUserStockAmount(user_id, ticker):
    query_statement = "SELECT SUM(NUM_SHARES) FROM STOCKS WHERE USER_ID = ? AND TICKER = ?"
    
    CURSOR.execute(
        query_statement,
        (
            user_id,
            ticker,
        ),
    )
    result = CURSOR.fetchone()
    return result[0] if result else 0

def updateUserStockAmount(user_id, transac_id, amount):
    update_statement = "UPDATE STOCKS SET NUM_SHARES = ? WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(
        update_statement,
        (
            amount,
            user_id,
            transac_id,
        ),
    )
    CONNECTION.commit()

def queryDistinctStock():
    distinct_ticker_statement = "SELECT DISTINCT TICKER FROM STOCKS"
    CURSOR.execute(distinct_ticker_statement)
    distinct_tickers = CURSOR.fetchall()
    return distinct_tickers

def removeFromUserStock(user_id, transac_id):
    remove_statement = "DELETE FROM STOCKS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(
        remove_statement,
        (
            user_id,
            transac_id,
        ),
    )
    CONNECTION.commit()

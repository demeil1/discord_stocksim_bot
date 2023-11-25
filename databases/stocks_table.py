from .database_globals import *

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

# def updateUserStockPrices(user_id):       MOVE THIS TO THE SPECIFIC UPDATING TABLE

#     distinct_ticker_statement = f"SELECT DISTINCT TICKER FROM STOCKS WHERE USER_ID = ?"
#     CURSOR.execute(distinct_ticker_statement, (user_id,))
#     distinct_tickers = CURSOR.fetchall()
    
#     update_statement = f'''UPDATE {user_id} 
#                             SET CURRENT_PRICE = ? 
#                             WHERE TICKER = ?'''
#     val_tkr_list = []

#     ticker_value_object = getValue(distinct_tickers)
#     for tkr, val in ticker_value_object:
#         val_tkr_list.append((val, tkr))

#     CURSOR.executemany(update_statement, val_tkr_list)
    
#     CONNECTION.commit()

def removeFromUserStock(user_id, transac_id):
    
    remove_statement = f"DELETE FROM STOCKS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(remove_statement, (user_id, transac_id,))

    CONNECTION.commit()

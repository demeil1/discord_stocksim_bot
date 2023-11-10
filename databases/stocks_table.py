from .database_globals import *
from .yf_scraper import getValue

STOCK_TABLE_IS_SETUP = False

def create_user_stock_table(user_id):

    create_table_statement = f'''CREATE TABLE IF NOT EXISTS {user_id} (
        TICKER TEXT, 
        NUM_SHARES INTEGER, 
        INITIAL_PRICE INTEGER,
        CURRENT_PRICE INTEGER,
        TRANSAC_ID TEXT,
        TRANSAC_TYPE TEXT,
        TRANSAC_DATE TEXT,
        TRANSAC_TIME TEXT
    )'''

    CURSOR.execute(create_table_statement)

def stock_table_setup():
    return STOCK_TABLE_IS_SETUP

def appendToStockTable(user_id,
                       transac_id,
                       transac_type,
                       transac_date,
                       transac_time,
                       ticker,
                       num_shares,
                       intitial_price,
                       current_price):

    if not stock_table_setup():
        create_user_stock_table(user_id)
        STOCK_TABLE_IS_SETUP = True

    append_statement = f'''INSERT INTO {user_id} (
        TICKER, 
        NUM_SHARES, 
        INITIAL_PRICE,
        CURRENT_PRICE,
        TRANSAC_ID,
        TRANSAC_TYPE,
        TRANSAC_DATE,
        TRANSAC_TIME 
    ) VALUES (?,?,?,?,?,?,?,?)'''

    CURSOR.execute(append_statement, (
        ticker,
        num_shares,
        intitial_price,
        current_price,
        transac_id,
        transac_type,
        transac_date,
        transac_time,
    )) 

    CONNECTION.commit()

def queryUserStock(user_id):

    query_statement = f"SELECT * FROM {user_id}"
    CURSOR.execute(query_statement)

    results = CURSOR.fetchall()
    if results == []:
        return None

    return results

def querySpecificUserStock(user_id, ticker):

    query_statement = f"SELECT * FROM {user_id} WHERE TICKER = ?"
    CURSOR.execute(query_statement, (ticker,))

    results = CURSOR.fetchall()
    if results == []:
        return None
        
    return results

def updateUserStockAmount(user_id, transac_id, amount): # finish

    update_statement = f"UPDATE {user_id} SET NUM_SHARES = ? WHERE TRANSAC_ID = ?"
    CURSOR.execute(update_statement, (amount, transac_id,))
    CONNECTION.commit()

def updateUserStockPrices(user_id):

    distinct_ticker_statement = f"SELECT DISTINCT TICKER FROM {user_id}"
    CURSOR.execute(distinct_ticker_statement)
    distinct_tickers = CURSOR.fetchall()
    
    update_statement = f'''UPDATE {user_id} 
                            SET CURRENT_PRICE = ? 
                            WHERE TICKER = ?'''
    val_tkr_list = []

    ticker_value_object = getValue(distinct_tickers)
    for tkr, val in ticker_value_object:
        val_tkr_list.append((val, tkr))

    CURSOR.executemany(update_statement, val_tkr_list)
    
    CONNECTION.commit()

def removeFromUserStock(user_id, transac_id):
    
    remove_statement = f"DELETE FROM {user_id} where TRANSAC_ID = ?"
    CURSOR.execute(remove_statement, (transac_id,))

    CONNECTION.commit()

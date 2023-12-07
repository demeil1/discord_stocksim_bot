# may need too create specific user ids because discord api 
# only gives us the name and we need a more robust way of 
# keeping track of users because usernames can change or interfer
from .database_globals import *

def createShortsTable():

    create_table_statement = '''CREATE TABLE IF NOT EXISTS SHORTS (
        USER_ID TEXT,
        TRANSAC_ID TEXT,
        TICKER TEXT,
        NUM_SHARES INTEGER,
        INITIAL_PRICE INTEGER,
        STOP_LOSS INTEGER,
        TRANSAC_TYPE TEXT,
        TRANSAC_TIME_SINCE_EPOCH INTEGER
    )''' 
    CURSOR.execute(create_table_statement)

def appendToShortTable(user_id,
                       transac_id,
                       ticker,
                       num_shares,
                       initial_price,
                       stop_loss
                       transac_type,
                       transac_time):

    append_statement = '''INSERT INTO SHORTS (
        USER_ID,
        TRANSAC_ID,
        TICKER,
        NUM_SHARES,
        INITIAL_PRICE,
        STOP_LOSS,
        TRANSAC_TYPE,
        TRANSAC_TIME_SINCE_EPOCH
    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''

    CURSOR.execute(append_statement, (
        user_id,
        transac_id,
        ticker,
        num_shares,
        initial_price,
        stop_loss,
        transac_type,
        transac_time
    ))
    CONNECTION.commit()

def queryUserShorts(user_id):

    query_statement = "SELECT * FROM SHORTS WHERE USER_ID = ?"
    CURSOR.execute(query_statement, (user_id,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def querySpecificUserShorts(user_id, ticker):
    
    query_statement = "SELECT * FROM STOCKS WHERE USER_ID = ? AND TICKER = ?"
    CURSOR.execute(query_statement, (user_id, ticker,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def removeFromUserShort(user_id, transac_id):

    remove_statement = "DELETE FROM STOCKS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(remove_statement, (user_id, transac_id,))
    CONNECTION.commit()

# may need too create specific user ids because discord api 
# only gives us the name and we need a more robust way of 
# keeping track of users because usernames can change or interfer

from .database_globals import *

def createOptionsTable():

    create_table_statement = '''CREATE TABLE IF NOT EXISTS OPTIONS (
        USER_ID TEXT,
        TRANSAC_ID TEXT,
        TICKER TEXT,
        NUM_SHARES INTEGER,
        STRIKE_PRICE INTEGER,
        PREMIUM INTEGER,
        EXPIRATION_DAYS INTEGER,
        TRANSAC_TYPE TEXT,
        TRANSAC_DATE TEXT,
        TRANSAC_TIME TEXT,
        TRANSAC_TIME_SINCE_EPOCH INTEGER
    )'''
    CURSOR.execute(create_table_statement)

def appendToOptionTable(user_id,
                        transac_id,
                        ticker,
                        num_shares,
                        strike_price,
                        premium,
                        expiration_days,
                        transac_type,
                        transac_date,
                        transac_time,
                        transac_time_since_epoch):

    append_statement = '''INSERT INTO OPTIONS (
        USER_ID,
        TRANSAC_ID,
        TICKER,
        NUM_SHARES,
        STRIKE_PRICE,
        PREMIUM,
        EXPIRATION_DAYS,
        TRANSAC_TYPE,
        TRANSAC_DATE,
        TRANSAC_TIME,
        TRANSAC_TIME_SINCE_EPOCH
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    CURSOR.execute(append_statement, (
        user_id,
        transac_id,
        ticker,
        num_shares,
        strike_price,
        premium,
        expiration_days,
        transac_type,
        transac_date,
        transac_time,
        transac_time_since_epoch
    ))

    CONNECTION.commit()

def queryOptions():

    query_statement = "SELECT * FROM OPTIONS"
    CURSOR.execute(query_statement)

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def queryUserOptions(user_id):

    query_statement = "SELECT * FROM OPTIONS WHERE USER_ID = ?"
    CURSOR.execute(query_statement, (user_id,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def queryOptionById(user_id, transac_id):

    query_statement = "SELECT * FROM OPTIONS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(query_statement, (user_id, transac_id,))

    result = CURSOR.fetchall()
    if result == []:
        return None
    return result[0]

def querySpecificUserOptions(user_id, ticker):

    query_statement = "SELECT * FROM OPTIONS WHERE USER_ID = ? AND TICKER = ?"
    CURSOR.execute(query_statement, (user_id, ticker,))

    results = CURSOR.fetchall()
    if results == []:
        return None
    return results

def removeFromUserOption(user_id, transac_id):

    remove_statement = "DELETE FROM OPTIONS WHERE USER_ID = ? AND TRANSAC_ID = ?"
    CURSOR.execute(remove_statement, (user_id, transac_id,))
    CONNECTION.commit()


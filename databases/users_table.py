from .database_globals import *

USERS_TABLE_IS_SETUP = False

def create_users_table():
    
    create_table_statement = '''CREATE TABLE IF NOT EXISTS USERS (
        USER_ID TEXT PRIMARY KEY,
        BALANCE INTEGER
    )'''
    
    CURSOR.execute(create_table_statement)

def users_table_setup():
    return USERS_TABLE_IS_SETUP

def appendToUserTable(user_id):

    if not users_table_setup():
        create_users_table()
        USERS_TABLE_IS_SETUP = True

    append_statement = '''INSERT INTO USERS (
        USER_ID,
        BALANCE
    ) VALUES (?,?)'''

    STARTING_BALANCE = 10000
    CURSOR.execute(append_statement, (user_id, STARTING_BALANCE))
    CONNECTION.commit()

def queryUserBalance(user_id):

    if not users_table_setup():
        create_users_table()
        USERS_TABLE_IS_SETUP = True
    
    query_statement = "SELECT BALANCE FROM USERS WHERE USER_ID = ?"
    BALANCE_INDEX = 0
    CURSOR.execute(query_statement, (user_id,))
    result = CURSOR.fetchone()

    if result == None:
        appendToUserTable(user_id)

        CURSOR.execute(query_statement, (user_id,))
        balance = CURSOR.fetchone()[BALANCE_INDEX]
        return balance
    
    return result[BALANCE_INDEX]

def updateUserBalance(user_id, balance):

    update_statement = "UPDATE USERS SET BALANCE = ? WHERE USER_ID = ?"
    CURSOR.execute(update_statement, (balance, user_id))
    CONNECTION.commit()

def removeFromUserDatabase(user_id):

    remove_statement = "DELETE FROM USERS WHERE USER_ID = ?"
    CURSOR.execute(remove_statement, (user_id))
    CONNECTION.commit()
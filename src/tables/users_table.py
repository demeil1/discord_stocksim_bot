from .database_globals import *

def createUsersTable():
    
    create_table_statement = '''CREATE TABLE IF NOT EXISTS USERS (
        USER_ID INTEGER PRIMARY KEY,
        BALANCE INTEGER
    )'''
    CURSOR.execute(create_table_statement)

def appendToUserTable(user_id):

    append_statement = '''INSERT INTO USERS (
        USER_ID,
        BALANCE
    ) VALUES (?,?)'''

    STARTING_BALANCE = 10000
    CURSOR.execute(append_statement, (user_id, STARTING_BALANCE))
    CONNECTION.commit()

def queryUserBalance(user_id):

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
    CURSOR.execute(remove_statement, (user_id,))
    CONNECTION.commit()

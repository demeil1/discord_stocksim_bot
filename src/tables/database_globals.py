import sqlite3

# database setup

CONNECTION = sqlite3.connect("STOCKSIM.db", check_same_thread=False)
CURSOR = CONNECTION.cursor()

# database cleanup

def databaseCleanup():
    CURSOR.close()
    CONNECTION.close()

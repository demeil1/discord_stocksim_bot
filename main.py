from src.bot_config import *
from src.bot import *
from src.tables.users_table import createUsersTable
from src.tables.stocks_table import createStockTable
from src.tables.shorts_table import createShortsTable
from src.tables.options_table import createOptionsTable
from src.tables.database_globals import databaseCleanup
from src.bot_config import INTEREST_RATE, STARTING_BALANCE

def main():
    if ((not (type(INTEREST_RATE) == int) and 
        (not type(INTEREST_RATE) == float)) or 
        (INTEREST_RATE <= 0)):
        print("src/bot_config.py's:\n\n"\
              "INTEREST_RATE must be a of type float or int, "\
              "it also must be > 0.")
        return
    if ((not (type(STARTING_BALANCE) == int) and 
        (not type(STARTING_BALANCE) == float)) or 
        (STARTING_BALANCE <= 0)):
        print("src/bot_config.py's:\n\n"\
              "STARTING_BALANCE must be a of type float or int, "\
              "it also must be > 0.")
        return
    createUsersTable()
    createStockTable()
    createShortsTable()
    createOptionsTable()
    CLIENT.run(TOKEN)
    databaseCleanup()


main()

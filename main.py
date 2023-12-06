from databases.users_table import createUsersTable
from databases.stocks_table import createStockTable
from databases.updating import createUpdatingTable, updateUpdatingTableStocks
from bot_config import *
from bot import *
from databases.timing import marketHours
from databases.database_globals import databaseCleanup

def main():

    createUsersTable()
    createStockTable()
    createUpdatingTable()

    # while True:
        # if not marketHours():
            # pass
        # updateUpdatingTableStocks
    CLIENT.run(TOKEN)

    databaseCleanup()

main()

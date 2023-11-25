from databases.users_table import createUsersTable
from databases.stocks_table import createStockTable
from bot_config import *
from bot import *
from databases.timing import marketHours
from databases.database_globals import databaseCleanup

def main():

    createUsersTable()
    createStockTable()

    # while True:
        # if not marketHours():
            # pass
        # updateStockPrices
    CLIENT.run(TOKEN)

    databaseCleanup()

main()
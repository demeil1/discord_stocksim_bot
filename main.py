from bot_config import *
from bot import *
from databases.timing import marketHours
from databases.users_table import createUsersTable
from databases.stocks_table import createStockTable
from databases.shorts_table import createShortsTable
from databases.database_globals import databaseCleanup

def main():

    createUsersTable()
    createStockTable()
    createShortsTable()

    # while True:
        # if not marketHours():
            # pass
    CLIENT.run(TOKEN)

    databaseCleanup()

main()

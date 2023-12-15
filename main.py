from src.bot_config import *
from src.bot import *
from src.utils.timing import marketHours
from src.tables.users_table import createUsersTable
from src.tables.stocks_table import createStockTable
from src.tables.shorts_table import createShortsTable
from src.tables.database_globals import databaseCleanup

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

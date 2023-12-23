from src.bot_config import *
from src.bot import *
from src.tables.users_table import createUsersTable
from src.tables.stocks_table import createStockTable
from src.tables.shorts_table import createShortsTable
from src.tables.options_table import createOptionsTable
from src.tables.database_globals import databaseCleanup

def main():
    createUsersTable()
    createStockTable()
    createShortsTable()
    createOptionsTable()
    CLIENT.run(TOKEN)
    databaseCleanup()

if __name__ == "main":
    main()

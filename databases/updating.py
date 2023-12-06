from .database_globals import *
from .yf_scraper import scrape

def createUpdatingTable():
    
    create_table_statement = f'''CREATE TABLE IF NOT EXISTS UPDATING (
        TICKER TEXT, 
        CUR_PRICE INTEGER
    )'''
    CURSOR.execute(create_table_statement)

def setUpdatingTableStocks():

    stock_table_tickers = queryDistinctStock()
    if not stock_table_tickers:
        return
    updating_table_tickers = queryUpdatingTableStocks()
    
    stock_table_tickers = set(stock_table_tickers)
    updating_table_tickers = set(updating_table_tickers)
    
    tickers_to_add = stock_table_tickers.difference(updating_table_tickers)
    tickers_to_remove = updating_table_tickers.difference(stock_table_tickers)

    if tickers_to_add:
        ticker_values = scrape(ticker_to_add)
        ticker_value_zip = zip(tickers_to_add, ticker_values)
        for ticker, value in ticker_value_zip:
            appendToUpdatingTable(ticker, value)
    if tickers_to_remove:
        for ticker in tickers_to_remove:
            removeFromUpdatingTable(ticker):

def appendToUpdatingTable(ticker, value):

    append_statement = '''INSERT INTO UPDATING (
        TICKER,
        CUR_PRICE
    )'''
    CURSOR.execute(append_statement, (ticker, value,))
    CONNECTION.commit()

def removeFromUpdatingTable(ticker):

    remove_statement = "DELETE FROM UPDATING WHERE TICKER = ?"
    CURSOR.execute(remove_statement, (ticker,))
    CONNECTION.commit()
    
def updateUpdatingTableStocks():

    distinct_tickers = queryUpdatingTableStocks() 
    ticker_values = scrape(distinct_tickers)
    pass # finish later

def queryUpdatingTableStocks():

    query_statement = "SELECT TICKER FROM UPDATING"
    CURSOR.execute(query_statement)
    tickers = CURSOR.fetchall()
    return tickers


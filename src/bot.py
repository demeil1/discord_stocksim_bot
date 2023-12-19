from .bot_config import *
from .buying import buyStock, delBuyStock
from .selling import sellStock, delSellStock
from .shorting import shortStock, coverShort, checkShortPositions
from .options import optionStock, checkOptionPositions
from .utils.ids import userIdToString
from .utils.yf_scraper import getValue, calculateOptionPremium
from .tables.stocks_table import queryUserStock, querySpecificUserStock
from .tables.users_table import queryUserBalance
from .tables.shorts_table import queryUserShorts, querySpecificUserShorts
from .tables.options_table import queryUserOptions, querySpecificUserOptions
from .networth import calculateUserNetWorth
# from commands import buying, selling, options, shorting, pichart, leaderboard

@CLIENT.event
async def on_ready(): 

    sync = await CLIENT.tree.sync()
    print(f"\nSynced {len(sync)} command(s)")
    print(f"\nSuccessful: We have logged in as {CLIENT.user}")
    checkStaleShorts.start()
    checkStaleOptions.start()

@tasks.loop(seconds = 3.0)
async def checkStaleShorts():
    checkShortPositions()

@tasks.loop(seconds = 3.0)
async def checkStaleOptions():
    checkOptionPositions()

@CLIENT.tree.command(description="buy [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker="ticker:",
                       num_shares="# of shares:")
async def buy(interaction: discord.Interaction, 
              ticker: str, 
              num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    user_id = userIdToString(interaction.user.id)
    result = buyStock(user_id, parsed_message)
    await interaction.response.send_message(result)

#fix commands below and set them up in the correct guild

@CLIENT.tree.command(description = "target price buy [ticker: text] [# of shares: integer] [low: decimal] [high: decimal]")
@app_commands.describe(ticker = "ticker:",
                       num_shares = "# of shares:", 
                       tp_low = "low target price:", 
                       tp_high = "high target price:")
async def delbuy(interaction: discord.Interaction,
                 ticker: str,
                 num_shares: int,
                 tp_low: float,
                 tp_high: float):

    parsed_message = [ticker.upper(), num_shares, tp_low, tp_high]
    user_id = userIdToString(interaction.user.id)
    result = delBuyStock(user_id, parsed_message)
    await interaction.response.send_message(f"{interaction.user.mention} " + result)

@CLIENT.tree.command(description = "sell [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:", 
                       num_shares = "# of shares:")
async def sell(interaction: discord.Interaction,
               ticker: str,
               num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    user_id = userIdToString(interaction.user.id)
    result = sellStock(user_id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "target price sell [ticker: text] [# of shares: integer] [low: decimal] [high: decimal]")
@app_commands.describe(ticker = "ticker:", 
                       num_shares = "# of shares:", 
                       tp_low = "low target price:", 
                       tp_high = "high target price:")
async def delsell(interaction: discord.Interaction,
                  ticker: str,
                  num_shares: int,
                  tp_low: float,
                  tp_high: float):

    parsed_message = [ticker.upper(), num_shares, tp_low, tp_high]
    user_id = userIdToString(interaction.user.id)
    result = delSellStock(user_id, parsed_message)
    await interaction.response.send_message(f"{interaction.user.mention} " + result)

@CLIENT.tree.command(description = "short [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:",
                       num_shares = "# of shares:",
                       stop_loss = "stop loss:")
async def short(interaction: discord.Interaction,
                ticker: str,
                num_shares: int,
                stop_loss: float):

    # await interaction.response.defer()
    parsed_message = [ticker.upper(), num_shares, stop_loss]
    user_id = userIdToString(interaction.user.id)
    result = shortStock(user_id, parsed_message)
    await interaction.response.send_message(result)
    # await interaction.followup.send(result)

@CLIENT.tree.command(description = "cover shorted [transaction: id]")
@app_commands.describe(transac_id = "transaction id:")
async def cover(interaction: discord.Interaction,
                transac_id: str):

    parsed_message = [transac_id]
    user_id = userIdToString(interaction.user.id)
    result = coverShort(user_id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "view option premium before purchasing")
@app_commands.describe(ticker = "ticker:",
                       expiration_days = "days until contract expires")
async def premium(interaction: discord.Interaction,
                  ticker: str,
                  expiration_days: int):
    interest_rate = 0.02
    strike_price = getValue([ticker.upper()])
    result = calculateOptionPremium(ticker.upper(), strike_price, expiration_days, interest_rate)
    if result:
        await interaction.response.send_message(f"{ticker.upper()}'s Premium: ${result:.2f}")
        return
    await interaction.response.send_message(f"Task Terminated: Error finding {ticker.upper()}'s premium")
    
@CLIENT.tree.command(description = "call [ticker: text] [# of shares: integer] [expiration days: integer]")
@app_commands.describe(ticker = "ticker:",
                       num_shares = "# of shares:",
                       expiration_days = "expiration days")
async def call(interaction: discord.Interaction,
               ticker: str,
               num_shares: int,
               expiration_days: int):
    
    interest_rate = 0.02
    parsed_message = [ticker.upper(), num_shares, expiration_days, interest_rate, "call"]
    user_id = userIdToString(interaction.user.id)
    result = callStock(user_id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "put [ticker: text] [# of shares: integer] [expiration days: integer]")
@app_commands.describe(ticker = "ticker:",
                       num_shares = "# of shares:",
                       expiration_days = "expiration days")
async def put(interaction: discord.Interaction,
               ticker: str,
               num_shares: int,
               expiration_days: int):
    
    interest_rate = 0.02
    parsed_message = [ticker.upper(), num_shares, expiration_days, interest_rate, "put"]
    user_id = userIdToString(interaction.user.id)
    result = putStock(user_id, parsed_message)
    await interaction.response.send_message(result)
    
@CLIENT.tree.command(description = "returns transactions of all purchases or purchases of specified tickers")
@app_commands.describe(tickers = "enter '*' for all transactions or ticker(s) seperated by spaces for specific ones")      
async def query(interaction: discord.Interaction,
                tickers: str):

    transacs = ""
    user_id = userIdToString(interaction.user.id)
    if tickers == "*":
        stocks_result = queryUserStock(user_id)
        shorts_result = queryUserShorts(user_id)
        options_result = queryUserOptions(user_id)
        
        transacs += "----- Stocks Owned -----\n\n"
        if stocks_result == None:
            transacs += "It's empty in here... Nothing in stocks database\n"
        else:
            for t in stocks_result:
                transacs += f"('{t[2]}', {t[3]}, {t[4]:.2f}, '{t[5]}', '{t[6]}', '{t[7]}')\n"

        transacs += "\n----- Short Positions -----\n\n"
        if shorts_result == None:
            transacs += "It's empty in here... Nothing in shorts database\n"
        else:
            for t in shorts_result:
                transacs += f"('{t[1]}', {t[2]}', {t[3]}, {t[4]:.2f}, {t[5]:.2f}, '{t[6]}', '{t[7]}', '{t[8]}')\n"

        transacs += "\n----- Option Contracts -----\n\n"
        if options_result == None:
            transacs += "It's empty in here... Nothing in options database\n"
        else:
            for t in options_result:
                transacs += f"('{t[1]}', {t[2]}', {t[3]}, {t[4]:.2f}, {t[5]:.2f}, '{t[6]:.2f}', '{t[7]}', '{t[8]}', '{t[9]}')\n"
    else:
        stocks_str = "----- Stocks Owned -----\n\n"
        shorts_str = "----- Short Positions -----\n\n"
        options_str = "----- Option Contracts -----\n\n"

        tickers = tickers.strip().split()
        for ticker in tickers:
            stocks_result = querySpecificUserStock(user_id, ticker.upper())
            shorts_result = querySpecificUserShorts(user_id, ticker.upper())
            options_result = querySpecificUserOptions(user_id, ticker.upper())

            if not stocks_result:
                stocks_str += f"\nNo {ticker.upper()} shares owned\n"
            else:
                for t in stocks_result:
                    stocks_str += f"('{t[2]}', {t[3]}, {t[4]:.2f}, '{t[5]}', '{t[6]}', '{t[7]}')\n"

            if not shorts_result:
                shorts_str += f"\nNo {ticker.upper()} short positions\n"
            else:
                for t in shorts_result:
                    shorts_str += f"('{t[1]}', '{t[2]}', {t[3]}, {t[4]:.2f}, {t[5]:.2f}, '{t[6]}', '{t[7]}', '{t[8]}')\n"

            if not options_result:
                options_str += f"\nNo {ticker.upper()} option contracts\n"
            else:
                for t in options_str:
                    options_str += f"('{t[1]}', '{t[2]}', {t[3]}, {t[4]:.2f}, {t[5]:.2f}, '{t[6]}', '{t[7]}', '{t[8]}')\n"

        transacs = stocks_str + "\n" + shorts_str + "\n" + options_str
    await interaction.response.send_message(transacs)

@CLIENT.tree.command(description = "returns your current balance")
async def balance(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    balance = queryUserBalance(user_id)
    await interaction.response.send_message(f"{interaction.user}'s balance: ${balance:.2f}")

@CLIENT.tree.command(description = "returns your net worth")
async def networth(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    networth = calculateUserNetWorth(user_id)
    await interaction.response.send_message(f"{interaction.user}'s networth: ${networth:.2f}")

from bot_config import *
from buying import buyStock, delBuyStock
from selling import sellStock, delSellStock
from shorting import shortStock, coverShort, checkShortPositions
from databases.ids import userIdToString
from databases.stocks_table import queryUserStock, querySpecificUserStock
from databases.users_table import queryUserBalance
from databases.shorts_table import queryUserShorts, querySpecificUserShorts
from networth import calculateUserNetWorth
# from commands import buying, selling, options, shorting, pichart, leaderboard

@CLIENT.event
async def on_ready(): 

    sync = await CLIENT.tree.sync()
    print(f"\nSynced {len(sync)} command(s)")
    print(f"\nSuccessful: We have logged in as {CLIENT.user}")
    checkStaleShorts.start()

@tasks.loop(seconds = 3.0)
async def checkStaleShorts():
    await checkShortPositions()

@CLIENT.tree.command(description="buy [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker="ticker",
                       num_shares="# of shares")
async def buy(interaction: discord.Interaction, 
              ticker: str, 
              num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    user_id = userIdToString(interaction.user.id)
    result = await buyStock(user_id, parsed_message)
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
    result = await delBuyStock(user_id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "sell [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:", 
                       num_shares = "# of shares:")
async def sell(interaction: discord.Interaction,
               ticker: str,
               num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    user_id = userIdToString(interaction.user.id)
    result = await sellStock(user_id, parsed_message)
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
    result = await delSellStock(user_id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "short [ticker: text] [# of shares]")
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
    result = await shortStock(user_id, parsed_message)
    await interaction.response.send_message(result)
    # await interaction.followup.send(result)

@CLIENT.tree.command(description = "cover shorted [transaction: id]")
@app_commands.describe(transac_id = "transaction id:")
async def cover(interaction: discord.Interaction,
                transac_id: str):

    parsed_message = [transac_id]
    user_id = userIdToString(interaction.user.id)
    result = await coverShort(user_id, parsed_message)
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
    else:
        stocks_str = "----- Stocks Owned -----\n\n"
        shorts_str = "----- Short Positions -----\n\n"

        tickers = tickers.strip().split()
        for ticker in tickers:
            stocks_result = querySpecificUserStock(user_id, ticker.upper())
            shorts_result = querySpecificUserShorts(user_id, ticker.upper())

            if stocks_result == None:
                stocks_str += f"\nNo {ticker.upper()} shares owned\n"
            else:
                for t in stocks_result:
                    stocks_str += f"('{t[2]}', {t[3]}, {t[4]:.2f}, '{t[5]}', '{t[6]}', '{t[7]}')\n"

            if shorts_result == None:
                shorts_str += f"\nNo {ticker.upper()} short positions\n"
            else:
                for t in shorts_result:
                    shorts_str += f"('{t[1]}', '{t[2]}', {t[3]}, {t[4]:.2f}, {t[5]:.2f}, '{t[6]}', '{t[7]}', '{t[8]}')\n"
        transacs = stocks_str + "\n" + shorts_str
    await interaction.response.send_message(transacs)

@CLIENT.tree.command(description = "returns your current balance")
async def balance(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    balance = queryUserBalance(user_id)
    await interaction.response.send_message(f"{interaction.user}'s balance: ${balance:.2f}")

@CLIENT.tree.command(description = "returns your net worth")
async def networth(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    networth = await calculateUserNetWorth(user_id)
    await interaction.response.send_message(f"{interaction.user}'s networth: ${networth:.2f}")

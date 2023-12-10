from bot_config import *
from buying import buyStock, delBuyStock
from selling import sellStock, delSellStock
from shorting import shortStock, coverShort
from databases.ids import userIdToString
from databases.stocks_table import queryUserStock, querySpecificUserStock
from databases.users_table import queryUserBalance
from networth import calculateUserNetWorth
# from commands import buying, selling, options, shorting, pichart, leaderboard

@CLIENT.event
async def on_ready(): 

    sync = await CLIENT.tree.sync()
    print(f"\nSynced {len(sync)} command(s)")
    print(f"\nSuccessful: We have logged in as {CLIENT.user}")

@CLIENT.tree.command(description="buy [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker="ticker",
                       num_shares="# of shares")
async def buy(interaction: discord.Interaction, 
              ticker: str, 
              num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    result = await buyStock(interaction.user.id, parsed_message)
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
    result = await delBuyStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "sell [ticker: text] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:", 
                       num_shares = "# of shares:")
async def sell(interaction: discord.Interaction,
               ticker: str,
               num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    result = await sellStock(interaction.user.id, parsed_message)
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
    result = await delSellStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "short [ticker: text] [# of shares]")
@app_commands.describe(ticker = "ticker:",
                       num_shares = "# of shares:",
                       stop_loss = "stop loss:")
async def short(interaction: discord.Interaction,
                ticker: str,
                num_shares: int,
                stop_loss: float):

    parsed_message = [ticker.upper(), num_shares, stop_loss]
    result = await shortStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "cover shorted [transaction: id]")
@app_commands.describe(transac_id = "transaction id:")
async def cover(interaction: discord.Interaction,
                transac_id: str):

    parsed_message = [transac_id]
    result = await coverShort(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "returns transactions of all purchases or purchases of specified tickers")
@app_commands.describe(tickers = "enter '*' for all transactions or ticker(s) seperated by spaces for specific ones")      
async def query(interaction: discord.Interaction,
                tickers: str):

    transacs = ""
    user_id = userIdToString(interaction.user.id)
    if tickers == "*":
        result = queryUserStock(user_id)
        if result == None:
            result = "It's empty in here... Nothing in your database"
            await interaction.response.send_message(result)
            return
        
        for t in result:
            transacs += f"{t[1:]}\n"
    else:
        tickers = tickers.strip().split()
        for ticker in tickers:
            result = querySpecificUserStock(user_id, ticker.upper())

            if result == None:
                result = f"\n----- No {ticker.upper()} shares owned -----\n\n"
                transacs += result
                   
            for t in result:
                transacs += f"{t[1:]}\n"

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

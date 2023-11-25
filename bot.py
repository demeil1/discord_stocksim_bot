from bot_config import *
from buying import buyStock, delBuyStock
from selling import sellStock, delSellStock
from databases.ids import userIdToString
from databases.stocks_table import queryUserStock
from databases.users_table import queryUserBalance
# from commands import buying, selling, options, shorting, pichart, leaderboard

@CLIENT.event
async def on_ready(): 

    sync = await CLIENT.tree.sync()
    print(f"\nSynced {len(sync)} command(s)")
    print(f"\nSuccessful: We have logged in as {CLIENT.user}")

@CLIENT.tree.command(description="buy [ticker: string] [# of shares: integer]")
@app_commands.describe(ticker="ticker",
                       num_shares="# of shares")
async def buy(interaction: discord.Interaction, 
              ticker: str, 
              num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    result = await buyStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

#fix commands below and set them up in the correct guild

@CLIENT.tree.command(description = "target price buy [ticker] [# of shares: integer] [low: decimal] [high: decimal]")
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

@CLIENT.tree.command(description = "sell [ticker] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:", 
                       num_shares = "# of shares:")
async def sell(interaction: discord.Interaction,
               ticker: str,
               num_shares: int):

    parsed_message = [ticker.upper(), num_shares]
    result = await sellStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

@CLIENT.tree.command(description = "target price sell [ticker] [# of shares: integer] [low: decimal] [high: decimal]")
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

@CLIENT.tree.command(description = "return all stocks owned")
# @app_commands(tickers = "ticker(s) to search seperated by space")       need to allow querying for multiple but not all stocks
async def query(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    results = queryUserStock(user_id)
    if results == None:
        result = "It's empty in here... Nothing in your database"
    
    transacs = ""
    for t in results:
        transacs += f"{t[2:]}\n"
    await interaction.response.send_message(transacs)

@CLIENT.tree.command(description = "returns your current balance")
async def balance(interaction: discord.Interaction):

    user_id = userIdToString(interaction.user.id)
    balance = queryUserBalance(user_id)
    await interaction.response.send_message(f"{interaction.user}'s balance = $ {balance:.2f}")

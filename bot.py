from bot_config import *
from buying import buyStock, delBuyStock
from selling import sellStock, delSellStock
from databases.ids import userIdToString
from databases.stocks_table import queryUserStock
from databases.users_table import queryUserBalance
# from commands import buying, selling, options, shorting, pichart, leaderboard

def parse_message(message):

    message = message.strip().split()
    return message

@CLIENT.event
async def on_ready(): 
    # Synchronize commands
    sync = await CLIENT.tree.sync()
    print(f"\nSynced {len(sync)} command(s)")
    print(f"\nSuccessful: We have logged in as {CLIENT.user}\n")

@CLIENT.tree.command(description="buy [ticker: string] [# of shares: integer]")
@app_commands.describe(ticker="ticker", num_shares="# of shares")
async def buy(interaction: discord.Interaction, ticker: str, num_shares: int):

    parsed_message = [ticker, num_shares]
    result = await buyStock(interaction.user.id, parsed_message)
    await interaction.response.send_message(result)

#fix commands below and set them up in the correct guild

@CLIENT.command(description = "target price buy [ticker] [# of shares: integer] [low: decimal] [high: decimal]")
@app_commands.describe(ticker = "ticker:", num_shares = "# of shares:", tp_low = "low target price:", tp_high = "high target price:")
async def delbuy(ctx, *, message: str):

    parsed_message = parse_message(message)
    result = await delBuyStock(ctx.author.id, parsed_message)
    await ctx.reply(result)

@CLIENT.command(description = "sell [ticker] [# of shares: integer]")
@app_commands.describe(ticker = "ticker:", num_shares = "# of shares:")
async def sell(ctx, *, message: str):

    parsed_message = parse_message(message)
    result = await sellStock(ctx.author.id, parsed_message)
    await ctx.reply(result)

@CLIENT.command(description = "target price sell [ticker] [# of shares: integer] [low: decimal] [high: decimal]")
@app_commands.describe(ticker = "ticker:", num_shares = "# of shares:", tp_low = "low target price:", tp_high = "high target price:")
async def delsell(ctx, *, message: str):

    parsed_message = parse_message(message)
    result = await delSellStock(ctx.author.id, parsed_message)
    await ctx.reply(result)

@CLIENT.command(description = "return all stocks owned")
async def query(ctx):

    user_id = userIdToString(ctx.author.id)
    result = queryUserStock(user_id)
    if result == None:
        result = "It's empty in here... Nothing in your database"
    await ctx.reply(result)

@CLIENT.command(description = "returns your current balance")
async def balance(ctx):

    user_id = userIdToString(ctx.author.id)
    balance = queryUserBalance(user_id)
    await ctx.reply(f"{ctx.author}'s balance = {balance:.2f}")

CLIENT.run(TOKEN)
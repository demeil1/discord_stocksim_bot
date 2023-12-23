import discord
from discord import app_commands
from discord.ext import commands, tasks

# bot setup

TOKEN = "" # add discord bot token between quotation marks 
INTENTS = discord.Intents.all()
INTENTS.message_content = True
INTENTS.members = True
CLIENT = commands.Bot(command_prefix="$", intents=INTENTS)

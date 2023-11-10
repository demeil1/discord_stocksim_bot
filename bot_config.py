# HAVE TO CREATE A COVER COMMAND THAT ALLOWS USERS TO COVER SHORT PSNs
# HAVE TO CREATE A COMMAND THAT ALLOWS YOU TO EXEC YOUR OPTION

import discord
from discord import app_commands
from discord.ext import commands

# bot setup 

TOKEN                   = "MTE2NTc4MDc3OTQ5OTAwODA3MA.GsQL33.tAGZhS5g83gku_0VYfFLw2kRY2k2-GKovefY90"
INTENTS                 = discord.Intents.all()
INTENTS.message_content = True
CLIENT                  = commands.Bot(command_prefix='$', intents=INTENTS)

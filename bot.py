import disnake
from data.settings import *
from logging import *
from disnake.ext import commands

basicConfig(level=INFO)
bot = commands.InteractionBot()

@bot.event
async def on_ready():
    debug('Bot is ready')

bot.load_extensions('cogs')

if __name__ == "__main__":
    bot.run(TOKEN)

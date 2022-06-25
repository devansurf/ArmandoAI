import os
import discord
from discord.ext import commands
from modules import stalk as s
from modules import read_channel as r
from dotenv import load_dotenv

#Setup
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = commands.Bot(command_prefix='$')

@bot.command()
async def stalk(ctx, username):
    await s.stalk(ctx, username)

@bot.command()
async def read(ctx):
    await r.read_channel(ctx)

@bot.event
async def on_ready():
    print("{0.user} is now online!".format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello, I am ArmandoBot.')

    await bot.process_commands(message)

bot.run(TOKEN)

# if __name__ == "__main__":
#     main()

import os
import discord
from discord.ext import commands
from modules import stats as s
from modules import read_channels as r
from modules import tf
from dotenv import load_dotenv

#Setup
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = commands.Bot(command_prefix='$')

@bot.command()
async def train(ctx, epochSize):
    if ctx.author.guild_permissions.administrator:
        await tf.trainAI(ctx, epochSize)

@bot.command()
async def predict(ctx, *, inp):
    await tf.predict(ctx, inp)

@bot.command()
async def stats(ctx, *, username):
    await s.stats(ctx, username)

@bot.command()
async def read(ctx):
    await r.read_channels(ctx)

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

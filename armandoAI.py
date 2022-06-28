import asyncio
import os
import time
from discord.ext import commands
from modules import stats as s
from modules import read_channels as r
from modules import anim as a
from modules import tf
from modules import help as h
from dotenv import load_dotenv

#Setup
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = commands.Bot(command_prefix='$')
@bot.command()
async def train(ctx, epochSize):
    if ctx.author.guild_permissions.administrator:
        deltaTime = time.time()
        msg = "Training ArmandoBot..."
        m = await a.roboMessage(ctx, msg)
        await tf.trainAI(ctx, epochSize)
        await m.edit(content = "Training Completed in: " + str((time.time()-deltaTime)/60.0) + " minutes.")

@bot.command()
async def predict(ctx, *, text):
    deltaTime = time.time()
    msg = "Calculating Prediction..."
    m = await a.roboMessage(ctx, msg)
    await tf.predict(ctx, text)
    await m.edit(content = "Prediction Completed in: " + str(time.time()-deltaTime) + " seconds.")

@bot.command()
async def stats(ctx, *, username):
    loading_anim = asyncio.create_task(a.loading(ctx, "Computing Stats")) 
    await s.stats(ctx, username)
    loading_anim.cancel()

@bot.command()
async def read(ctx):
    if ctx.author.guild_permissions.administrator:
        loading_anim = asyncio.create_task(a.loading(ctx, "Reading Channel Text")) 
        await r.read_channels(ctx)
        loading_anim.cancel()

@bot.event
async def on_ready():
    print("{0.user} is now online!".format(bot))

bot.run(TOKEN)


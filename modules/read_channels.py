import os
import asyncio
import pickle
from modules import utils as u
CACHE = './cache'
HISTORY = './history'
CACHE_DIRECTORY = './cache/{channel}.txt'
HISTORY_DIRECTORY = './history/{channel}.txt'



def storeData(ctx, messages):
    mCache = open(CACHE_DIRECTORY.format(channel = ctx.guild.id), 'wb')
    pickle.dump(messages,mCache)
    mCache.close()

def loadData(ctx):
    messages = []
    mCache = open(CACHE_DIRECTORY.format(channel = ctx.guild.id), 'rb')
    messages = pickle.load(mCache)
    if len(messages) == 0:
       read_channels(ctx)
       messages = pickle.load(mCache)
        
    mCache.close()
    return messages

def writeData(ctx, messages):
    file = open(HISTORY_DIRECTORY.format(channel = ctx.guild.id), 'w')
    for message in messages:
        file.write("\n" + message["name"] + "\n" + message["content"]+"\n")
    file.close()

async def read_channels(ctx):
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(HISTORY, exist_ok=True)
    messages = []
    #sort text channels by date
    channels = ctx.guild.text_channels
    channels.sort(key=lambda x: x.created_at.date(), reverse=True)

    for channel in channels:
        async for message in channel.history(limit = None):
            #validate that the message meets some parameters     
            #extract the important details of the message to store
            if not u.isSpam(message):
                messages.append({"name" : message.author.name, "content" : message.content, "date":  message.created_at.strftime("%d %B, %Y")})

    storeData(ctx,messages)
    writeData(ctx,messages)
    
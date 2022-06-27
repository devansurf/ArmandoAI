import asyncio
import pickle
from modules import anim as a
from modules import utils as u

MCACHE_DIRECTORY = 'cache/messageCache'
WRITE_DIRECTORY = 'channel_history.txt'

def storeData(messages):
    mCache = open(MCACHE_DIRECTORY, 'wb')
    pickle.dump(messages,mCache)
    mCache.close()

def loadData(ctx):
    messages = []
    mCache = open(MCACHE_DIRECTORY, 'rb')
    messages = pickle.load(mCache)
    if len(messages) == 0:
       read_channels(ctx)
       messages = pickle.load(mCache)
        
    mCache.close()
    return messages

def writeData(messages):
    file = open(WRITE_DIRECTORY, 'w')
    for message in messages:
        file.write("\n" + message["name"] + "\n" + message["content"]+"\n")
    file.close()

async def read_channels(ctx):
    messages = []
    channels = ctx.guild.text_channels
    loading_anim = asyncio.create_task(a.loading(ctx, "Reading Channel Text")) 
    for channel in channels:
        async for message in channel.history(limit = None):
            #validate that the message meets some parameters     
            #extract the important details of the message to store
            if not u.isSpam(message):
                messages.append({"name" : message.author.name, "content" : message.content, "date":  message.created_at.strftime("%d %B, %Y")})
    loading_anim.cancel()

    storeData(messages)
    writeData(messages)
    
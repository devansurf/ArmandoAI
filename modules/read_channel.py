import pickle
from modules import anim as a

DIRECTORY = 'cache/messageCache'
def storeData(messages):
    mCache = open(DIRECTORY, 'wb')
    pickle.dump(messages,mCache)
    mCache.close()

def loadData(ctx):
    messages = []
    mCache = open(DIRECTORY, 'rb')
    messages = pickle.load(mCache)
    if len(messages) == 0:
       read_channel(ctx)
       messages = pickle.load(mCache)
        
    mCache.close()
    return messages

async def read_channel(ctx):
    messages = []
    channel = ctx.channel
    await a.loading(ctx, "bruh")
    async for message in channel.history(limit = None):
        #validate that the message meets some parameters     
        #extract the important details of the message to store
        messages.append({"name" : message.author.name, "content" : message.content})
        print(message.content)
    storeData(messages)
    
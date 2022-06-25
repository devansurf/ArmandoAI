from datetime import datetime
import time
from modules import read_channel as r

def validateMessage(message,username):
    valid = True
 
    #Check if the author is valid
    if message["name"].lower() != username.lower():
        return False

    #check if content is empty
    if not message["content"]:
        return False

    #Check if the message is valid and ignores commands
    blacklist = ['$', '/', '!']
    for e in blacklist:
        if message["content"].startswith(e):
            return False
  
    return valid

async def stalk(ctx, username):
    channel = ctx.channel
    messages = r.loadData(ctx)
    deltaTime = time.time()
    count = 0

    #loop through all the channel's messages
    for message in messages:
        print(message)
        if validateMessage(message,username):
            count += 1

    await channel.send(username + " has said stuff " + str(count) + " times\n Time of execution: " + str(time.time()-deltaTime))
    print(count)
    print(messages)
    # user = ctx.author
    # await ctx.channel.send("saludos desde Guatemala" + str(ctx.author.name.lower() == username.lower()))
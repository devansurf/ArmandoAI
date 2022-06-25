
def validateMessage(message,username):
    valid = True

    #Check if the author is valid
    if message.author.name.lower() != username.lower():
        return False

    #Check if the message is valid and ignores commands
    blacklist = ['$', '/', '!']
    for e in blacklist:
        if message.content.startswith(e):
            return False
    #Check if the message is an image
    if message.attachments:
        return False

    return valid

async def stalk(ctx, username):
    channel = ctx.channel
    messages = []
    
    async for message in channel.history(limit=200):
        if validateMessage(message,username):
            messages.append(message)
    print(messages)
    await channel.send("Searching back 200 messages, " + username + " said " + messages[len(messages)-1].content)
    # user = ctx.author
    # await ctx.channel.send("saludos desde Guatemala" + str(ctx.author.name.lower() == username.lower()))
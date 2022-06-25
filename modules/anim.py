import time

async def loading(ctx, txt):
    count = 0
    print("hello!/")
    message = await ctx.channel.send(str(count))
    while count < 10:
        deltaTime = time.time()
        await message.edit(content = str(count))
        deltaTime = time.time() - deltaTime
        time.sleep(1 - deltaTime)
        count += 1
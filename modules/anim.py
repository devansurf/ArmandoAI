import asyncio
import random
import time

anim_tick = 1
loading_anim_array = ["[========]",
                      "[+=======]",
                      "[++======]",          
                      "[+++=====]",          
                      "[++++====]",          
                      "[+++++===]",          
                      "[++++++==]",
                      "[+++++++=]",          
                      "[++++++++]",          
                      "[=+++++++]",          
                      "[==++++++]",
                      "[===+++++]",
                      "[====++++]",          
                      "[=====+++]",          
                      "[======++]",          
                      "[=======+]"]
roboGifs = ['https://tenor.com/bc91Z.gif', 
            'https://tenor.com/bE1Qx.gif',
            'https://tenor.com/bTbe6.gif',
            'https://tenor.com/pEhE.gif']

async def roboMessage(ctx, msg):
    #Select random gif and send
    rand = random.randint(0,len(roboGifs)-1)
    m = await ctx.channel.send(content = msg + "\n" + roboGifs[rand])
    return m

async def loading(ctx, txt):
    frame = 0
    globalTime = time.time()
    message = await ctx.channel.send(txt)
    try:   
        while True:
            deltaTime = time.time()
            await message.edit(content = txt + " " + loading_anim_array[frame % len(loading_anim_array)])
            deltaTime = time.time() - deltaTime
            await asyncio.sleep(abs(anim_tick) - deltaTime)
            frame += 1
    except asyncio.CancelledError:
        await message.edit(content = "Task: '" + txt + "' completed with an execution time of: " + str(time.time()-globalTime) + " seconds.")
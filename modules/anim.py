import asyncio
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
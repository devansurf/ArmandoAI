import discord
from discord.ext import commands
from modules import stalk as s



# def main():
TOKEN = ""
bot = commands.Bot(command_prefix='$')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def stalk(ctx, username):
    await s.stalk(ctx, username)

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

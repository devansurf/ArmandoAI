import asyncio
from datetime import datetime
import time, discord
from modules import anim as a
from modules import read_channel as r
from modules import utils as u

def validateMessage(message,username):
    valid = True
 
    #Check if the author is valid
    if message["name"].lower() != username.lower():
        return False

    #check if content is empty
    if not message["content"]:
        return False

    #Check if the message is valid and ignores commands
    blacklist = ['$', '/', '!', '-']
    for e in blacklist:
        if message["content"].startswith(e):
            return False
    return valid

#collect any relevant data found within the messages, returns a formatted string
def findData(messages, username):
    #get the count
    mNum = len(messages)
    #find the top 10 favorite words
    wordList = {}
    for message in messages:
        split_sentence = message["content"].split()
        #fill out dictionary with occurrences of each word
        for word in split_sentence:
            if word in wordList:
                wordList[word] += 1
            else:
                wordList[word] = 1
    #sort the wordList
    preposition_list = u.fetch_preposition_words()
    most_used_words = []
    top_ten = ""
    for k, v in sorted(wordList.items(), key=lambda item: item[1], reverse = True):
        if not k in preposition_list:
            most_used_words.append([k,v])

    top_ten = u.words_to_string(most_used_words, 10)

    #first message sent with date
    first_message = messages[len(messages)-1]
    fMes = first_message["content"]
    fDate = first_message["date"]
    fMes = fMes + "\n\nsent on: " + fDate

    #indecent words said
    indecent_words = {}
    indecent_word_count = 0
    most_used_indecent_words = []
    profaned_list = u.fetch_profanity_words()
    for k, v in wordList.items():
        if k in profaned_list:
            indecent_words[k] = v
            indecent_word_count += v

    for k, v in sorted(indecent_words.items(), key=lambda item: item[1], reverse = True):
        most_used_indecent_words.append([k,v])

    indecent_sentence = str(indecent_word_count) + "\n Among them, the top 5 most used are:\n" 

    embed = discord.embed=discord.Embed(
        title= username + "'s Armando Bean Stats:",
        color=discord.Color.green()
    )
    embed.add_field(name="Top 10 most used words:", value=top_ten, inline=True)
    embed.add_field(name="Top 5 most used bad words:", value=u.words_to_string(most_used_indecent_words, 5), inline=True)
    embed.add_field(name="Bad words typed:", value=str(indecent_word_count), inline=True)
    embed.add_field(name="First message sent:", value=fMes, inline=True)
    embed.add_field(name="Messages sent:", value=mNum, inline=True)
   
    return embed

async def stats(ctx, username):
    if username.startswith("<"):
        user = await ctx.bot.fetch_user(u.id_from_mention(username))
        username = user.name
    print(username)
    channel = ctx.channel
    messages = r.loadData(ctx)
    filteredMessages = []
    count = 0
    loading_anim = asyncio.create_task(a.loading(ctx, "Computing stats")) 
    #loop through all the channel's messages
    for message in messages:
        if validateMessage(message,username):
            filteredMessages.append(message)
            count += 1
    
    await channel.send(embed = findData(filteredMessages, username))
    loading_anim.cancel()
   
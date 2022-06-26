import asyncio
from datetime import datetime
import time
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
    blacklist = ['$', '/', '!']
    for e in blacklist:
        if message["content"].startswith(e):
            return False
    return valid

#collect any relevant data found within the messages, returns a formatted string
def findData(messages, username):
    output = "{}'s Armando Beans Stats:\n-Messages sent: {}\n-Top 10 Most used words: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n-First message sent: '{}' on {}"
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
    most_used_words = []
    for k, v in sorted(wordList.items(), key=lambda item: item[1], reverse = True):
        most_used_words.append([k,v])
  
    #first message sent with date
    first_message = messages[len(messages)-1]
    fMes = first_message["content"]
    fDate = first_message["date"]

    output = output.format(username,mNum,most_used_words[0][0],most_used_words[1][0], most_used_words[2][0],most_used_words[3][0], most_used_words[4][0],most_used_words[5][0],most_used_words[6][0],most_used_words[7][0], most_used_words[8][0],most_used_words[9][0],fMes,fDate)
    return output

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
    
    await channel.send(findData(filteredMessages, username))
    loading_anim.cancel()
   
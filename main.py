import tweepy
import os
import nextcord
from nextcord.ext import commands,tasks
import time
from dotenv import load_dotenv
import keep_alive
load_dotenv()


#variables
#query
x = "shill your NFT -filter:retweets"
#last post id
pstID = "1517938166312939520"
#Discord channel
chid = 966095582940770424
#wanted language
language="en"
#text to display before link
txt1="Check Tweet before raiding! If the Tweet is not appropriate for raiding type: **%raid**. "




#Twitter AUTH
auth = tweepy.OAuth2BearerHandler(os.getenv('tTOKEN'))
api = tweepy.API(auth)

#dc
bot = commands.Bot(command_prefix='%')

#%raid command
@bot.command()
async def raid(ctx):
    print("command")
    res = api.search_tweets(q=x, count=1,result_type="popular",lang=language)
    for tweets in res:
        link = "https://twitter.com/twitter/statuses/" + str(tweets.id)
        print(link)
        await ctx.reply(txt1+link+" Next tweet in 30 minutes!")



#main loop

@tasks.loop(minutes=120.0, count=None)
async def my_background_task():
    await bot.wait_until_ready()
    global pstID
    print("working 1")
    res = api.search_tweets(q=x, count=1,since_id=pstID,result_type="recent",lang=language)
    print("working 2")
    for tweets in res:
        print("working 3")
        pstID = tweets.id
        link = "https://twitter.com/twitter/statuses/" + str(tweets.id)
        print(link)
        channel = bot.get_channel(chid)
        await channel.send(txt1+link)
       

@bot.event
async def on_ready():
    my_background_task.start()

#for 24/7 running
keep_alive.keep_alive()

# Discord AUTH
bot.run(os.getenv('dTOKEN'))



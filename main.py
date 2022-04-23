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
x = "shill your NFT"
#last post id
pstID = "1517938166312939520"
#Discord channel
chid = 966095582940770424

#Twitter AUTH
auth = tweepy.OAuth2BearerHandler(os.getenv('tTOKEN'))
api = tweepy.API(auth)

#dc
bot = commands.Bot(command_prefix='%')

pstID="1517677950451306497"

@bot.command()
async def raid(ctx):
    print("command")
    res = api.search_tweets(q=x, count=1,result_type="popular")
    for tweets in res:
        pstID = tweets.id
        link = "https://twitter.com/twitter/statuses/" + str(tweets.id)
        print(link)
        channel = bot.get_channel(chid)
        await ctx.reply("Check Tweet before raiding! If the Tweet is not appropriate for raiding type: **%raid.** "+link+" Next tweet in 30 minutes!")



#main loop

@tasks.loop(minutes=30.0, count=None)
async def my_background_task():
    await bot.wait_until_ready()

    global pstID
   
    print("working 1")
    res = api.search_tweets(q=x, count=1,since_id=pstID,result_type="recent")
    print("working 2")
    for tweets in res:
        print("working 3")
        pstID = tweets.id
        link = "https://twitter.com/twitter/statuses/" + str(tweets.id)
        print(link)
        channel = bot.get_channel(chid)
        await channel.send("Check Tweet before raiding! If the Tweet is not appropriate for raiding type: **%raid**. "+link)
       

@bot.event
async def on_ready():
    my_background_task.start()


keep_alive.keep_alive()

# Discord AUTH
bot.run(os.getenv('dTOKEN'))



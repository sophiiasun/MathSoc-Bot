import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

DRIVER = config('DRIVER')

def checkUserExist(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cnt = cursor.execute("select count(*) as cnt from mathData where username = '" + name + "'").fetchone().cnt
            if cnt == 0:  
                return False
            return True

def userNotExistEmbed(ctx):
    mbed = discord.Embed (
        description = 'Please register with the bot before using it. To do this, use the command `+register`.',
        color = 15158332 # RED 
    )
    mbed.set_author(name='Hello ' + ctx.author.name + '. You are not registered yet!')
    return mbed

def createUserDB(ctx):
    user = ctx.author
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("insert into mathData (username, xpLevel, xpCount, activityStatus) Values ('" + str(user) + "', 0, 0, 'none');")
            cursor.commit() 

def registerEmbed(ctx):
    mbed = discord.Embed (
        description = '**Below are the terms and agreements for MathSoc Bot:**\n\n \
            —> I will not spam commands that I will not use.\n \
            —> I will not purposely try commands that do not exist. Please see `+help` for a list of commands.\n \
            —> I will be respectful to everyone in this server, including the bot (no roasting, creator-san will be sad :3).\n\
            —> I will be mindful of others using the bot and share this resource (yea, that means no hogging).\n\n\
            **Please take note of:**\n\
            —> This bot is unprofessionally made so there are probably bugs and typos; use `+report bug` or `+report typos`, respectively.\n\
            —> There are some formating requirements when answering problems. Your answer will not be deemed correct if it does not follow those requirements.\n\
            —> If there are any other issues, please notify the creator by using `+creator <message>`. You will be contacted when creator-san is available.\n\n\
            **React to this message with :ballot_box_with_check:. You will be automatically registered once you accept to the above terms.**',
        color = 16776960 # YELLOW
    )
    mbed.set_author(name=ctx.author.name + '\'s Registration', icon_url=ctx.author.avatar_url)
    return mbed

def registerAcceptEmbed(ctx):
    mbed = discord.Embed (
        color = 3066993 # GREEN
    )
    mbed.set_author(name='Thank you for accepting ' + ctx.author.name + '!', icon_url=ctx.author.avatar_url)
    return mbed
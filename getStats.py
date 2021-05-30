import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

DRIVER = config('DRIVER')

# CHECK USER XP LEVEL COMMAND
def getUserLevel(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cnt = cursor.execute("select count(*) as cnt from mathData where username = '" + name + "'").fetchone().cnt
            if cnt == 0:  # user exists, update
                cursor.execute("insert into vibeScores (username, xpLevel, xpCount, activityStatus) Values ('" + name + ", 0, 0, 'none'" + "');")
                cursor.commit() 
                return False
            lvl = cursor.execute("select xpLevel from mathData where username = '" + name + "'").fetchone().xpLevel
            xp = cursor.execute("select xpCount from mathData where username = '" + name + "'").fetchone().xpCount
            return [lvl, xp]

def getUserLevelEmbed(ctx):
    user = ctx.author
    mbed = discord.Embed(color = 3447003) # BLUE
    mbed.set_author(name=user.name + '\'s Stats', icon_url=user.avatar_url)



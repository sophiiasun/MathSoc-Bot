import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

from emoji import Emoji

DRIVER = config('DRIVER')

LEVEL_XP_TOTAL = [70, 70, 100, 100, 150, 150, 250, 250]


# CHECK USER XP LEVEL COMMAND
def getUserLevel(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            lvl = cursor.execute("select xpLevel from mathData where username = '" + name + "'").fetchone().xpLevel
            xp = cursor.execute("select xpCount from mathData where username = '" + name + "'").fetchone().xpCount
            return [lvl, xp]

def levelUpEmbed(user):
    lvl = getUserLevel(user)
    mbed = discord.Embed(
        title = Emoji.star2 + ' **Level:** ' + str(lvl[0]) + ' ' + Emoji.star2 + ' | ' + Emoji.low_brightness + '**XP**: ' + str(lvl[1]) + '/' + str(LEVEL_XP_TOTAL[lvl[0]]) + ' ' + Emoji.low_brightness,
        color = 3447003 # BLUE
    )
    mbed.set_author(name=user.name + ' has leveled up!', icon_url=user.avatar_url)
    return mbed

def getUserLevelEmbed(ctx):
    user = ctx.author
    lvl = getUserLevel(user)
    mbed = discord.Embed(
        title = Emoji.star2 + ' **Level:** ' + str(lvl[0]) + ' ' + Emoji.star2 + ' | ' + Emoji.low_brightness + '**XP**: ' + str(lvl[1]) + '/' + str(LEVEL_XP_TOTAL[lvl[0]]) + ' ' + Emoji.low_brightness,
        color = 3447003 # BLUE
    )
    mbed.set_author(name='Showing ' + user.name + '\'s Stats', icon_url=user.avatar_url)
    return mbed
    



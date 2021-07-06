import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

from getStats import *

DRIVER = config('DRIVER')
LEVEL_XP_TOTAL = [70, 70, 100, 100, 150, 150, 250, 250]

def getName(user):
    return user.name + '#' + user.discriminator

def getProblemType(user):
    name = getName(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select activityStatus from mathData where username = '" + name + "'").fetchone().activityStatus

def getProblemAnswer(user):
    name = getName(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select answer from mathData where username ='" + name + "'").fetchone().answer

def getPoints(type):
    if type == 'quest':
        return 50
    if type == 'challenge':
        return 10

def clearProblemDB(user):
    name = getName(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set activityStatus = 'none' where username = '" + name + "'")
            cursor.commit()

def getMultiplier(user):
    name = getName(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select multiplier from mathData where username = '" + name + "'").fetchone().multiplier

def processCorrectAnswer(user):
    name = getName(user)
    xp = getPoints(getProblemType(user)) * getMultiplier(user)
    lvl = getUserLevel(user)
    clearProblemDB(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            if lvl[1] + xp >= LEVEL_XP_TOTAL[lvl[0]]: # level up
                cursor.execute("update mathData set xpLevel = xpLevel + 1 where username = '" + name + "'")
                cursor.execute("update mathData set xpCount = (xpCount + '" + str(xp) + "') - '" + str(LEVEL_XP_TOTAL[lvl[0]]) + "' where username = '" + name + "'")
                cursor.commit()
                return levelUpEmbed(user)
            else:
                cursor.execute("update mathData set xpCount = xpCount + '" + str(xp) + "' where username = '" + name + "'")
                cursor.commit()
                return None

def storeProblem(user, answer, type):
    name = getName(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set activityStatus = '" + type + "' where username = '" + name + "'")
            cursor.execute("update mathData set answer = '" + answer + "' where username = '" + name + "'")
            cursor.execute("update mathData set multiplier = '2' where username = '" + name + "'")
            cursor.commit()

def displayQuest(ctx, problem):
    user = ctx.author
    mbed = discord.Embed (
        title = 'Problem Credits: ' + problem[3],
        description = problem[0],
        color = 10181046 # PURPLE
    )
    mbed.set_image(url=problem[1])
    mbed.set_author(name=user.name, icon_url=user.avatar_url)
    return mbed

def displayChallenge(ctx, problem):
    user = ctx.author
    mbed = discord.Embed (
        title = 'Problem Credits: ' + problem[3],
        description = problem[0],
        color = 10181046 # PURPLE
    )
    mbed.set_image(url=problem[1])
    mbed.set_author(name=user.name, icon_url=user.avatar_url)
    return mbed

def acceptBattle(ctx):
    user = ctx.author
    mbed = discord.Embed (
        description = user.name + ' has accepted the battle! Let the matches begin! Best three out of five rounds.',
        color = 15844367 # GOLD
    )
    mbed.set_author(name=user.name + ' challenges ' + user.name + ' to a math battle!', icon_url=user.avatar_url)
    return mbed

def noPendingProblem(user):
    mbed = discord.Embed(
        description = 'No pending problem.'
    )
    return mbed

def correctAnswerEmbed(user, answer, points):
    mbed = discord.Embed (
        title = Emoji.white_check_mark + ' **|** ' + user.name + '\'s anwer is correct! You earned ' + str(points*getMultiplier(user)) + ' xp.', 
        color = 3066993 # GREEN
    )
    return mbed

def wrongAnswerEmbed(user, answer):
    mbed = discord.Embed (
        description = 'Your answer is incorrect. Try again.',
        color = 15158332 # RED
    )
    mbed.set_author(name=user.name + ' answered ' + answer + '!', icon_url=user.avatar_url)
    return mbed
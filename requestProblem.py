import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

from getStats import *

DRIVER = config('DRIVER')
LEVEL_XP_TOTAL = [70, 70, 100, 100, 150, 150, 250, 250]

# QUEST ======================================================================================================================================

def storeAnswer(user, answer, type):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set answer = '" + answer + "' where username = '" + name + "'")
            cursor.execute("update mathData set activityStatus = '" + type + "' where username = '" + name + "'")
            cursor.commit()

def getQuestEmbed(ctx):
    user = ctx.author
    mbed = discord.Embed (
        description = 'Here is your daily quest...',
        color = 10181046
    )
    mbed.set_author(name=user.name + ' is claiming their daily quest!', icon_url=user.avatar_url)
    return mbed

# CHALLENGE ==================================================================================================================================

def displayChallenge(ctx, message):
    user = ctx.author
    mbed = discord.Embed (
        description = 'Presenting a ' + str(message) + ' problem for the math-hungry you...',
        color = 10181046
    )
    mbed.set_author(name=user.name + ' is seeking for a challenge!', icon_url=user.avatar_url)
    return mbed

def editChallengeEmbed(problem, mbed):
    mbed.description = problem[0]
    mbed.set_image(url=problem[1])
    return mbed

# BATTLE =====================================================================================================================================

def acceptBattle(user, author, msg):
    mbed = discord.Embed (
        description = user.name + ' has accepted the battle! Let the matches begin! Best three out of five rounds.',
        color = 15844367 # GOLD
    )
    mbed.set_author(name=author.name + ' challenges ' + user.name + ' to a math battle!', icon_url=author.avatar_url)
    return mbed

# ANSWER QUESTION ============================================================================================================================

def getProblemType(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select activityStatus from mathData where username = '" + name + "'").fetchone().activityStatus

def noPendingProblem(user):
    mbed = discord.Embed(
        description = 'no pending problem'
    )
    return mbed

def getProblemAnswer(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select answer from mathData where username ='" + name + "'").fetchone().answer

def getPoints(type):
    if type == 'quest':
        return 50
    if type == 'challenge':
        return 10

def levelUpEmbed(user):
    lvl = getUserLevel(user)
    name = user.name + '#' + user.discriminator
    mbed = discord.Embed(
        description = 'Your are now level ' + str(lvl[0]) + ' with ' + str(lvl[1]) + '/' + str(LEVEL_XP_TOTAL[lvl[0]]) + ' xp.',
        color = 3447003 # BLUE
    )
    mbed.set_author(name=name + ' has leveled up!', icon_url=user.avatar_url)
    return mbed

def clearProblemDB(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set activityStatus = 'none' where username = '" + name + "'")
            cursor.commit()

def processCorrectAnswer(user):
    name = user.name + '#' + user.discriminator
    xp = getPoints(getProblemType(user))
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

# def processWrongAnswer(user):
    # THINK ABOUT WHAT I WANT TO HAPPEN WHEN USERS ANWER Q WRONG

def answerEmbedCorrect(user, answer, points):
    mbed = discord.Embed (
        description = 'Your answer is correct! You earned ' + points + ' xp.', 
        color = 3066993 # GREEN
    )
    mbed.set_author(name=user.name + ' answered + ' + answer + '!', icon_url=user.avatar_url)
    return mbed

def answerEmbedWrong(user, answer):
    mbed = discord.Embed (
        description = 'Your answer is incorrect. Try again.',
        color = 15158332 # RED
    )
    mbed.set_author(name=user.name + ' answered ' + answer + '!', icon_url=user.avatar_url)
    return mbed



def setProblemType(user, type):
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set activityStatus = '" + type + "'")
            cursor.commit()
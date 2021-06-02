import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

from getStats import *

DRIVER = config('DRIVER')


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
            return cursor.execute("select activityStatus from mathData where username = '" + name + "'")

def noPendingProblem(user):
    mbed = discord.Embed(
        description = ''
    )

def getProblemAnswer(user):
    name = user.name + '#' + user.discriminator
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            return cursor.execute("select answer from mathData where username ='" + name + "'").fetchone().answer

def processCorrectAnswer(user):
    name = user.name + '#' + user.discriminator
    type = getProblemType(user)
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cursor.execute("update mathData set xpCount = '" + type + "' where username = '" + name + "'")

def answerEmbedCorrect(user, answer, points):
    mbed = discord.Embed (
        description = 'Your answer is correct! You earned ' + points + ' xp.', 
        color = 3066993 # GREEN
    )
    mbed.set_author(name=user.name + ' answered + ' + answer + '!', icon_url=user.avatar_url)
    level = getUserLevel(user)

def answerEmbedWrong(user, answer):
    mbed = discord.Embed (
        description = 'Your answer is incorrect. Try again.',
        color = 15158332 # RED
    )
    mbed.set_author(name=user.name + ' answered + ' + answer + '!', icon_url=user.avatar_url)
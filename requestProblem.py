import pyodbc
from decouple import config
import discord
from discord.utils import get
from discord.ext import commands

DRIVER = config('DRIVER')


# QUEST ======================================================================================================================================

def questStoreAnswer(user, answer):
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cnt = cursor.execute("select count(*) as cnt from mathData where username = '" + str(user) + "'").fetchone().cnt
            if cnt > 0:  # user exists, update
                cursor.execute("update mathData set answer = '" + str(answer) + "' where username = '" + str(user) + "'")
            else:
                cursor.execute("insert into mathData (username, recent, average, vibeCount) Values ('" + str(user) + "', '" + str(user) + "', '" + str(user) + "', '1');")
            cursor.commit()

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

def answerEmbedCorrect(user, answer, points):
    msg = 'Your answer is correct! You earned ' # if quest, add comments
    mbed = discord.Embed (
        description = 'Your answer is correct! You earned ' + ' xp.', # experience amount depending on challenge (10) / quest (50)
        color = 3066993 # GREEN
    )
    mbed.set_author(name=user.name + ' answered + ' + answer + '!', icon_url=user.avatar_url)
    # process level increases

def answerEmbedWrong():
    mbed = discord.Embed (
        
    )
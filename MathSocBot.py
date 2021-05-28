import discord
from discord.utils import get
from discord.ext import commands
import pyodbc
import random
from decouple import config
from mathChallenges import *
import time

client = commands.Bot(command_prefix = '+', help_command = None)
TOKEN = config('TOKEN')
DRIVER = config('DRIVER')
EMOJI_CHALLENGE = ['\U00002705', '\U0001F17E'] # white_check_mark, o2

CHALLENGES = Challenges()

# CLIENT LOAD
@client.event
async def on_ready():
    general_channel = client.get_channel(847222513980276788)
    mbed = discord.Embed(
        title = 'MathSoc Bot is Now Online!',
        description = 'See `+help` for a list of commands. Enjoy!',
        color = discord.Color.green()
    )
    await general_channel.send(embed = mbed)

# CHECK USER XP LEVEL COMMAND
@client.command(pass_context=True) 
async def level(ctx):
    user = ctx.author


def checkUserExist(user):
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cnt = cursor.execute("select count(*) as cnt from mathData where username = '" + user + "'").fetchone().cnt
            if cnt == 0:  # user exists, update
                cursor.execute("insert into vibeScores (username, xpLevel, xpCount, activityStatus) Values ('" + user + \
                    ", 0, 0, 'nothing'" + "');")
                cursor.commit() 
                return False
            return True

def userNotExistEmbed(user):
    mbed = discord.Embed (
        description = 'Please register with the bot before using it. To do this, use the command `+register`.'
    )

@client.command(pass_context=True)
async def register(ctx):
    user = ctx.author
    mbed = discord.Embed (
        description = '**Below are the terms and agreements for MathSoc Bot:**\n\n \
            —> I will not spam commands that I will not use.\n \
            —> I will not purposely try commands that do not exist. Please see `+help` for a list of commands.\n \
            —> I will be respectful to everyone in this server, including the bot (no roasting, creator-san will be sad :3).\n\n\
            **Please take note of:**\n\
            —> This bot is unprofessionally made so there are probably bugs, please use `+'
    )

# DAILY QUEST COMMAND
def questStoreAnswer(user, answer):
    with pyodbc.connect(DRIVER) as conn:
        with conn.cursor() as cursor:
            cnt = cursor.execute("select count(*) as cnt from mathData where username = '" + str(user) + "'").fetchone().cnt
            if cnt > 0:  # user exists, update
                cursor.execute("update mathData set answer = '" + str(answer) + "' where username = '" + str(user) + "'")
            else:
                cursor.execute("insert into vibeScores (username, recent, average, vibeCount) Values ('" + str(name) + "', '" + str(score) + "', '" + str(score) + "', '1');")
            cursor.commit()

@client.command(pass_context=True)
async def quest(ctx):
    user = ctx.author
    if not checkUserExist(user.name):
        userNotExistEmbed(user)
    mbed = discord.Embed (
        description = 'Here is your daily quest...',
        color = 10181046
    )
    mbed.set_author(name=user.name + ' is claiming their daily quest!', icon_url=user.avatar_url)
    message = await ctx.send(embed = mbed)
    time.sleep(3) # pause 3 seconds
    problem = CHALLENGES.getChallenge()
    mbed.description = 'Here is your daily quest...\n\n' + problem[0]
    mbed.set_image(url=problem[1])
    await message.edit(embed = mbed)

# CHALLENGE PROBLEMS COMMAND
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

@client.command(pass_context=True)
async def challenge(ctx):
    # check if there is still pending 
    messageUser = ctx.message.content.split(' ')
    mbed = displayChallenge(ctx, messageUser[1])
    message = await ctx.send(embed = mbed)
    time.sleep(1) # pause 3 seconds
    mbed = editChallengeEmbed(CHALLENGES.getChallenge(messageUser[1]), mbed)
    await message.edit(embed = mbed)

# HELP COMMAND
@client.command(pass_context=True)
async def help(ctx):
    mbed = discord.Embed (
        description = 'Below are a list of commands that MathSoc Bot supports. Please don\'t go too overboard... Developer-san does not want to fix more bugs :3',
        color = 16776960
    )
    mbed.add_field(name='About Page: `+about`', value='Get to know Milliken\'s ~~only~~ best math club.', inline=False)
    mbed.add_field(name='Battle: `+battle <user_mention>`', value='Challenge a worthy opponent and see who deserves the ultimate bragging rights.', inline=False)
    mbed.add_field(name='Challenge: `+challenge <subject>`', value='Pick a mathematical topic you\'d like to work on and receive a mind-boggling challenge.', inline=False)
    mbed.add_field(name='Quest: `+quest`', value='Complete a daily quest to earn double xp. Quest resets at 12:00 AM EST.', inline=False)
    mbed.add_field(name='XP Level: `+level`', value='Check your level of mathematical expertise. Earn `xp` by doing math activities with the bot.', inline=False)
    await ctx.send(embed = mbed)

# BATTLE ANOTHER USER COMMAND
def acceptBattle(user, author, msg):
    mbed = discord.Embed (
        description = user.name + ' has accepted the battle! Let the matches begin! Best three out of five rounds.',
        color = 15844367 # GOLD
    )
    mbed.set_author(name=author.name + ' challenges ' + user.name + ' to a math battle!', icon_url=author.avatar_url)
    return mbed

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    author = message.author
    if user.bot:
        return
    if reaction.emoji == '\U00002705': # white_check_mark
        await message.edit(embed = acceptBattle(user, author))

@client.command(pass_context=True)
async def battle(ctx):
    user = ctx.author
    message = ctx.message
    others = message.mentions
    mbed = discord.Embed (
        description = others[0].mention + ' Click :white_check_mark: to accept and :o2: to decline. \
            \n \n Competitors will compete in five rounds to see who can respond with the correct answer\
            in the shortest amount of time. Best out of three. Winner will receive the **ultimate** bragging\
            rights. Are YOU up for the battle?', # display user stats
        color = 12745742 # DARK GOLD
    )
    mbed.set_author(name=user.name + ' challenges ' + others[0].name + ' to a math battle!', icon_url=user.avatar_url)
    message = await ctx.send(embed = mbed)
    for emoji in EMOJI_CHALLENGE:
        await message.add_reaction(emoji)

# ANSWERING PROBLEMS COMMAND
def answerEmbedCorrect(user, answer):
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

@client.command(pass_context=True)
async def answer(ctx):
    # check if there is pending challenge
    user = ctx.author
    message = ctx.message
    text = message.content
    answer = ''; # retrieve from DB
    if text == answer:
        await message.edit(embed = answerEmbedCorrect(user, answer))
    else:
        await message.edit(embed = answerEmbedWrong(user, answer))

client.run(TOKEN)



    
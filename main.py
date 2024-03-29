import discord
from discord.utils import get
from discord.ext import commands
import pyodbc
import random
from decouple import config
import time

from mathChallenges import *
from getStats import *
from requestProblem import *
from registration import *
from emoji import Emoji

client = commands.Bot(command_prefix = '+', help_command = None)
TOKEN = config('TOKEN')
DRIVER = config('DRIVER')

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

@client.command(pass_context=True) 
async def level(ctx):
    await ctx.send(embed = getUserLevelEmbed(ctx))

@client.command(pass_context=True)
async def register(ctx):
    user = ctx.author
    if checkUserExist(user) == True:
        await ctx.send(embed = userAlreadyRegistered(ctx))
        return
    message = await ctx.send(embed = registerEmbed(ctx))
    await message.add_reaction(Emoji.ballot_box_with_check) # :ballot_box_with_check:

# DAILY QUEST COMMAND

@client.command(pass_context=True)
async def quest(ctx):
    user = ctx.author
    if not checkUserExist(user):
        return await ctx.send(embed = userNotExistEmbed(ctx))
    problem = CHALLENGES.getChallenge('random')
    mbed = displayQuest(ctx, problem)
    message = await ctx.send(embed = mbed)
    storeProblem(user, problem[2], 'quest')

# CHALLENGE PROBLEMS COMMAND

@client.command(pass_context=True)
async def challenge(ctx):
    user = ctx.author
    if not checkUserExist(user):
        return await ctx.send(embed = userNotExistEmbed(ctx))
    type = ctx.message.content.split(' ')[1]
    problem = CHALLENGES.getChallenge(type)
    mbed = displayChallenge(ctx, problem)
    message = await ctx.send(embed = mbed)
    storeProblem(user, problem[2], 'challenge')

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

@client.command(pass_context=True)
async def battle(ctx):
    user = ctx.author
    others = ctx.message.mentions
    mbed = discord.Embed (
        description = others[0].mention + ' Click :white_check_mark: to accept and :o2: to decline. \
            \n \n Competitors will compete in five rounds to see who can respond with the correct answer\
            in the shortest amount of time. Best out of three. Winner will receive the **ultimate** bragging\
            rights. Are YOU up for the battle?', # display user stats
        color = 12745742 # DARK GOLD
    )
    mbed.set_author(name=user.name + ' challenges ' + others[0].name + ' to a math battle!', icon_url=user.avatar_url)
    message = await ctx.send(embed = mbed)
    await message.add_reaction(Emoji.white_check_mark)
    await message.add_reaction(Emoji.o2)

# ANSWERING PROBLEMS COMMAND

@client.command(pass_context=True)
async def answer(ctx, *, msg):
    user = ctx.author
    status = getProblemType(user)
    if not (status == 'quest' or status == 'challenge'): # no pending question
        await ctx.send('no quest')
        return await ctx.send(embed = noPendingProblem(user))
    answer = str(getProblemAnswer(user))
    if str(msg) == answer:
        await ctx.send(embed = correctAnswerEmbed(user, answer, getPoints(status)))
        mbed = processCorrectAnswer(user)
        if not (mbed == None):
            await ctx.send(embed = mbed)
    # else:
    #     processWrongAnswer(user)
    #     await message.edit(embed = answerEmbedWrong(user, answer))

# PROCESS USER ADDING REACTIONS

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    author = message.author
    if user.bot:
        return
    if reaction.emoji == Emoji.white_check_mark: 
        await message.edit(embed = acceptBattle(user, author))
    elif reaction.emoji == Emoji.ballot_box_with_check: 
        createUserDB(user)
        await message.edit(embed = registerAcceptEmbed(user))

@client.command(pass_context=True)
async def test(ctx):
    await ctx.send(ctx.author.name + '#' + ctx.author.discriminator)

client.run(TOKEN)



    
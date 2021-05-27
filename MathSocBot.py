import discord
from discord.utils import get
from discord.ext import commands
import random
from decouple import config

client = commands.Bot(command_prefix = '+', help_command=None)
TOKEN = config('TOKEN');

EMOJI_CHALLENGE = ['\U00002705', '\U0001F17E']

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
async def battle(ctx):
    user = ctx.author
    message = ctx.message
    others = message.mentions
    mbed = discord.Embed (
        description = user.mention + ' Click :white_check_mark: to accept and :o2: to decline.',
        color = 1752220 # AQUA
    )
    mbed.set_author(name=str(user).split('#')[0] + ' challenges ' + str(others[0]).split('#')[0] + ' to a math battle!', icon_url=user.avatar_url)
    message = await ctx.send(embed = mbed)
    for emoji in EMOJI_CHALLENGE:
        await message.add_reaction(emoji)

@client.command(pass_context=True)
async def quest(ctx):
    user = ctx.author
    mbed = discord.Embed (
        description = user.mention + ' Here is your daily quest.',
        color = 10181046
    )
    mbed.set_author(name=str(user).split('#')[0] + ' is claiming their daily quest!', icon_url=user.avatar_url)
    await ctx.send(embed = mbed)

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

client.run(TOKEN)



    
import discord
from discord.utils import get
from discord.ext import commands
import random
from decouple import config

client = commands.Bot(command_prefix = '+', help_command=None)
TOKEN = config('TOKEN');

EMOJI_CHALLENGE = ['']

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
        title = str(user).split('#')[0] + ' has challenged ' + str(others[0]).split('#')[0] + ' to a math battle!',
        description = user.mention + 'Click :white_check_mark: to accept and :o2: to decline.',
        color = 1752220 # AQUA
    )
    mbed.set_author(name=str(user), icon_url=user.avatar_url)
    await ctx.send(embed = mbed)

client.run(TOKEN)



    
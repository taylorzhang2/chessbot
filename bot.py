import discord
import asyncio
import logging
from discord.ext import commands
from discord.ext.commands import Bot
import traceback
import sys
import yaml

import os
import discord
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
#bot = commands.Bot(command_prefix='m!')

# below: manual input of token/guild vals
#TOKEN = input('Please enter the token: ')
#GUILD = input('Please enter the guild: ')

# client = discord.Client()

#stream = open('config.yaml')
#data = yaml.load(stream)

description = """beep boop I'm a bot that lets you play chess"""

extensions = ['cogs.game']
#discord_logger = logging.getLogger('discord')
#discord_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.WARNING)
#handler = logging.FileHandler(filename='tz.log', encoding='utf-8', mode='w')
#log.addHandler(handler)
help_attrs = dict(hidden=True)

bot = commands.Bot(command_prefix='>', description=description, pm_help=None, help_attrs=help_attrs)

@bot.event
async def on_ready():
    print('logged in as: ')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

@bot.event
async def on_message(message):
    print('on_message')
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name='hi')
async def hello(ctx):
    response = 'Hi, ' + ctx.author.name + '!'
    await ctx.send(response)

"""
@commands.command()
async def load(extension_name : str, ctx):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("'''py\n{}; {}\n'''".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))
"""

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension}.")
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__,e))
    bot.run(TOKEN, bot=True, reconnect=True)
    #handlers = log.handlers[:]
    #for hdlr in handlers:
        #hdlr.close()
        #log.removeHandler(hdlr)

"""
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
)
"""


"""

def eval(s,op):
    lst = []
    for i in s:
        if i.isnumeric():
            lst.append(int(i))
    if op == 'add':
        return sum(lst)
    elif op == 'mult':
        result = 1
        for i in lst:
            result *= i
        return result

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    cmddict = {'greet':'Hi, ' + message.author.name + '!',
               'gay':'no u',
               'm!':'haha yes very funny',
               'fuck':'wow haha i am dying of laughter',
               'daily':'wrong prefix idiot. not tatsumaki smdh',
               '':"that's not a command dumbass, that's the absence of a command. smdh",
               'help':'Commands:\n\t1. greet (prints a greeting)\n\t2. gay (no u)\n\t3. add (adds ints in input)\n\t4. mult (multiplies ints in input)'}
    prefix = 'm!'
    if message.content[:len(prefix)] == prefix:
        body = message.content[len(prefix):]
        if body[:3] == 'add':
            response = eval(message.content, 'add')
        elif body[:4] == 'mult':
            response = eval(message.content, 'mult')
        elif body not in cmddict:
            response = 'enter a valid command dumbass'
        else:
            response = cmddict[body]
        await message.channel.send(response)

client.run(TOKEN)
#bot.run(TOKEN)
"""

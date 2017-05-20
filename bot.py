import discord
import asyncio
import logging
from discord.ext import commands
import traceback
import sys
import yaml
stream = open('config.yaml')
data = yaml.load(stream)

description = """beep boop I'm a bot that lets you play chess"""

extensions = ['cogs.game']
#discord_logger = logging.getLogger('discord')
#discord_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
#handler = logging.FileHandler(filename='tz.log', encoding='utf-8', mode='w')
#log.addHandler(handler)
help_attrs = dict(hidden=True)
prefix = ['?', '!', '\N{HEAVY EXCLAMATION MARK SYMBOL}']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None, help_attrs=help_attrs)

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
@bot.command()
async def load(extension_name : str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("'''py\n{}; {}\n'''".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))
        
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__,e))
    bot.run(data['key'])
    #handlers = log.handlers[:]
    #for hdlr in handlers:
        #hdlr.close()
        #log.removeHandler(hdlr)


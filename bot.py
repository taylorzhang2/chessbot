import discord
import asyncio
import logging
from game import Game
import yaml
logging.basicConfig(level=logging.DEBUG)
BOARD_GAME = None
stream = open('config.yaml')
data = yaml.load(stream)
print(data)
client = discord.Client()

@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    global BOARD_GAME
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!playchess'):
        if BOARD_GAME != None:
            await client.send_message(message.channel, 'Game already started')
        else:
            m = message.content.split(' ')
            if len(m) == 2:
                print('fuck')
                print(m)
                challengee = m[1].strip()
                print(challengee)
                if not challengee.startswith('<@'):
                    await client.send_message(message.channel, 'You must tag another user with @ in order to play with them') 
                else:    
                    challenger = message.author.mention
                    BOARD_GAME = Game(challenger, challengee)
                    print(BOARD_GAME.board)
                    await client.send_message(message.channel, BOARD_GAME.board) 
                    await client.send_message(message.channel, 'Your move, {}'.format(BOARD_GAME.white.username))
                    #startgame 
    elif BOARD_GAME != None and message.content.startswith('!play'):
        move = message.content.split(' ')[1].strip()
        if message.author.mention == BOARD_GAME.white.username:
            if BOARD_GAME.white.turn:
                try:
                    BOARD_GAME.board.push_san(move)
                    BOARD_GAME.white.turn = False
                    BOARD_GAME.black.turn = True
                    await client.send_message(message.channel, BOARD_GAME.board) 
                    await client.send_message(message.channel, 'Your move, {}'.format(BOARD_GAME.black.username))
                except ValueError:
                    await client.send_message(message.channel, '{} is an illegal move, {}'.format(move, message.author))
            else: 
                await client.send_message(message.channel, 'It is not your turn, {}'.format(message.author))
        elif message.author.mention == BOARD_GAME.black.username:
            if BOARD_GAME.black.turn: 
                try:
                    BOARD_GAME.board.push_san(move)
                    BOARD_GAME.white.turn = True
                    BOARD_GAME.black.turn = False
                    await client.send_message(message.channel, BOARD_GAME.board) 
                    await client.send_message(message.channel, 'Your move, {}'.format(BOARD_GAME.white.username))
                except ValueError:
                    await client.send_message(message.channel, '{} is an illegal move, {}'.formate(move, message.author))
            else: 
                await client.send_message(message.channel, 'It is not your turn, {}'.format(message.author))
        if BOARD_GAME.board.is_game_over():
            BOARD_GAME = None
            await client.send_message(message.channel, 'Game over. {}'.format(BOARD_GAME.board.result()))
        
client.run(data['key'])



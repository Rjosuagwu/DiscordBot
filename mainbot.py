import discord
from discord.ext import commands
import os

from cogs.Greetings import Greetings
#key
from Apis import *

intents = discord.Intents.all()
intents.members = True

queues = {}

def check_queue(ctx,id):
    if queues[id]!=[]:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix = '!', intents=intents) #this is to initialise the bot
# inside the parenthesis is the prefix

# Add the Greetings cog to the bot

@client.event
async def on_ready():   #this will run when the bot has set up 
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Being built!"))
    print("This bot is HERE!")
    print("--------------------------")

    await client.load_extension("cogs.Greetings")
    await client.load_extension("cogs.Admin")
    await client.load_extension("cogs.Music")
    await client.load_extension("cogs.Fun")


client.run(bot_token) #This is our api key

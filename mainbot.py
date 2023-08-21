import discord
import requests
import json         #only relevent for the joke api to read the json file 
from discord.ext import commands
from discord import FFmpegPCMAudio
#for kicking and banning
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

from Apis import*

queues = {}

def check_queue(ctx,id):
    if queues[id]!=[]:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents=intents) #this is to initialise the bot
# inside the parenthesis is the prefix

@client.event
async def on_ready():   #this will run when the bot has set up 
    print("This bot is HERE!")
    print("--------------------------")

@client.command()
async def year(ctx):   #this function name will be what the command name is
    await ctx.send("The Year Is 2023!")

@client.event 
async def on_member_join(member):

    jokeurl = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"

    headers = {
	"X-RapidAPI-Key": joke_token,       #encapsulated Api key
	"X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(jokeurl, headers=headers)

    channel = client.get_channel(1143304964689645641)
    await channel.send("Your new friend " + member.name + " has joined the party.")
    await channel.send(json.loads(response.text)[0]['joke'])        # Accessing the json file

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1143304964689645641)
    await channel.send("Everyone wave goodbye to "+ member.name)


#Leaving and Joining voice channels

@client.command(pass_context = True)  #decorator for leaving and joining voice channels
async def join(ctx):            #since the decorator is for commands then this function is command that you would type
    if(ctx.author.voice):       #if the person that wrote the command is in a voice channel
        channel = ctx.message.author.voice.channel      #we store the channel of the author in a variable
        voice = await channel.connect()         #The bot will connect to this channel
        source = FFmpegPCMAudio('C:/Users/rjosu/.vscode/Codeee/DiscordBot/audiofiles/hello.mp3')
        player = voice.play(source)
    else:
        await ctx.send("You are not currently in a voice channel.")      #let the user know that they are not in a voice channel

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)     #This piece of code is used to get the voice connection that the bot has.
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused!")
    else:
        await ctx.send("There is no music currently playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("The music is already playing!")
    else:
        voice.resume()
        await ctx.send("The party has been resumed!!")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop

@client.command()
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = ('C:/Users/rjosu/.vscode/Codeee/DiscordBot/audiofiles/'+arg+'.mp3')
    source = FFmpegPCMAudio(song)        # this allows us to play any sound as long as it is in our library
    player = voice.play(source, after = lambda x = None: check_queue(ctx,ctx.message.guild.id))

@client.command()
async def queue(ctx,arg):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    song = ('C:/Users/rjosu/.vscode/Codeee/DiscordBot/'+arg+'.mp3')
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = source

    await ctx.send("Queued!")



@client.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):       #checks if the voiceclient is currently connected to a voice chat
        await ctx.guild.voice_client.disconnect()       
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I am not currently in a voice channel.")



"""@client.event
async def on_message(message):      #This command will be called when the message is sent
    
    if message.content =="Address":
        await message.delete()
        await message.channel.send("Don't send any sensitive messages again!")      #finds the channel that the message was sent into
"""

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'User {member} has been kicked')        #f string that allows me to pass in variables

@kick.error 
async def kick_error(ctx, error):       #this is used to catch errors

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permisson to kick people!")


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been Banned!')        #f string that allows me to pass in variables

@ban.error 
async def ban_error(ctx, error):       #this is used to catch errors

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to Ban people!")

@client.command()
async def nerd(ctx):
    embed = discord.Embed(title = "NERD", type = "rich", url = "https://media.makeameme.org/created/lets-get-nerdy.jpg", description="STOP BEING SO NERDY!", color=0x8080ff)
    embed.set_author(name = ctx.author.display_name, icon_url = "https://ih1.redbubble.net/image.3640920496.6320/raf,360x360,075,t,fafafa:ca443f4786.jpg")
    embed.set_thumbnail(url= "https://sphero.com/cdn/shop/articles/coding_languages_1000x.png?v=1619126283")
        
    await ctx.send(embed=embed)


client.run(bot_token) #This is our api key

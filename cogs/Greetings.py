import discord
from discord.ext import commands
from discord import Member
import os
import sys
import requests
import json         #only relevent for the joke api to read the json file 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Apis import *
sys.path.pop()

class Greetings(commands.Cog):

    def __init__(self,client):
        self.client = client


    @commands.Cog.listener() 
    async def on_member_join(self, member):

        jokeurl = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"

        headers = {
	    "X-RapidAPI-Key": joke_token,       #encapsulated Api key
	    "X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
        }

        response = requests.get(jokeurl, headers=headers)

        channel = self.client.get_channel(1143304964689645641)
        await channel.send("Your new friend " + member.name + " has joined the party.")
        await channel.send(json.loads(response.text)[0]['joke'])        # Accessing the json file

    @commands.Cog.listener() 
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1143304964689645641)
        await channel.send("Everyone wave goodbye to "+ member.name)

    @commands.command()
    async def year(self, ctx):   #this function name will be what the command name is
        await ctx.send("The Year Is 2023!")

    @commands.command()
    async def welcome(self, ctx, user:discord.Member, message = None):
        message = "Welcome Home!"
        embed = discord.Embed(title=message)
        await user.send(embed = embed)

    @commands.Cog.listener() 
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions to do that")

    @commands.command()
    async def nerd(self, ctx):
        embed = discord.Embed(title = "NERD", type = "rich", url = "https://media.makeameme.org/created/lets-get-nerdy.jpg", description="STOP BEING SO NERDY!", color=0x8080ff)
        embed.set_author(name = ctx.author.display_name, icon_url = "https://ih1.redbubble.net/image.3640920496.6320/raf,360x360,075,t,fafafa:ca443f4786.jpg")
        embed.set_thumbnail(url= "https://sphero.com/cdn/shop/articles/coding_languages_1000x.png?v=1619126283")
        
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Greetings(client))
import discord
from discord.ext import commands
from discord import Member


class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        channel = reaction.message.channel
        await channel.send(user.name + " said: " + reaction.emoji)

    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction,user):
        channel = reaction.message.channel
        await channel.send(user.name + " removed: " + reaction.emoji)



async def setup(client):
    await client.add_cog(Fun(client))
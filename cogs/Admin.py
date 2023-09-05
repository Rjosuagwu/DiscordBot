import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

class Admin(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        await ctx.send(f'User {member} has been kicked')        #f string that allows me to pass in variables

    @kick.error 
    async def kick_error(self,ctx, error):       #this is used to catch errors

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permisson to kick people!")


    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'User {member} has been Banned!')        #f string that allows me to pass in variables

    @ban.error 
    async def ban_error(self,ctx, error):       #this is used to catch errors

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to Ban people!")

    @commands.command()
    @has_permissions(administrator=True)
    async def unban(self,ctx, member:discord.Member,*, reason=None):
        await ctx.guild.unban(member)
        await ctx.send(f"{member} has been unbanned")

    @commands.Cog.listener() 
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions to do that")

    @commands.command(pass_context = True) # this decorator is used to pass various information about the context in which the command what invoked
    @commands.has_permissions(manage_roles = True)
    async def addRole(self, ctx, user : discord.Member, *, role:discord.Role):

        if role in user.roles:
            await ctx.send(f"{user.mention} already has this role!")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user.mention} has been given the power!")

    @commands.command(pass_context = True) # this decorator is used to pass various information about the context in which the command what invoked
    @commands.has_permissions(manage_roles = True)
    async def removeRole(self, ctx, user : discord.Member, *, role:discord.Role):

        if role not in user.roles:
            await ctx.send(f"{user.mention} doesn't have this role!")
        else:
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} has been stripped of their dignity!")

    @addRole.error
    async def role_error (self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions to use this!")

    @removeRole.error
    async def role_error (self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions to use this!")

async def setup(client):
    await client.add_cog(Admin(client))
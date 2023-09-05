import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


class Music(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.queues = {}

    def check_queue(self,ctx,id):
        if self.queues[id]!=[]:
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)
            player = voice.play(source)

    @commands.command(pass_context = True)  #decorator for leaving and joining voice channels
    async def join(self,ctx):            #since the decorator is for commands then this function is command that you would type
        if(ctx.author.voice):       #if the person that wrote the command is in a voice channel
            channel = ctx.message.author.voice.channel      #we store the channel of the author in a variable
            voice = await channel.connect()         #The bot will connect to this channel
            source = FFmpegPCMAudio('C:/Users/rjosu/.vscode/Codeee/DiscordBot/audiofiles/hello.mp3')
            player = voice.play(source)
        else:
            await ctx.send("You are not currently in a voice channel.")      #let the user know that they are not in a voice channel

    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)     #This piece of code is used to get the voice connection that the bot has.
        if voice.is_playing():
            voice.pause()
            await ctx.send("Paused!")
        else:
            await ctx.send("There is no music currently playing.")

    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        if voice.is_playing():
            await ctx.send("The music is already playing!")
        else:
            voice.resume()
            await ctx.send("The party has been resumed!!")

    @commands.command()
    async def stop(self,ctx):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        voice.stop

    @commands.command()
    async def play(self, ctx, arg):
        voice = ctx.guild.voice_client
        song = ('C:/Users/rjosu/.vscode/Codeee/DiscordBot/audiofiles/'+arg+'.mp3')
        source = FFmpegPCMAudio(song)        # this allows us to play any sound as long as it is in our library
        player = voice.play(source, after = lambda x = None: self.check_queue(self,ctx,ctx.message.guild.id))

    @commands.command()
    async def queue(self,ctx,arg):
        voice = discord.utils.get(self.client.voice_clients,guild=ctx.guild)
        song = ('C:/Users/rjosu/.vscode/Codeee/DiscordBot/'+arg+'.mp3')
        source = FFmpegPCMAudio(song)

        guild_id = ctx.message.guild.id

        if guild_id in self.queues:
            self.queues[guild_id].append(source)
        else:
            self.queues[guild_id] = source

        await ctx.send("Queued!")



    @commands.command(pass_context=True)
    async def leave(self,ctx):
        if(ctx.voice_client):       #checks if the voiceclient is currently connected to a voice chat
            await ctx.guild.voice_client.disconnect()       
            await ctx.send("I have left the voice channel.")
        else:
            await ctx.send("I am not currently in a voice channel.")



async def setup(client):
    await client.add_cog(Music(client))
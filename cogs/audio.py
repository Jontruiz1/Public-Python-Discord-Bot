import youtube_dl
import discord
import asyncio
from discord.ext import commands

class Audio(commands.Cog, name='Audio, not working'):
    def __init__(self, bot):
        self.bot = bot
    

def setup(bot):
    bot.add_cog(Audio(bot))
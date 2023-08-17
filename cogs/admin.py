from discord.ext import commands
import re
import discord

class Admin(commands.Cog, name='Admin - Testing commands'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    '''Making a custom help command
    def embed_creator(self, ctx):
            author_name = ctx.message.author.display_name
            author_image = ctx.message.author.avatar_url

            embed=discord.Embed(title="Command help", color=discord.Color.random())
            embed.set_author(name=author_name, icon_url=author_image)

            print(self.bot.extensions)

            return embed

    @commands.command(brief='Get information for each of the commands')
    async def help(self, ctx):
    
        embed = embed_creator(self, ctx)
        await ctx.send(embed=embed)
    '''
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting Down")
        await ctx.bot.close()

    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, cerror: commands.CommandError):
        text = ctx.message.content
        
        if (isinstance(cerror, commands.CommandNotFound)):
            found = re.search(".h.*e.*l.*p*", text)
            if(found != None and len(found.string) > 0):
                message = f"Did you mean to say '^help'"
            else:
                message = f"Command not found!"
        elif (isinstance(cerror, commands.UserInputError)):
            message = f"Something about your input was wrong, please check your input and try again!"
        else:
            message = f"Check your parameters"
        
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)

        

async def setup(bot):
    await bot.add_cog(Admin(bot))
from discord.ext import commands
import discord


class Socialize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_roles = ['220', '255', '301', '302', '310', '315', '318', '320', '360', '418', '420', '435', '460', '475']
        self.available_roles = ['320', '418', '435', '475']
        self.poll_choices = ['🇦', '🇧','🇨', '🇩','🇪','🇫','🇬']

    ''' Some code to start working on the poll creation, not working yet 
    @commands.command(brief='Create a poll', description='format is =poll pollname pollarg1 pollarg2 ... pollargn')
    async def poll(self, ctx, pollName, duration, *args):
        
        if(int(duration) > 60):
            await ctx.send("Please enter a time in minutes less than or equal to an hour", delete_after=3)
        elif (len(args) > 7 or len(args) <  2):
            await ctx.send("Please enter a max of 7 and min of 2 poll choices", delete_after=3)
        else:
            author_name = ctx.message.author.display_name
            author_image = ctx.message.author.avatar_url

            embed=discord.Embed(title=pollName, color=discord.Color.random())
            embed.set_author(name=author_name, icon_url=author_image)
            message = '{duration} minutes'.format(duration) if duration < 60 else '1 hour'
            time = 'This poll will disappear in ' + message
            embed.set_footer(text=time)
            embed.timestamp = datetime.datetime.now()

            for i in range(len(args)):
                embed.add_field(name=(self.poll_choices[i]), value=args[i], inline=False)
            modifier = await ctx.send(embed=embed, delete_after=10)
            for i in range(len(args)):
                await modifier.add_reaction(self.poll_choices[i])

        await ctx.message.delete(delay=10)
        await asyncio.sleep(5)
        await ctx.send(modifier.reactions)
    '''
    
    @commands.command(brief = 'gets currently popular classes', 
                      description='format is =role public_roles, only works in the welcome-roles chat, if you want another class added let me know')
    async def public_roles(self,ctx):
        message = "Current public classes are:\n"
        channel = str(ctx.message.channel)

        if channel == 'welcome-roles':
            for role in self.public_roles :
                message += (role + ', ')
            message = message[:-2]
            await ctx.send(message)
        else:
            await ctx.send('Please send this message in the proper channel', delete_after=5)
            await ctx.message.delete(delay=5)



    @commands.command(brief = 'assigns a role in welcome chat', 
                      description='format is =role roll_name, only works in the welcome-roles chat, if you already have the role, it will be removed')
    async def addrole(self,ctx, arg1):
        name = str(arg1)
        channel = str(ctx.message.channel)
        user = ctx.message.author
        member_roles = user.roles
        
        role_name = discord.utils.find(lambda r: r.name == name, ctx.message.guild.roles)
        
        if  name in self.available_roles and channel == 'welcome':
            if(role_name in member_roles):
                await user.remove_roles(role_name)
                await ctx.send('Role removed!')
            else:
                await user.add_roles(role_name)
                await ctx.send('Role added!')
        elif channel != 'welcome-roles':
            await ctx.send('Please send this message in the proper channel', delete_after=5)
            await ctx.message.delete(delay=5)
        else:
            await ctx.send('Not a valid role\nUse =public_roles to look at the list of public currently active classes', delete_after=5)
            await ctx.message.delete(delay=5)

def setup(bot):
    bot.add_cog(Socialize(bot))
from discord.ext import commands

class Math(commands.Cog, name='Math - Little Math Commands'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief='adds numbers infinitely', description='format is =add arg1 arg2 ... argn, does arg1 + arg2 + .. + argn', pass_context=True)
    async def add(self,ctx, *message):
        sum = 0
        try:
            for num in message:
                sum += float(num)
            await ctx.send(sum)
        except ValueError:
            await ctx.send('Check the parameters!')

    @commands.command(brief='subtracts numbers infinitely', description='format is =sub arg1 arg2 ... argn, does arg1 - arg2 - ... - argn', pass_context=True)
    async def sub(self, ctx, *message):
        sum = 0
        try:
            for i in range(len(message)):
                if i == 0:
                    sum = float(message[i])
                else:
                    sum -= float(message[i])
            await ctx.send(sum)
        except ValueError:
            await ctx.send('Check the parameters!')

    @commands.command(brief='multiplies numbers infinitely', description='format is =mul arg1 arg2 ... argn, does arg1 * arg2 * ... * argn', pass_context=True)
    async def mul(self, ctx, *message):
        try:
            for i in range(len(message)):
                if i == 0:
                    sum = float(message[i])
                else:
                    sum *= float(message[i])
            await ctx.send(sum)
        except ValueError:
            await ctx.send('Check the parameters!')

    @commands.command(brief='divides numbers infinitely', description='format is =div arg1 arg2 ... argn, does arg1 / arg2 / ... / argn', pass_contex=True)
    async def div(self, ctx, *message):
        try:
            for i in range(len(message)):
                if i == 0:
                    sum = float(message[i])
                else:
                    sum /= float(message[i])
            await ctx.send(sum)
        except ValueError:
            await ctx.send('Check the parameters!')
        except ZeroDivisionError:
            await ctx.send('Divided by zero :/')
    
    @commands.command(brief='exponentiates 2 numbers', description='format is =power arg1 arg2, raises arg1 to ⌊arg2⌋', pass_contex=True)
    async def power(self, ctx, arg1, arg2):
        a = float(arg1)
        b = int(arg2)
        await ctx.send(pow(a, b))

    
    @commands.command(brief='modulates numbers infinitely', description='format is =mod arg1 arg2 ... argn, does arg1 % arg2 % ... % argn')
    async def mod(self, ctx, *message):
        try:
            for i in range(len(message)):
                if i == 0:
                    modulation = float(message[i])
                else:
                    modulation %= float(message[i])
            await ctx.send(modulation)
        except ValueError:
            await ctx.send('Check the parameters!')
        except ZeroDivisionError:
            await ctx.send('Modulated by zero :/')

async def setup(bot):
    await bot.add_cog(Math(bot))
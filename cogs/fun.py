import datetime, random, os
import discord, asyncio, aiohttp
from datetime import date
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.holiday_cats = os.listdir('Holiday_Cats/')
        self._last_member = None

    @commands.command(brief='Gives a random dog pic', description='Gives a random dog pic')
    async def dogceo(self, ctx):
        url = 'https://dog.ceo/api/breeds/image/random'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if(r.status==200):
                    await ctx.send(('😒\n' if (random.randint(0, 10)) < 2 else '') + (await r.json())['message'])
                else:
                    await ctx.send('Something went wrong accessing the dogs')

    @commands.command(brief='Gives a random cat pic', description='Gives a random cat pic')
    async def cataas(self, ctx): 
        url = "https://api.thecatapi.com/v1/images/search"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if(r.status == 200):
                    '''
                    img = await r.read()
                    with io.BytesIO(img) as file:
                        await ctx.send(file=discord.File(file, 'catimg.jpg'))
                    '''
                    info = await r.json()
                    main = info[0]
                    link = main['url']
                    await ctx.send(link)
                else:
                    await ctx.send('Something went wrong accessing the cats')
    
    @commands.command(brief="Flip a single coin", description='Flip a coin to get heads or tails, maybe it lands on the side?')
    async def coinflip(self, ctx):
        num = random.randint(0,6000)
        if(num < 3000):
            await ctx.send("Heads!")
        elif(num >= 3000 and num != 6000):
            await ctx.send("Tails!")
        else:
            await ctx.send("Landed on the side!")

    @commands.command(brief="Rock, paper, scissors", description='Play a game of rock, paper, scissors')
    async def roshambo(self, ctx):
        message = ctx.message
        computer_choice = random.randint(0, 2)
        player_choice = 0
        play = True
        wins = 0
        losses = 0
        draws = 0
        games = 0

        def playerChoice(reaction, user):
            nonlocal player_choice
            if(user != message.author):
                return False
            
            if(str(reaction.emoji) == '✊'):
                player_choice = 0
            elif(str(reaction.emoji) == '✋'):
                player_choice = 1
            elif(str(reaction.emoji) == '✌️'):
                player_choice = 2
            else:
                return False
            
            return True
        
        def playAgain(reaction, user):
            if(user == message.author):
                return (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❎')
            else:
                return False
                
        async def game():
            nonlocal play
            nonlocal wins
            nonlocal losses
            nonlocal draws

            msg = await ctx.send('Rock, paper, scissors!')
            game_reactions = ['✊', '✋', '✌️']
            play_again = ['✅', '❎']
            result = ''
            play = True

            for emoji in game_reactions:
                await msg.add_reaction(emoji)
            try:
                reaction = await self.bot.wait_for('reaction_add', timeout=10.0, check=playerChoice)
                await msg.delete(delay=10)
            except asyncio.TimeoutError:
                await ctx.send('You took to long to pick!')
                play = False
            else:
                if(computer_choice == 0):
                    result = '✊'
                    if(player_choice == 0):
                        result += ' Draw!'
                        draws += 1
                    elif(player_choice == 1):
                        result += ' I lost :c'
                        wins +=1
                    else:
                        result += ' I win!!!'
                        losses +=1
                    temp = discord.File('Roshambo/Rock_cat.png')
                elif(computer_choice == 1):
                    result = '✋'
                    if(player_choice == 1):
                        result += ' Draw!'
                        draws += 1
                    elif(player_choice == 2):
                        result += ' I lost :c'
                        wins += 1
                    else:
                        result += ' I win!!!'
                        losses += 1
                    temp = discord.File('Roshambo/Paper_cat.jpg')
                else:
                    result = '✌️'
                    if(player_choice == 2):
                        result += ' Draw!'
                        draws += 1
                    elif(player_choice == 0):
                        result += ' I lost :c'
                        wins += 1
                    else:
                        result += ' I win!!!'
                        losses += 1
                    temp = discord.File('Roshambo/Scissors_cat.jpg')
                    result += '\n'
                await msg.delete(delay=0)

                message = await ctx.send(result, file=temp)

                msg = await ctx.send('\nPlay again?')
                for emoji in play_again:
                    await msg.add_reaction(emoji)

                try:
                    reaction = await self.bot.wait_for('reaction_add', timeout=10.0, check=playAgain)
                except asyncio.TimeoutError:
                    play = False
                    await message.delete(delay=0.0)
                    await msg.delete(delay=0.0)
                else:
                    play = (str(reaction[0].emoji) == '✅')
                    await msg.delete(delay=0)
                    await message.delete(delay=0)
        result = ''

        while(play and games <= 5):
            computer_choice = random.randint(0, 2)
            games += 1
            await game()
        
        if(games >= 5):
            result = 'Game limit reached!\n'  
        result += 'Game over!\n'
        if(wins > 0):
            result += (f'You won {wins} times(s)\n')
        if(losses > 0):
            result += (f'I won {losses} time(s)\n')
        if(draws > 0):
            result += (f'We drew {draws} time(s)')

        await ctx.send(result)

    @commands.command(brief="Flips n number of coins", description="Flips arg1 coins in range [0, 990000]")
    async def coinsflipper(self, ctx, arg1):
        heads = 0
        tails = 0
        sides = 0
        rangeNum = int(arg1)
        msg = "Flipped the coin {} time(s).".format(rangeNum)

        if(rangeNum > 990000):
            await ctx.send("Too many coins, please go lower")
        else:
            for x in range (rangeNum):
                num = random.randint(0,6000)
                if(num < 3000):
                    heads += 1
                elif (num >= 3000 and num != 6000):
                    tails += 1
                else:
                    sides += 1

            if(heads > 0):
                msg += "\n{} head(s)".format(heads)
            if(tails > 0):
                msg += "\n{} tail(s)".format(tails)
            if(sides > 0):
                msg += "\n{} time(s) on its side!!".format(sides)
            await ctx.send(msg)
      
    @commands.command(brief='Sends a cow! A sphere cauw c:')
    async def cauw(self, ctx):
        await ctx.send('https://tenor.com/view/cow-spot-the-cow-topology-funny-gif-22643459')
    
    @commands.command(brief='Send a holiday picture')
    async def holiday(self, ctx):
        today = date.today()
        day = today.strftime('%d')
        dayName = today.strftime('%A')
        month = today.strftime('%m')
        thanksgiving = False

        if(month == '11' and not thanksgiving):
            thanksgiving = True if day > 21 and dayName == 'Thursday' else False

        current = today.strftime('%d/%m')

        if(current == '4/07'):
            await ctx.send ('Happy Firework Day!', file=discord.File('Holiday_Cats/Firework_cat.jpg'))
        elif (current == '10/31'):
            await ctx.send ('Happy Spooky Day!', file=discord.File('Holiday_Cats/Spooky_cat.jpg'))
        elif current == '02/14':
            await ctx.send ('Happy Love Day!', file=discord.File('Holiday_Cats/Love_cat.jpg'))
        elif current == '12/25':
            await ctx.send ('Happy Jesus Day!', file=discord.File('Holiday_Cats/Jesus_cat.jpeg'))
        elif thanksgiving:
            await ctx.send ('Happy Turkey Day!', file=discord.File('Holiday_Cats/Turkey_cat.jpg'))
        else:
            await ctx.send ("I don't know of any holidays today :(")
            ''' Render doesn't like match statements so i do elifs :(
        match current:
            case '04/07':
                await ctx.send ('Happy Firework Day!', file=discord.File('Holiday_Cats/Firework_cat.jpg'))
            case '10/31':
                await ctx.send ('Happy Spooky Day!', file=discord.File('Holiday_Cats/Spooky_cat.jpg'))
            case '02/14':
                await ctx.send ('Happy Love Day!', file=discord.File('Holiday_Cats/Love_cat.jpg'))
            case '12/25':
                await ctx.send ('Happy Jesus Day!', file=discord.File('Holiday_Cats/Jesus_cat.jpeg'))
            case _:
                if thanksgiving: await ctx.send ('Happy Turkey Day!', file=discord.File('Holiday_Cats/Turkey_cat.jpg'))
                else: await ctx.send ("I don't know of any holidays today :(")
        '''
    @commands.command(brief='Send capystack', description='Stack of capybaras :o')
    async def capystack(self, ctx):
        await ctx.send (file=discord.File('Random_Fun/Capy_stack.jpg'))
    @commands.command(brief='For when pain', description="For when words aren't enough to describe the pain you feel")
    async def pain(self, ctx):
        await ctx.send(file=discord.File('Random_Fun/pain.jpg'))

    @commands.command(brief='Secret santer pairer', description='Pairs the people in a discord channel with eachother for a secret Santa event!')
    async def secretsanta(self, ctx):
        members = list(ctx.guild.members)
        channel = ctx.channel
        members.remove(self.bot.user)
        receivers = members.copy()

        if(str(channel) != 'christmas'): 
            await ctx.send('Incorrect channel')
            return

        for member in members:
            first = member

            receiver = randint(0, len(receivers)-1)
            while receivers[receiver] == member:
                receiver = randint(0, len(receivers)-1)

            second = receivers[receiver]

            dm = await first.create_dm()
            await dm.send(f'Your gift receiver is {second.name}')

            receivers.remove(second)      
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready! Time:', datetime.datetime.now().hour)
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        author = msg.author
        content = msg.content
        guild = msg.channel

        if(content.lower().__contains__('i hate cs')):
            await msg.add_reaction('😔')
        if(content.lower() == 'bark'):
            await guild.send('HISSSSSSS')
        if( (content.lower() == 'meow' or content.lower() == 'nya' ) and author.id != 541133397544665096 and author.id != 958726337173024808):
            await guild.send('meow')
        if(content.lower().__contains__('achoo')):
            await guild.send('bless you')
        if(content.lower().__contains__('thanks lil')):
            await guild.send("u welcome")
        if(content.lower() == '😮'):
            await guild.send(file=discord.File('Emoji_Cats/Surprise_cat.jpg'))
        if(content.lower() == '🤔'):
            await guild.send(file=discord.File('Emoji_Cats/Thinking_cat.jpg'))
        if(content.lower() == '😂'):
            await guild.send(file=discord.File('Emoji_Cats/Laughing_cat.jpg'))
        if(content.lower() == '😭'):
            await guild.send(file=discord.File('Emoji_Cats/Sobbing_cat.jpg'))
        if(content.lower() == '👍'):
            await guild.send(file=discord.File('Emoji_Cats/Thumbs_up_cat.png'))
        

async def setup(bot):
    await bot.add_cog(Fun(bot))
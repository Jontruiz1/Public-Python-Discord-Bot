import bson, discord, random, os
from discord.ext import commands
from pymongo import MongoClient

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.name = "=help, Tacos: {tacos}"

        self.taco_cats = os.listdir('Taco_cats/')
        self.mad_cats = os.listdir('Hiss_cats/')
        self.happy_cats = os.listdir('Happy_cats/')

        client = "MONGODB DATABASE CONNECTION STRING"
        cluster = MongoClient(client)
        db = cluster["CatBot"]
        self.pet_collection = db['pets']
        self.pet_result = self.pet_collection.find_one()
        self.taco_collection = db['tacos']
        self.taco_result = self.taco_collection.find_one()

        self.rejection_collection = db['rejections']
        self.rejection_result = self.rejection_collection.find_one()

        self.rejections = self.rejection_result['_count']
        self.pets = self.pet_result['_count']
        self.tacos = self.taco_result['_count']   

    @commands.command(brief='Eat a taco', description='Makes the cat eat a taco and increments the public taco counter')
    async def taco(self, ctx):
        global taco_result
        # create a string from message author and query to see if they have said this command before
        author = '{}'.format(ctx.message.author.id)
        query = {author : {'$exists' : True}}
        cursor = self.taco_collection.find_one(query)
        # if author does not exist, create and set to 1 for taco count
        if(cursor == None):
            self.taco_collection.update_one({'_id' : self.taco_result['_id']}, 
            {'$set': 
                    {author : bson.Int64(1) }
            })
        else:
            # increment author's taco count
            self.taco_collection.update_one({author : cursor[author]},
            {'$inc' : 
                    {author : 1}
            })
            
        # increment total taco count
        self.taco_collection.update_one({ '_count': self.taco_result['_count']},
        {'$inc' : 
            {'_count' : 1}
        })

        self.taco_result = self.taco_collection.find_one()
        self.tacos = self.taco_result['_count']

        activity = discord.Activity(type=discord.ActivityType.listening, name=self.name.format(tacos=self.tacos))
        await self.bot.change_presence(activity=activity)
        await ctx.send ('Nom🌮Eaten🌮{}🌮tacos🌮Nom\n'.format(self.tacos), file=discord.File('Taco_cats/' + self.taco_cats[random.randint(0, len(self.taco_cats)-1)]) )
    
    @commands.command(brief='Get your tacos', description='Gets the total number of tacos you have made the cat eat')
    async def mytacos(self, ctx):
        author = '{}'.format(ctx.message.author.id)
        query = {author : {'$exists' : True}}
        cursor = self.taco_collection.find_one(query)
        # if author does not exist no tacos have been eaten
        if(cursor == None):
            await ctx.send("You haven't had any tacos!")
        else:
            count = cursor[author]
            await ctx.send("You have eaten {} tacos".format(count))
    
    @commands.command(brief='Pet the cat!', description='Pet the cat, maybe the cat likes you')
    async def pet(self, ctx):
        # create a string from message author and query to see if they have said this command before
        author = '{}'.format(ctx.message.author.id)
        query = {author : {'$exists' : True}}
        cursor = self.pet_collection.find_one(query)
        # if author does not exist, create and set to 1 for pet count
        if(cursor == None):
            self.pet_collection.update_one({'_id' : self.pet_result['_id']}, 
            {'$set': 
                    {author : bson.Int64(1) }
            })
        else:
            # increment author's pet count
            self.pet_collection.update_one({author : cursor[author]},
            {'$inc' : 
                    {author : 1}
            })
            
        # increment total pet count
        self.pet_collection.update_one({ '_count': self.pet_result['_count']},
        {'$inc' : 
            {'_count' : 1}
        })

        self.pet_result = self.pet_collection.find_one()
        self.pets = self.pet_result['_count']

        query = {author : {'$exists' : True}}
        cursor = self.pet_collection.find_one(query)

        if(cursor[author] < 10):
            await ctx.send("**hiss**", file=discord.File('Hiss_cats/' + self.mad_cats[random.randint(0, len(self.mad_cats)-1)]))
        else:
            await ctx.send("*purr*", file=discord.File('Happy_cats/' + self.happy_cats[random.randint(0, len(self.happy_cats)-1)]))
    
    @commands.command(brief="Total rejection count")
    async def rejection(self, ctx):
        # create a string from message author and query to see if they have said this command before
        author = '{}'.format(ctx.message.author.id)
        query = {author : {'$exists' : True}}
        cursor = self.rejection_collection.find_one(query)
        # if author does not exist, create and set to 1 for rejection count
        if(cursor == None):
            self.rejection_collection.update_one({'_id' : self.rejection_result['_id']}, 
            {'$set': 
                    {author : bson.Int64(1) }
            })
        else:
            # increment author's rejection count
            self.rejection_collection.update_one({author : cursor[author]},
            {'$inc' : 
                    {author : 1}
            })
            
        # increment total rejection count
        self.rejection_collection.update_one({ '_count': self.rejection_result['_count']},
        {'$inc' : 
            {'_count' : 1}
        })

        self.rejection_result = self.rejection_collection.find_one()
        self.rejections = self.rejection_result['_count']

        await ctx.send('Total rejection count is {}.'.format(self.rejections))

    @commands.command(brief='Get your rejection count', description='Gets the total number of rejections you have received')
    async def myrejections(self, ctx):
        author = '{}'.format(ctx.message.author.id)
        query = {author : {'$exists' : True}}
        cursor = self.rejection_collection.find_one(query)
        # if author does not exist, they haven't been rejected yet
        if(cursor == None):
            await ctx.send("You have not been rejected yet! Wow!")
        else:
            count = cursor[author]
            await ctx.send("You have been rejected {} time(s) out of {}. That's {}% of the total rejection count.".format(count, self.rejections,(count/self.rejections) * 100))
    
    @commands.command(brief='Get the total rejection count', description='Gets the total number of rejections across everyone who has received one')
    async def rejections(self, ctx):
        await ctx.send('Total rejection count is {}.'.format(self.rejections))

async def setup(bot):
    await bot.add_cog(Data(bot))
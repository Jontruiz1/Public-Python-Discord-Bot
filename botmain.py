import discord
from discord.ext import commands
from pymongo import MongoClient

intents = discord.Intents.all()
intents.members = True

extensions = ['cogs.data', 'cogs.math', 'cogs.fun', 'cogs.admin', 'cogs.scraper']

name = "=help, Tacos: {tacos}"
client = "MONGODBDATABASE CONNECTION"
cluster = MongoClient(client)
db = cluster["CatBot"]

taco_collection = db['tacos']
taco_result = taco_collection.find_one()

tacos = taco_result['_count']
cluster.close()

activity = discord.Activity(type=discord.ActivityType.listening, name=name.format(tacos=tacos))
#activity = discord.Activity(type=discord.ActivityType.listening)
bot = commands.Bot(command_prefix='=', activity=activity, status=discord.Status.online, intents=intents)

#bot.remove_command('help') for the custom help command

@bot.event
async def on_ready():
    for i in extensions:    
        await bot.load_extension(i)

@bot.event
async def on_message(msg):
    if(msg.author != bot.user):
        await bot.process_commands(msg)

@bot.command(pass_context=True, brief='Reloads extensions', description='Reloads all currently active extensions')
@commands.is_owner()
async def reload(ctx):
    for i in extensions:
        await bot.reload_extension(i)
    await ctx.send('Extensions reloaded')

    
bot.run('DISCORD BOT AUTHENTICATION KEY') ## main bot 
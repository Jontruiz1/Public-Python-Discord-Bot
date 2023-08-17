from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
import discord, aiohttp

class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    '''
    @botmain.bot.event
    async def on_message(message):
        if not message.guild and message.author != botmain.bot:
            await message.channel.send('dmed!')
    
     
    @commands.command(Brief='Get Valorant patch notes - unimplemented')
    async def valopatcho(self, ctx):
        html = urlopen('https://playvalorant.com/en-us/news/game-updates/valorant-patch-notes-6-01/')
        bs = BeautifulSoup(html, 'html.parser')
        print(bs)
    '''    
    @commands.command(Brief='Gets the weather', description="Gets the current weather in a city, format='=weather cityname' ")
    async def weather(self, ctx, *args):
        API_Key = "OPENWEATHER API KEY"
        city_name = ''
        for word in args:
            city_name += str(word + ' ')
        city_name = city_name[:-1]
        
        # Provide a valid city name
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if(r.status == 200):
                    x = await r.json()
                    if['cod'] != '404':
                        y = x['main']
                        current_temperature = y['temp']
                        current_humidity = y['humidity']
                        current_name = x['name']
                        current_country = x['sys']['country']
                        
                        z = x['weather']
                        weather_description = z[0]['description']
                        weather_id = int(z[0]['id'])
                        dusty_cats = [731, 751, 761, 'Weather_cats/7_Dusty_cat.jpg']
                        foggy_cats = [701, 741, 'Weather_cats/8_Foggy_cat.jpg']
                        smoky_cats = [711, 721, 'Weather_cats/9_Smoky_cat.jpg']
                        windy_cats = [771, 781, 'Weather_cats/10_Windy_cat.gif']
                        group_cats = [
                            dusty_cats, 
                            foggy_cats, 
                            smoky_cats,
                            windy_cats]
                        
                        await ctx.send(str(current_name) + ', ' + str(current_country) + 
                        '\nTemperature (celsius, fahrenheit) = ' + '(' + 
                            str(round(current_temperature - 273.15, 1)) + ', ' + 
                            str(round( (current_temperature - 273.15) * (9/5) + 32, 1)) + ')' +
                "\nhumidity (in percentage) = " +
                            str(current_humidity) +
                "\n" +
                            str(weather_description))
                        if(weather_id < 300):
                            await ctx.send(file=discord.File('Weather_cats/0_Thunder_cat.jpg'))
                        elif(weather_id < 400):
                            await ctx.send(file=discord.File('Weather_cats/1_Drizzle_cat.jpg'))
                        elif(weather_id < 600):
                            await ctx.send(file=discord.File('Weather_cats/2_Rain_cat.jpg'))
                        elif(weather_id < 700):
                            await ctx.send(file=discord.File('Weather_cats/3_Snow_cat.jpg'))
                        elif(weather_id == 800):
                            await ctx.send(file=discord.File('Weather_cats/4_Clear_cat.jpg'))
                        elif(weather_id > 800):
                            await ctx.send(file=discord.File('Weather_cats/5_Cloudy_cat.jpg'))
                        else:
                            if(weather_id == 762):
                                await ctx.send(file=discord.File('Weather_cats/6_Volcano_cat.jpg'))
                            else:
                                for lst in group_cats:
                                    if(lst.__contains__(weather_id)):
                                        await ctx.send(file=discord.File(lst[len(lst)-1]))
                                        break
                    else:
                        await ctx.send("Something's wrong with the city name")
                        await ctx.send(file=discord.File('404_cat.jpg'))
                else:
                    await ctx.send("Something went wrong accessing openweathermap.org")
                    await ctx.send(file=discord.File('404_cat.jpg'))
async def setup(bot):
    await bot.add_cog(Scraper(bot))
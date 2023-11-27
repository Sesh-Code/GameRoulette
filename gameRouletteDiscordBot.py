from gameDatabaseAPICalls import gameNameCall
import discord
import random
from discord.ext import commands 
api = gameNameCall()

tokenFile = open("Discord Bot Token.txt", "rt")
tokenFileContents = tokenFile.read()
tokenFile.close()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True 
bot = commands.Bot(command_prefix='$', intents=intents)

### This bot calls the API RAWG Games Database, it pulls a random game from the API and then pulls the list of users from the server and picks one randomly
## This calls the bot command $roulette in the discord server and will pull a unique game that is rated betwen 75% - 100% on metacritic in the singleplayer format

@bot.command()
async def roulette(ctx):
    guild = ctx.guild
    members = [member for member in guild.members if not member.bot]

    if not members:
        await ctx.send("No users found.")
        return

    selectedMember = random.choice(members)
    selectedGame = api.apiCallGame()
    selectedGameStr = str(selectedGame)[1:-1]

    # Sending the message
    await ctx.send(f"@here\nThe user picked is: {selectedMember.mention}\nThe game picked is: {selectedGameStr}")
    
    
bot.run(tokenFileContents)
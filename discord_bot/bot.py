"""
Author: [Leni]
Version: 1.0
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello')
async def hello(ctx):
    """Responds with a greeting"""
    await ctx.send(f'Hello {ctx.author.name}!')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot's latency"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)

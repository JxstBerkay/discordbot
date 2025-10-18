import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import asyncio
load_dotenv()
token = os.getenv("token")

intens = discord.Intents.default()
intens.message_content = True
intens.members = True
intens.presences = True
bot = commands.Bot(command_prefix="!",intents=intens)

@bot.event
async def on_ready():
    print("Bot Is Ready!")

#Loading Files
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
#Starting The Bot
async def main():
    async with bot:
        await load()
        await bot.start(token)

asyncio.run(main())


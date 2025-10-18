import discord
from discord.ext import commands
from discord import app_commands
import json
with open('serverdata.json') as f:
    data = json.load(f)

filtered_words = data["swearwords"]

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded moderation...")
    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author == self.bot.user:
            return

        msg_content = ctx.content.lower()


        for word in filtered_words:
            if word in msg_content:
                await ctx.delete()
                await ctx.channel.send(f"{ctx.author.mention} Please do not use that word!")
                break 

        await self.bot.process_commands(ctx)

async def setup(bot):
    await bot.add_cog(moderation(bot))
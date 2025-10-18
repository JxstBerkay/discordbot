import discord
from discord.ext import commands
from discord import app_commands, Member
import json
import time
import math
cooldown = 86400
with open('userdata.json') as f:
    data = json.load(f)
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded Economy...")
  

    @app_commands.command(name="money",description="See The Money Of A User")
    async def Money(self, interaction: discord.Interaction, user: discord.Member=None):
        if user == None:
            user = interaction.user
        if data.get(user.name) is None:
            print("None")
            data[user.name] = {}
            data[user.name]["Money"] = 100
            with open('userdata.json', 'w') as f:
                json.dump(data, f, indent=4)
        

        embed = discord.Embed(
            title="Money",
            description=f"Here is the Money Of {user.mention} 💵",
            color=discord.Color.green()
        )

        embed.add_field(name="Money💵",value=data[user.name]["Money"])
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Made with discord.py")

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="daily",description="Get A Daily Sum Of Money")
    async def Daily(self, interaction: discord.Interaction):
        user = interaction.user
        if data.get(user.name) is None:
            data[user.name] = {}
            data[user.name]["Money"] = 100
        


        if "LastClaimed" not in data[user.name]:
            data[user.name]["LastClaimed"] = time.time()
            data[user.name]["Money"] += 300
            with open('userdata.json', 'w') as f:
                json.dump(data, f, indent=4)   
            await interaction.response.send_message("Sucessfully Claimed 300 Money!",ephemeral=True)
            return
        

        timeinsecs = data[user.name].get("LastClaimed", 0)
        elapsed = time.time() - timeinsecs
        if elapsed >= cooldown:
            data[user.name]["Money"] += 300
            await interaction.response.send_message(
                "✅ Successfully claimed 300 Money!", ephemeral=True
            )
            data[user.name]["LastClaimed"] = time.time()
        else:
            remaining = cooldown - elapsed
            hours = math.floor(remaining // 3600)
            minutes = math.floor((remaining % 3600) // 60)
            seconds = math.floor(remaining % 60)
            await interaction.response.send_message(
                f"⏳ You need to wait **{hours}h {minutes}m {seconds}s** before claiming again.", ephemeral=True
            )


        with open('userdata.json', 'w') as f:
                json.dump(data, f, indent=4)   

    
    @app_commands.command(name="leaderboard",description="see the users with the highest amount of Money")
    async def leaderboard(self, interaction: discord.Interaction):
        print("run")
        users = {}
        i = 0
        for user in data:
            users[user] = data[user]["Money"]
            i += 1
            if i == 10:
                break
        
        print(users)
        sorted_dict = dict(sorted(users.items(), key=lambda item: item[1], reverse=True))
        print(sorted_dict)
        embed = discord.Embed(
            title="People With The Most Money",
            color=discord.Color.green()
        )
        counter = 1
        for i in sorted_dict:
            print(sorted_dict[i])
            embed.add_field(name=f"**{counter}**",value=f"**{i}** {sorted_dict[i]} Money",inline=False)
            counter += 1

        
    
        await interaction.response.send_message(embed=embed, ephemeral=True)
    @app_commands.command(name="give",description="Give a User Some Of Your Money!")
    async def give(self, interaction: discord.Interaction,user: discord.Member=None, amount: int=None):
        if user == None:
           await interaction.response.send_message("You Need To Choose A User!",ephemeral=True)
           return
        if data.get(user.name) is None:
            data[user.name] = {}
            data[user.name]["Money"] = 100


        if amount <= data[interaction.user.name]["Money"]:
            data[user.name]["Money"] += amount 
            data[interaction.user.name]["Money"] -= amount
            await interaction.response.send_message(f"{interaction.user.mention} Gave {user.mention} {amount} Money✅")
        else:
            await interaction.response.send_message(f"You Dont Have Enough Money!",ephemeral=True)

        with open('userdata.json', 'w') as f:
                json.dump(data, f, indent=4)   

            


async def setup(bot):
    await bot.add_cog(Economy(bot))
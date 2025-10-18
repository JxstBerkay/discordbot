import discord
from discord.ext import commands
from discord import app_commands, Member
from datetime import datetime
Ownerid = 1091482982113615923
class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded slash commands...")
        
    @app_commands.command(name="userinfo",description="Get userinfo")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member=None):
        if user == None:
            user = interaction.user
        embed = discord.Embed(
            title="User Info",
            description=f"Here is some info about {user.mention} 👋",
            color=discord.Color.blue()
        )
        
        join_date = user.joined_at  
        formatted_date = join_date.strftime("%Y-%m-%d")
        created_date = user.created_at
        formatted_date2 = created_date.strftime("%Y-%m-%d")
        embed.add_field(name="Join Date", value=formatted_date)
        embed.add_field(name="Created Account In", value=formatted_date2)
        if user.bot == True:
             embed.add_field(name="Bot?", value="✅")
        else:
            embed.add_field(name="Bot?", value="❌")

        if user.id == Ownerid:
            embed.add_field(name="Owner?", value="✅")
        else:
             embed.add_field(name="Owner?", value="❌")

        roles = []
        for role in user.roles:
            if role.name == "@everyone":
                roles.append(role.name)  
            else:
                roles.append(role.mention)  

        roles_string = ", ".join(roles)

        embed.add_field(name="Roles", value=roles_string, inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="Made with discord.py")

        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="clear",description="clear")
    async def clear(self, interaction: discord.Interaction, limit:int=None):
        await interaction.response.defer(ephemeral=True)  #let Discord know we’re working
        deleted = await interaction.channel.purge(limit=limit)
        await interaction.followup.send(
            f"✅ Successfully deleted {len(deleted)} messages.", ephemeral=True
        )
    
    @app_commands.command(name="sync", description="Sync slash commands")
    @app_commands.checks.has_permissions(administrator=True) 
    async def sync(self, interaction: discord.Interaction, guild_only: bool = True):
        if guild_only:
            guild = discord.Object(id=interaction.guild_id)
            synced = await self.bot.tree.sync(guild=guild)
            await interaction.response.send_message(
                f"✅ Synced {len(synced)} commands to this guild.", ephemeral=True
            )
        else:
            synced = await self.bot.tree.sync()
            await interaction.response.send_message(
                f"✅ Synced {len(synced)} commands globally.", ephemeral=True
            )
    
        

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
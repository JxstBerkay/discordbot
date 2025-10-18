import discord
from discord.ext import commands
from discord import app_commands
import json
with open('serverdata.json') as f:
    data = json.load(f)

class CloseButton(discord.ui.View):
     @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🎫")
     async def button_callback(self,interaction:discord.Interaction,button):
        role_names = [r.name for r in interaction.user.roles]

        if any(name in role_names for name in ("Staff", "Owner")):
            await interaction.channel.delete()
        else:
            await interaction.response.send_message(
                "You can't delete the ticket.", ephemeral=True
            )

class MyView(discord.ui.View): 
    @discord.ui.button(label="Open A Ticket", style=discord.ButtonStyle.success, emoji="🎫") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, interaction,button):
        staffteam = discord.utils.get(interaction.guild.roles,name="Staff")
        channel_overwrites = {interaction.user:discord.PermissionOverwrite(view_channel=True,send_messages=True),
                              staffteam:discord.PermissionOverwrite(view_channel=True,send_messages=True),
                              interaction.guild.default_role:discord.PermissionOverwrite(view_channel=False)}
        
        channel = await interaction.guild.create_text_channel(name=f"Ticket#{data["TicketNumber"]}",overwrites=channel_overwrites)

        await channel.send(staffteam.mention)

        embed = discord.Embed(
                title="Our Staff Team Will Be With You Soon",
                description=f"Please Wait until One Of Our staff Members Comes to Help You",
                color=discord.Color.blue()
            )   
        
        await channel.send(embed=embed,view=CloseButton())
        data["TicketNumber"] += 1
        with open('serverdata.json', 'w') as f:
                json.dump(data, f, indent=4)

        

class ticketcreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded Tickets")
    
    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author == self.bot.user:
            return

        msg_content = ctx.content.lower()

        if msg_content == "!ticketcreate":
            print("creating...")
            embed = discord.Embed(
                title="Ticket",
                description=f"Click On The Button To Open a Ticket!",
                color=discord.Color.blue()
            )   

            await ctx.channel.send(embed=embed,view=MyView())


        await self.bot.process_commands(ctx)



async def setup(bot):
    await bot.add_cog(ticketcreate(bot))
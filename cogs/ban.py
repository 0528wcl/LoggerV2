import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Ban(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @app_commands.command(name = "ban", description = "Bans a user from the server")
    @commands.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member == interaction.user:
            description = "You cannot ban yourself!"
            color = self.RED
        else:
            await member.ban(reason = reason)
            color = self.GREEN
            description = f"{member.name} has been banned!"

        embed = discord.Embed(
            color = color,
            description = description,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User", value = f"{member.mention}", inline = False)
        embed.add_field(name = "Ban Reason", value = f"{reason}", inline = False)
        embed.set_author(name = interaction.user.name, icon_url = interaction.user.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)

        await interaction.response.send_message(embed = embed)

async def setup(client):
    from main import RED, BLUE, GREEN
    await client.add_cog(Ban(client, RED, BLUE, GREEN))
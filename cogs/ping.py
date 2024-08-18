import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Ping(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @app_commands.command(name = "ping", description = "Sends you the latency of the bot")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color = self.BLUE,
            description = f"Pong! {round(self.client.latency * 1000, 0)}ms",
            timestamp = datetime.now()
        )
        embed.set_author(name = interaction.user.name, icon_url = interaction.user.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
        await interaction.response.send_message(embed = embed)

async def setup(client):
    from main import RED, BLUE, GREEN
    await client.add_cog(Ping(client, RED, BLUE, GREEN))
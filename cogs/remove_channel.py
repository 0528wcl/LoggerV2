import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from main import load_channels, save_channels

class RemoveChannel(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @app_commands.command(name = "remove_channel", description = "Removes a channel from logging in your server")
    @commands.has_permissions(administrator = True)
    async def remove_channel(self, interaction: discord.Interaction):
        channel_id = str(interaction.message.channel.id)
        guild_id = str(interaction.guild.id)

        channels = load_channels()

        if guild_id in channels:
            if channels[guild_id] == channel_id:
                channels.pop(guild_id)
                save_channels(channels)
                description = f"Successfully removed the channel {interaction.message.channel.mention} for this server."
                color = self.GREEN
            else:
                description = f"This channel is not set to log on this server. If you want to remove logging, remove <#{channels[guild_id]}>"
                color = self.RED
        else:
            description = "No channel is set for this server. Send `!set_channel` to set up this channel."
            color = self.RED

        embed = discord.Embed(
            color = color,
            description = description,
            timestamp = datetime.now()
        )
        embed.set_author(name = interaction.user.name, icon_url = interaction.user.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)

        await interaction.response.send_message(embed = embed)

async def setup(client):
    from main import RED, BLUE, GREEN
    await client.add_cog(RemoveChannel(client, RED, BLUE, GREEN))
import discord
from discord.ext import commands
from datetime import datetime
from main import load_channels, save_channels

class RemoveChannel(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def remove_channel(self, ctx):
        channel_id = str(ctx.message.channel.id)
        guild_id = str(ctx.guild.id)

        channels = load_channels()

        if guild_id in channels:
            if channels[guild_id] == channel_id:
                channels.pop(guild_id)
                save_channels(channels)
                description = f"Successfully removed the channel {ctx.message.channel.mention} for this server."
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
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.avatar.url)

        await ctx.send(embed = embed)

async def setup(client):
    from main import RED, BLUE, GREEN
    await client.add_cog(RemoveChannel(client, RED, BLUE, GREEN))
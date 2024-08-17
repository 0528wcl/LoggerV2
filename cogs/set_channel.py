import discord
from discord.ext import commands
from datetime import datetime
from main import load_channels, save_channels

class SetChannel(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def set_channel(self, ctx):
        channel_id = str(ctx.message.channel.id)
        guild_id = str(ctx.guild.id)

        channels = load_channels()

        if guild_id in channels:
            if channels[guild_id] == channel_id:
                description = f"The channel {ctx.message.channel.mention} is already set for this server."
                color = self.RED
            else:
                description = f"There is already a channel set for this server: <#{channels[guild_id]}>"
                color = self.RED
        else:
            channels[guild_id] = channel_id
            save_channels(channels)
            description = f"Successfully set the channel {ctx.message.channel.mention} for this server."
            color = self.GREEN

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
    await client.add_cog(SetChannel(client, RED, BLUE, GREEN))
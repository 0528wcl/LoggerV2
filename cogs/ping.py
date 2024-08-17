import discord
from discord.ext import commands
from datetime import datetime

class Ping(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            color = self.BLUE,
            description = f"Pong! {round(self.client.latency * 1000, 0)}ms",
            timestamp = datetime.now()
        )
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.avatar.url)
        await ctx.send(embed = embed)

async def setup(client):
    from main import RED, BLUE, GREEN
    await client.add_cog(Ping(client, RED, BLUE, GREEN))
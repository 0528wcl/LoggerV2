import discord
from discord.ext import commands
import asyncio
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

os.system("cls" if os.name == "nt" else "clear")

logging.basicConfig(level = logging.INFO)

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

RED = discord.Color.from_rgb(255, 175, 175)
GREEN = discord.Color.from_rgb(175, 255, 175)
BLUE = discord.Color.from_rgb(175, 175, 255)

CHANNELS = "channels.json"

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.guild_typing = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = "!", intents = intents, help_command = None)

# Functions
def load_channels() -> dict:
    try:
        if os.path.getsize(CHANNELS) > 0:
            with open(CHANNELS, "r") as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {}

def save_channels(channels: dict) -> None:
    with open(CHANNELS, "w") as f:
        json.dump(channels, f, indent = 4)

def get_log_channel(guild_id: str):
    channels = load_channels()
    return channels.get(guild_id)

# Discord Bot
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "현승이티팬티"), status=discord.Status.idle)
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        description = "You don't have permission to use this command."
    elif isinstance(error, commands.CommandNotFound):
        description = "Command not found."
    else:
        description = "An error occurred while processing the command."
        logging.error(f"Error in command {ctx.command}: {error}")

    embed = discord.Embed(
        color = RED,
        description = description,
        timestamp = datetime.now()
    )
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)

    await ctx.send(embed = embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = "Bot Commands",
        description = "Here are the available commands",
        color = BLUE,
        timestamp = datetime.now()
    )
    embed.add_field(name = "!help", value = "Displays this message.", inline = False)
    embed.add_field(name = "!ping", value = "Check the bot's latency.", inline = False)
    embed.add_field(name = "!set_channel", value = "Set the current channel as the logging channel.", inline = False)
    embed.add_field(name = "!remove_channel", value = "Remove the current channel from the logging channels.", inline = False)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)

    await ctx.send(embed = embed)

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        color = BLUE,
        description = f"Pong! {round(client.latency * 1000, 0)}ms",
        timestamp = datetime.now()
    )
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(administrator = True)
async def set_channel(ctx):
    channel_id = str(ctx.message.channel.id)
    guild_id = str(ctx.guild.id)

    channels = load_channels()
    logging.info(f"Loaded channels: {channels}")

    if guild_id in channels:
        if channels[guild_id] == channel_id:
            description = f"The channel {ctx.message.channel.mention} is already set for this server."
            color = RED
        else:
            description = f"There is already a channel set for this server: <#{channels[guild_id]}>."
            color = RED
    else:
        channels[guild_id] = channel_id
        save_channels(channels)
        description = f"Successfully set the channel {ctx.message.channel.mention} for this server."
        color = GREEN

    embed = discord.Embed(
        color = color,
        description = description,
        timestamp = datetime.now()
    )
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
    
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(administrator = True)
async def remove_channel(ctx):
    channel_id = str(ctx.message.channel.id)
    guild_id = str(ctx.guild.id)

    channels = load_channels()

    if guild_id in channels:
        if channels[guild_id] == channel_id:
            channels.pop(guild_id)
            save_channels(channels)
            description = f"Successfully removed the channel {ctx.message.channel.mention} for this server."
            color = GREEN
        else:
            description = f"This channel is not set to log on this server. Send `!set_channel` to set up this channel."
            color = RED
    else:
        description = "No channel is set for this server. Send `!set_channel` to set up this channel."
        color = RED

    embed = discord.Embed(
        color = color,
        description = description,
        timestamp = datetime.now()
    )
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)

    await ctx.send(embed = embed)

# Logging
@client.event
async def on_message_delete(message):
    guild_id = str(message.guild.id)
    log_channel_id = get_log_channel(guild_id)
    if not log_channel_id:
        return

    channel = client.get_channel(int(log_channel_id))
    embed = discord.Embed(
        title = "Message Deleted",
        description = f"Message from {message.author.mention} was deleted in {message.channel.mention}",
        color = RED,
        timestamp = datetime.now()
    )
    embed.add_field(name = "Content", value = message.content, inline = False)
    embed.set_author(name = message.author.name, icon_url = message.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
    await channel.send(embed = embed)

@client.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return

    guild_id = str(before.guild.id)
    log_channel_id = get_log_channel(guild_id)
    if not log_channel_id:
        return

    channel = client.get_channel(int(log_channel_id))
    embed = discord.Embed(
        title = "Message Edited",
        description = f"Message by {before.author.mention} edited in {before.channel.mention}",
        color = BLUE,
        timestamp = datetime.now()
    )
    embed.add_field(name = "Before", value = before.content, inline = False)
    embed.add_field(name = "After", value = after.content, inline = False)
    embed.set_author(name = before.author.name, icon_url = before.author.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
    await channel.send(embed = embed)

@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    log_channel_id = get_log_channel(guild_id)
    if not log_channel_id:
        return

    channel = client.get_channel(int(log_channel_id))
    embed = discord.Embed(
        title = "Member Joined",
        description = f"{member.display_name} joined the server.",
        color = GREEN,
        timestamp = datetime.now()
    )
    embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
    embed.add_field(name = "ID", value = f"```js\nUSER = {member.id}\n```", inline = False)
    embed.set_thumbnail(url = member.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar)
    await channel.send(embed = embed)

@client.event
async def on_member_remove(member):
    guild_id = str(member.guild.id)
    log_channel_id = get_log_channel(guild_id)
    if not log_channel_id:
        return
    
    roles = [role.mention for role in member.roles if role.name != "@everyone"]
    roles_list = ", ".join(roles)

    channel = client.get_channel(int(log_channel_id))
    embed = discord.Embed(
        title = "Member Left",
        description = f"{member.display_name} left the server.",
        color = RED,
        timestamp = datetime.now()
    )
    embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
    embed.add_field(name = "Roles", value = roles_list, inline = False)
    embed.add_field(name = "ID", value = f"```js\nUSER = {member.id}\n```", inline = False)
    embed.set_thumbnail(url = member.avatar.url)
    embed.set_footer(text = client.user, icon_url = client.user.avatar)
    await channel.send(embed = embed)

@client.event
async def on_voice_state_update(member, before, after):
    guild_id = str(member.guild.id)
    log_channel_id = get_log_channel(guild_id)
    if not log_channel_id:
        return

    channel = client.get_channel(int(log_channel_id))

    # User joins a voice channel
    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            title = "Voice Channel Joined",
            description = f"{member.display_name} joined the voice channel {after.channel.mention}.",
            color = GREEN,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User Information", value=f"{member} ({member.mention})", inline = False)
        embed.add_field(name = "ID", value=f"```js\nUSER = {member.id}\nCHANNEL = {after.channel.id}\n```", inline = False)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
        await channel.send(embed = embed)

    # User leaves a voice channel
    elif before.channel is not None and after.channel is None:
        await asyncio.sleep(1)
        # Check the audit logs for a kick event
        async for entry in member.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_disconnect):
            if entry.target and entry.target.id == member.id:
                kicker = entry.user
                description = f"{member.display_name} was kicked from the voice channel {before.channel.mention} by {kicker.mention}."
                break
        else:
            description = f"{member.display_name} left the voice channel {before.channel.mention}."
        
        embed = discord.Embed(
            title = "Voice Channel Left",
            description = description,
            color = RED,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
        embed.add_field(name = "User ID", value=f"```js\nUSER = {member.id}\nCHANNEL = {before.channel.id}\n```", inline = False)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
        await channel.send(embed = embed)

    # User moves from one voice channel to another
    elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
        await asyncio.sleep(1)
        # Check the audit logs for a move event (member update)
        async for entry in member.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_update):
            if entry.target and entry.target.id == member.id and hasattr(entry.after, 'channel') and entry.after.channel.id == after.channel.id:
                mover = entry.user
                description = f"{member.display_name} was moved from {before.channel.mention} to {after.channel.mention} by {mover.mention}."
                break
        else:
            description = f"{member.display_name} moved from {before.channel.mention} to {after.channel.mention}."
        
        embed = discord.Embed(
            title = "Voice Channel Moved",
            description = description,
            color = BLUE,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
        embed.add_field(name = "User ID", value=f"```js\nUSER = {member.id}\nOLD = {before.channel.id}\nNEW = {after.channel.id}\n```", inline = False)
        embed.set_author(name = member.name, icon_url = member.avatar.url)
        embed.set_footer(text = client.user, icon_url = client.user.avatar.url)
        await channel.send(embed = embed)

client.run(TOKEN)
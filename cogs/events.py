import discord, asyncio, logging
from discord.ext import commands
from datetime import datetime
from itertools import cycle
from main import get_log_channel, RED, BLUE, GREEN

class Events(commands.Cog):
    def __init__(self, client, RED, BLUE, GREEN):
        self.client = client
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Logged in as {self.client.user}")
        try:
            synced_commands = await self.client.tree.sync()
            logging.info(f"Synced {len(synced_commands)} slash commands")
        except Exception as e:
            logging.warning(f"An error occurred while syncing slash commands. ", e)

        status_messages = cycle(["인간 시대의 끝이 도래했다","08년생로블록스프로지망생김현승"])

        while True:
            await self.client.change_presence(
                activity = discord.Activity(
                    type = discord.ActivityType.custom,
                    state = f"!help | {next(status_messages)}"
                ),
                status = discord.Status.do_not_disturb
            )
            await asyncio.sleep(30)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            description = "You don't have permission to use this command."
        else:
            description = "An error occurred while processing the command."
            logging.error(f"Error in command {ctx.command}: {error}")

        embed = discord.Embed(
            color = RED,
            description = description,
            timestamp = datetime.now()
        )
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)

        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild_id = str(message.guild.id)
        log_channel_id = get_log_channel(guild_id)
        if not log_channel_id:
            return

        channel = self.client.get_channel(int(log_channel_id))
        embed = discord.Embed(
            title = "Message Deleted",
            description = f"Message from {message.author.mention} was deleted in {message.channel.mention}",
            color = self.RED,
            timestamp = datetime.now()
        )
        embed.add_field(name = "Content", value = message.content, inline = False)
        embed.set_author(name = message.author.name, icon_url = message.author.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return

        guild_id = str(before.guild.id)
        log_channel_id = get_log_channel(guild_id)
        if not log_channel_id:
            return

        channel = self.client.get_channel(int(log_channel_id))
        embed = discord.Embed(
            title = "Message Edited",
            description = f"Message by {before.author.mention} edited in {before.channel.mention}",
            color = self.BLUE,
            timestamp = datetime.now()
        )
        embed.add_field(name = "Before", value = before.content, inline = False)
        embed.add_field(name = "After", value = after.content, inline = False)
        embed.set_author(name = before.author.name, icon_url = before.author.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        log_channel_id = get_log_channel(guild_id)
        if not log_channel_id:
            return

        channel = self.client.get_channel(int(log_channel_id))
        embed = discord.Embed(
            title = "Member Joined",
            description = f"{member.display_name} joined the server.",
            color = self.GREEN,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
        embed.add_field(name = "ID", value = f"```js\nUSER = {member.id}\n```", inline = False)
        embed.set_thumbnail(url = member.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.avatar)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        log_channel_id = get_log_channel(guild_id)
        if not log_channel_id:
            return
        
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles_list = ", ".join(roles)

        channel = self.client.get_channel(int(log_channel_id))
        embed = discord.Embed(
            title = "Member Left",
            description = f"{member.display_name} left the server.",
            color = self.RED,
            timestamp = datetime.now()
        )
        embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
        embed.add_field(name = "Roles", value = roles_list, inline = False)
        embed.add_field(name = "ID", value = f"```js\nUSER = {member.id}\n```", inline = False)
        embed.set_thumbnail(url = member.display_avatar.url)
        embed.set_footer(text = self.client.user, icon_url = self.client.user.avatar)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild_id = str(member.guild.id)
        log_channel_id = get_log_channel(guild_id)
        if not log_channel_id:
            return

        channel = self.client.get_channel(int(log_channel_id))

        # User joins a voice channel
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title = "Voice Channel Joined",
                description = f"{member.display_name} joined the voice channel {after.channel.mention}.",
                color = self.GREEN,
                timestamp = datetime.now()
            )
            embed.add_field(name = "User Information", value=f"{member} ({member.mention})", inline = False)
            embed.add_field(name = "ID", value=f"```js\nUSER = {member.id}\nCHANNEL = {after.channel.id}\n```", inline = False)
            embed.set_author(name = member.name, icon_url = member.display_avatar.url)
            embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
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
                color = self.RED,
                timestamp = datetime.now()
            )
            embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
            embed.add_field(name = "User ID", value=f"```js\nUSER = {member.id}\nCHANNEL = {before.channel.id}\n```", inline = False)
            embed.set_author(name = member.name, icon_url = member.display_avatar.url)
            embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
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
                color = self.BLUE,
                timestamp = datetime.now()
            )
            embed.add_field(name = "User Information", value = f"{member} ({member.mention})", inline = False)
            embed.add_field(name = "User ID", value=f"```js\nUSER = {member.id}\nOLD = {before.channel.id}\nNEW = {after.channel.id}\n```", inline = False)
            embed.set_author(name = member.name, icon_url = member.display_avatar.url)
            embed.set_footer(text = self.client.user, icon_url = self.client.user.display_avatar.url)
            await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild_id = str(after.guild.id)
        if hasattr(after, 'communication_disabled_until') and before.communication_disabled_until != after.communication_disabled_until:
            if after.communication_disabled_until is not None:
                guild_id = str(after.guild.id)
                log_channel_id = get_log_channel(guild_id)
                if not log_channel_id:
                    return

                channel = self.client.get_channel(int(log_channel_id))
                timeout_until = after.communication_disabled_until
                time_remaining = timeout_until - discord.utils.utcnow()

                embed = discord.Embed(
                    title = "Member Timed Out",
                    description = f"{after.display_name} has been timed out.",
                    color = self.RED,
                    timestamp = datetime.now()
                )
                embed.add_field(name = "Timed out until", value = f"{timeout_until}", inline = False)
                embed.add_field(name = "Time remaining", value = f"{time_remaining}", inline = False)
                embed.add_field(name = "User ID", value = f"```js\n{after.id}\n```", inline = False)
                embed.set_thumbnail(url = after.display_avatar.url)
                embed.set_footer(text = self.client.user.name, icon_url = self.client.user.display_avatar.url)

                await channel.send(embed = embed)

async def setup(client):
    await client.add_cog(Events(client, RED, BLUE, GREEN))
import discord, asyncio, os, logging, json
from discord.ext import commands
from dotenv import load_dotenv

os.system("cls" if os.name == "nt" else "clear")

logging.basicConfig(level = logging.INFO)

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

RED = discord.Color.from_rgb(255, 175, 175)
GREEN = discord.Color.from_rgb(175, 255, 175)
BLUE = discord.Color.from_rgb(175, 175, 255)

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.guild_typing = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = "!", intents = intents, help_command = None)

# -- Funcions -- #
CHANNELS = "./data/channels.json"

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

# -- Bot -- #
async def load_cogs():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await client.load_extension(f"cogs.{f[:-3]}")

async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
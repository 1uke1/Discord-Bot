import discord
from discord.ext import commands
import os
from dotenv import load_dotenv  

load_dotenv()  
TOKEN = os.getenv("DISCORD_TOKEN")  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Yapper is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

async def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

async def main():
    await load_all_cogs()
    await bot.start(TOKEN)  

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
from discord.ext import commands
from discord import Message

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        
        if message.author == self.bot.user:
            return

        msg = message.content.lower().strip()
        
        if msg.startswith("hello"):
            await message.channel.send(f"Yooo {message.author.mention}")
        elif msg.startswith("bye"):
            await message.channel.send(f"Later {message.author.mention}")
        elif msg.startswith("hi"):
            await message.channel.send(f"Hey {message.author.mention}")
        elif msg.startswith("amir"):
            await message.channel.send(f"Amir? who da fuk is that guy?")
        elif msg.startswith("dcurt"):
            await message.channel.send(f"Dcum? 29 years old with back problems?")
        
async def setup(bot):
    await bot.add_cog(Greetings(bot))

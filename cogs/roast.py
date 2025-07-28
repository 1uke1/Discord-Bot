import random
import discord
from discord import app_commands
from discord.ext import commands

class RoastMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roasts = [
            "You're like a cloud. When you disappear, it's a beautiful day.",
            "You're the reason shampoo has instructions.",
            "If I had a dollar for every smart thing you said, I'd be broke.",
            "You're the human version of a participation trophy.",
            "You bring everyone so much joy… when you leave the room.",
            "You're as useless as the 'g' in lasagna.",
            "You have something on your chin… no, the third one down.",
            "You're the reason the gene pool needs a lifeguard.",
            "You're not stupid; you just have bad luck thinking.",
            "Your secrets are safe with me. I never listen when you tell them.",
            "You're proof that evolution can go in reverse.",
            "You're the kind of person who claps when the plane lands.",
            "You're like a software update. Whenever I see you, I think, 'Not now.'",
            "You're as sharp as a butter knife.",
            "You're like a 404 error—nobody can find your purpose.",
            "You're not even on the same page—you’re not even in the same book.",
            "You're the reason they put directions on Pop-Tarts.",
            "Mirrors can't talk. Lucky for you, they can't laugh either.",
            "You're the human version of a participation trophy.",
            "If common sense were common, you'd be a unicorn.",
            "I've seen salad that dresses better than you."
        ]

    @app_commands.command(name="roastme", description="Get absolutely roasted by the bot")
    async def roastme(self, interaction: discord.Interaction):
        roast = random.choice(self.roasts)
        await interaction.response.send_message(f" {roast}")

    @app_commands.command(name="roast", description="Roast someone else by tagging them")
    @app_commands.describe(user="The user you want to roast")
    async def roast(self, interaction: discord.Interaction, user: discord.User):
        roast = random.choice(self.roasts)
        await interaction.response.send_message(f" {user.mention}, {roast}")

async def setup(bot):
    await bot.add_cog(RoastMe(bot))
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import pytz

TIMEZONE = pytz.timezone("America/Los_Angeles") 

class ReminderSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reminddaily", description="Set a daily recurring reminder")
    @app_commands.describe(time="Time in HH:MM (24hr format)", task="Reminder text")
    async def reminddaily(self, interaction: discord.Interaction, time: str, task: str):
        try:
            hour, minute = map(int, time.split(":"))
        except:
            await interaction.response.send_message(" Invalid time format! Use HH:MM (24hr)", ephemeral=True)
            return

        async def daily_task():
            while True:
                now = datetime.now(TIMEZONE)
                target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if target <= now:
                    target += timedelta(days=1)
                await asyncio.sleep((target - now).total_seconds())
                await interaction.channel.send(f"Daily Reminder: {task} (from {interaction.user.mention})")

        await interaction.response.send_message(f"Daily reminder set for **{time}**: `{task}`")
        asyncio.create_task(daily_task())

    @app_commands.command(name="remind", description="Set a reminder on a specific weekday and time")
    @app_commands.describe(day="Day of the week", time="Time in HH:MM (24hr format)", task="Reminder text")
    async def remind(self, interaction: discord.Interaction, day: str, time: str, task: str):
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
        }

        if day.lower() not in weekdays:
            await interaction.response.send_message("Invalid day. Use Monday–Sunday.", ephemeral=True)
            return

        try:
            hour, minute = map(int, time.split(":"))
        except:
            await interaction.response.send_message("Invalid time format! Use HH:MM (24hr)", ephemeral=True)
            return

        now = datetime.now(TIMEZONE)
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        target_day = weekdays[day.lower()]

        while reminder_time.weekday() != target_day or reminder_time <= now:
            reminder_time += timedelta(days=1)

        delay = (reminder_time - now).total_seconds()

        async def one_time_task():
            await asyncio.sleep(delay)
            await interaction.channel.send(f"Reminder: {task} (from {interaction.user.mention})")

        await interaction.response.send_message(f"Reminder set for **{day} at {time}**: `{task}`")
        asyncio.create_task(one_time_task())


async def setup(bot):
    await bot.add_cog(ReminderSlash(bot))

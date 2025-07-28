# Discord-Bot

A fun and modular Discord bot built with Python. Includes reminders, meme fetcher, roasts, and greeting commands.
Welcome to Yapper Bot, a simple Discord bot built using 'discord.py'. This is version 1 of the project, which focuses on basic interaction and scheduling features.

#FEATURES

- Slash commands to set:
  - One-time reminders (/remind)
  - Daily recurring reminders (/reminddaily)
  - Roast command (/roast)
  - Random meme pull from Lemmy API (/meme)

#STRUCTURE

- greetings.py - Handles text-based greetings (no slash)
- reminders.py - Manages /remind and /reminddaily
- roast.py - Roast command (/roast)
- memes.py - Pull memes from Lemmy API (/meme)

#Tech Stack

- (Python 3)
- (discord.py)
- (aiohttp) for external API calls
- (pytz) for timezone handling

#FUTURE VERSIONS

- V2: Buttons, dropdowns, better UI
- V3: Connect to local LLM for chatbot responses
- V4: Admin commands and moderation tools

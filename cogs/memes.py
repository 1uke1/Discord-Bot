import random
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import json

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="meme", description="Random meme from Lemmy")
    async def meme(self, interaction: discord.Interaction):
        # Try different Lemmy API endpoints
        endpoints = [
            "https://lemmy.world/api/v3/post/list?community_name=memes&sort=Hot&limit=20",
            "https://lemmy.world/api/v3/post/list?community_name=memes&sort=Active&limit=20",
            "https://lemmy.ml/api/v3/post/list?community_name=memes&sort=Hot&limit=20"
        ]
        
        headers = {
            'User-Agent': 'DiscordBot/1.0',
            'Accept': 'application/json'
        }
        
        for i, url in enumerate(endpoints):
            try:
                print(f"Trying endpoint {i+1}: {url}")  
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=15) as response:
                        print(f"Response status: {response.status}")  
                        
                        if response.status != 200:
                            print(f"Failed with status {response.status}")
                            continue
                        
                        
                        response_text = await response.text()
                        print(f"Response length: {len(response_text)}") 
                        
                        try:
                            data = json.loads(response_text)
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e}")
                            continue
                        
                        print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                        
                        
                        posts = None
                        if "posts" in data:
                            posts = data["posts"]
                        elif "data" in data and isinstance(data["data"], list):
                            posts = data["data"]
                        elif isinstance(data, list):
                            posts = data
                        
                        print(f"Found {len(posts) if posts else 0} posts")
                        
                        if not posts:
                            continue
                        
                        # Filter for image posts
                        image_posts = []
                        for post_item in posts:
                            # Handle different post structures
                            if isinstance(post_item, dict):
                                if "post" in post_item:
                                    post = post_item["post"]
                                else:
                                    post = post_item
                                
                                url_link = post.get("url", "")
                                name = post.get("name", "")
                                
                                print(f"Checking post: {name[:50]}... URL: {url_link[:100]}") 
                                
                                
                                if url_link and (
                                    any(url_link.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']) or
                                    'i.imgur.com' in url_link or
                                    'i.redd.it' in url_link
                                ):
                                    image_posts.append(post_item)
                        
                        print(f"Found {len(image_posts)} image posts")  
                        
                        if image_posts:
                            
                            selected_item = random.choice(image_posts)
                            if "post" in selected_item:
                                selected_post = selected_item["post"]
                            else:
                                selected_post = selected_item
                            
                            title = selected_post.get("name", "Meme")
                            image_url = selected_post.get("url", "")
                            post_id = selected_post.get("id", "")
                            
                            # Create proper post URL
                            if "lemmy.world" in url:
                                post_url = f"https://lemmy.world/post/{post_id}"
                            elif "lemmy.ml" in url:
                                post_url = f"https://lemmy.ml/post/{post_id}"
                            else:
                                post_url = image_url
                            
                            
                            embed = discord.Embed(
                                title=title[:256],
                                url=post_url,
                                color=discord.Color.green()
                            )
                            embed.set_image(url=image_url)
                            embed.set_footer(text="From Lemmy memes")
                            
                            await interaction.response.send_message(embed=embed)
                            return
                            
            except aiohttp.ClientTimeout:
                print(f"Timeout on endpoint {i+1}")
                continue
            except Exception as e:
                print(f"Error on endpoint {i+1}: {str(e)}")
                continue
        
        
        await interaction.response.send_message("Sorry, couldn't fetch memes from Lemmy right now. All endpoints failed.")

    @app_commands.command(name="test_lemmy", description="Test Lemmy API connection")
    async def test_lemmy(self, interaction: discord.Interaction):
        """Debug command to test the API"""
        url = "https://lemmy.world/api/v3/post/list?community_name=memes&sort=Hot&limit=5"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    status = response.status
                    text = await response.text()
                    
                    await interaction.response.send_message(
                        f"**Status:** {status}\n"
                        f"**Response length:** {len(text)}\n"
                        f"**First 500 chars:** ```{text[:500]}```"
                    )
        except Exception as e:
            await interaction.response.send_message(f"Error testing API: {str(e)}")

async def setup(bot):
    await bot.add_cog(Memes(bot))
"""ESN Discord bot starter (Python, discord.py). MIT License. https://esnoffical.com"""
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
COLOR = 0x6C5CE7


class Bot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


bot = Bot()


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} ({bot.user.id})")


@bot.tree.command(name="ping", description="Show the bot's latency")
async def ping(interaction: discord.Interaction) -> None:
    embed = discord.Embed(title="Pong!", description=f"{round(bot.latency * 1000)} ms", color=COLOR)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="hello", description="Say hi")
async def hello(interaction: discord.Interaction) -> None:
    embed = discord.Embed(description=f"Hey {interaction.user.mention}! 👋", color=COLOR)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="serverinfo", description="Show info about this server")
@app_commands.guild_only()
async def serverinfo(interaction: discord.Interaction) -> None:
    g = interaction.guild
    embed = discord.Embed(title=g.name, color=COLOR)
    embed.add_field(name="Members", value=str(g.member_count))
    embed.add_field(name="Created", value=discord.utils.format_dt(g.created_at, "D"))
    if g.icon:
        embed.set_thumbnail(url=g.icon.url)
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set DISCORD_TOKEN in .env first.")
    bot.run(TOKEN)

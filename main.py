import os

import discord

from api import list_incidents

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with dns"))
    print("Bot is ready")
    list_incidents()


if __name__ == "__main__":
    client.run(os.getenv("TOKEN"))

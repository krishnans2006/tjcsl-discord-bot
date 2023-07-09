import os
from datetime import timedelta

import discord
from discord.ext import tasks

from api import list_incidents

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with dns"))
    print("Bot is ready")
    list_incidents()


@tasks.loop(minutes=1)
async def check_incidents():
    new_incidents = list_incidents(duration=timedelta(minutes=1))
    for new_incident in new_incidents:
        print(new_incident)
    print("Checked for new incidents")


@check_incidents.before_loop
async def before_check_incidents():
    await client.wait_until_ready()


if __name__ == "__main__":
    check_incidents.start()
    client.run(os.getenv("TOKEN"))

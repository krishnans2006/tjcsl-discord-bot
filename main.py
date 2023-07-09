import os
from datetime import timedelta

import discord
from discord.ext import tasks

from api import list_incidents

intents = discord.Intents.default()

client = discord.Client(intents=intents)

guild_id = 1037482630838489179
channel_id = 1127402489013076038


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with dns"))
    print("Bot is ready")
    list_incidents()


@tasks.loop(minutes=1)
async def check_incidents():
    new_incidents = list_incidents(duration=timedelta(minutes=1))
    channel = None
    for incident, timestamp, is_resolved in new_incidents:
        if not channel:
            channel = client.get_guild(guild_id).get_channel(channel_id)
        if is_resolved:
            embed = discord.Embed(
                title="Resolved Incident",
                color=discord.Color.green(),
                timestamp=timestamp,
            )
        else:
            embed = discord.Embed(
                title="New Incident",
                color=discord.Color.red(),
                timestamp=timestamp,
            )
        embed.add_field(name="For", value=incident["attributes"]["name"], inline=True)
        embed.set_author(
            name="Better Stack",
            url="https://uptime.betterstack.com/team/58077/monitors",
            icon_url="https://pbs.twimg.com/profile_images/1380564657505718275/TToZVzli_400x400.jpg",
        )

        await channel.send(embed=embed)
    print("Checked for new incidents")


@check_incidents.before_loop
async def before_check_incidents():
    await client.wait_until_ready()


if __name__ == "__main__":
    check_incidents.start()
    client.run(os.getenv("TOKEN"))

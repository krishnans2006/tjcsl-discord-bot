import os
from datetime import timedelta
import random

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from api import list_incidents
from status import select_status

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

guild_id = 1037482630838489179
channel_id = 1127402489013076038

base_team_url = "https://uptime.betterstack.com/team/58077"

new_incident_description = """\u200B
**{name}** - {url}

**Cause:** {cause}

**Start:** <t:{start}:f> (<t:{start}:R>)
\u200B
"""

resolved_incident_description = """\u200B
**{name}** - {url}

**Cause:** {cause}

**Start:** <t:{start}:f> (<t:{start}:R>)
**End:** <t:{end}:f> (<t:{end}:R>)
**Duration:** `{duration}`
\u200B
"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with ur mom"))
    print("Bot is ready")


@tasks.loop(minutes=5)
async def change_status():
    status = select_status()
    await client.change_presence(activity=discord.Game(name=f"with {status}"))


@change_status.before_loop
async def before_change_status():
    await client.wait_until_ready()


@tasks.loop(minutes=1)
async def check_incidents():
    new_incidents = list_incidents(duration=timedelta(minutes=1))
    channel = None
    for incident, start_time, resolve_time, is_resolved in new_incidents:
        print(incident)

        name = incident["attributes"]["name"]
        url = incident["attributes"]["url"]
        cause = incident["attributes"]["cause"]
        start = round(start_time.timestamp())

        if not channel:
            channel = client.get_guild(guild_id).get_channel(channel_id)

        if is_resolved:
            end = round(resolve_time.timestamp())
            duration = timedelta(seconds=end - start)
            embed = discord.Embed(
                title="Resolved Incident",
                description=resolved_incident_description.format(
                    name=name, url=url, cause=cause, start=start, end=end, duration=duration
                ),
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="New Incident",
                description=new_incident_description.format(
                    name=name, url=url, cause=cause, start=start
                ),
                color=discord.Color.red(),
            )
        embed.set_author(
            name="Better Stack",
            icon_url="https://pbs.twimg.com/profile_images/1380564657505718275/TToZVzli_400x400.jpg",
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Better Stack Dashboard",
                url=f"{base_team_url}/monitors",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Status Page",
                url="https://status.tjhsst.edu",
            )
        )

        await channel.send(content="<@&1127698117370851552>", embed=embed, view=view)
    print("Checked for new incidents")


@check_incidents.before_loop
async def before_check_incidents():
    await client.wait_until_ready()


if __name__ == "__main__":
    check_incidents.start()
    change_status.start()
    client.run(os.getenv("TOKEN"))

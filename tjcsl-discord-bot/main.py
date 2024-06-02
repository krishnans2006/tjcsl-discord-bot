from datetime import timedelta
import logging
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from api import list_incidents
from status import select_status
import config as C

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

logger = logging.getLogger("main")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with ur mom"))
    logger.info("Bot is ready")


@tasks.loop(seconds=C.STATUS_CHANGE_INTERVAL_SECONDS)
async def change_status():
    status = select_status()
    await client.change_presence(activity=discord.Game(name=f"with {status}"))
    logger.info(f"Changed status to {status}")


@change_status.before_loop
async def before_change_status():
    await client.wait_until_ready()


@tasks.loop(seconds=C.TASK_LOOP_INTERVAL_SECONDS)
async def check_incidents():
    new_incidents = list_incidents(duration=timedelta(seconds=C.PAST_INCIDENT_SECONDS))
    channel = None
    for incident, start_time, resolve_time, is_resolved in new_incidents:
        logger.info(str(incident))

        name = incident["attributes"]["name"]
        url = incident["attributes"]["url"]
        cause = incident["attributes"]["cause"]
        start = round(start_time.timestamp())

        if not channel:
            channel = client.get_guild(C.GUILD_ID).get_channel(C.CHANNEL_ID)

        if is_resolved:
            end = round(resolve_time.timestamp())
            duration = timedelta(seconds=end - start)
            embed = discord.Embed(
                title="Resolved Incident",
                description=C.RESOLVED_INCIDENT_DESCRIPTION.format(
                    name=name, url=url, cause=cause, start=start, end=end, duration=duration
                ),
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="New Incident",
                description=C.NEW_INCIDENT_DESCRIPTION.format(
                    name=name, url=url, cause=cause, start=start
                ),
                color=discord.Color.red(),
            )
        embed.set_author(
            name="Better Stack",
            icon_url=C.BETTERSTACK_LOGO,
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Better Stack Dashboard",
                url=f"{C.BETTERSTACK_TEAM_URL}/monitors",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Status Page",
                url=C.STATUSPAGE_URL,
            )
        )

        await channel.send(content=f"<@&{C.ROLE_PING_ID}>", embed=embed, view=view)
    logger.info("Checked for new incidents")


@check_incidents.before_loop
async def before_check_incidents():
    await client.wait_until_ready()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] (%(name)s) %(asctime)s  %(message)-500s",
        handlers=(
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "info.log")),
        ),
    )
    check_incidents.start()
    change_status.start()
    client.run(C.BOT_TOKEN)

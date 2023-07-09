from datetime import datetime, timedelta
import os
from typing import Iterator

import requests

BASE_URL = "https://uptime.betterstack.com/api/v2/"
Incident = dict[str, str | dict[str, str]]


def call_api(endpoint: str, **kwargs) -> dict:
    response = requests.get(
        BASE_URL + endpoint,
        headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
        timeout=30,
        **kwargs,
    )
    return response.json()


def list_incidents(
    duration: timedelta = timedelta(minutes=1),
) -> Iterator[tuple[Incident, datetime, bool]] | None:
    current_incidents = call_api("incidents")["data"]
    for incident in current_incidents:
        start_time = datetime.strptime(
            incident["attributes"]["started_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if start_time > datetime.now() - duration:
            yield incident, start_time, False
        resolve_time = datetime.strptime(
            incident["attributes"]["resolved_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if resolve_time > datetime.now() - duration:
            yield incident, resolve_time, True
    yield current_incidents[0], datetime.now(), False

from datetime import datetime, timedelta, timezone
import os
from typing import Iterator

import requests

BASE_URL = "https://uptime.betterstack.com/api/v2/"
Incident = dict[str, str | dict[str, str]]
IncidentList = Iterator[tuple[Incident, datetime, datetime | None, bool]]


def call_api(endpoint: str, **kwargs) -> dict:
    response = requests.get(
        BASE_URL + endpoint,
        headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
        timeout=30,
        **kwargs,
    )
    return response.json()


def list_incidents(duration: timedelta = timedelta(minutes=1)) -> IncidentList | None:
    current_incidents = call_api("incidents")["data"]
    for incident in current_incidents:
        start_time = datetime.fromisoformat(incident["attributes"]["started_at"])
        if start_time > datetime.now(tz=timezone.utc) - duration:
            yield incident, start_time, None, False

        if incident["attributes"]["resolved_at"] is None:
            continue
        resolve_time = datetime.fromisoformat(incident["attributes"]["resolved_at"])
        if resolve_time > datetime.now(tz=timezone.utc) - duration:
            yield incident, start_time, resolve_time, True

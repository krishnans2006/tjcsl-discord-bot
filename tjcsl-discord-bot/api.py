from datetime import datetime, timedelta, timezone
from dateutil import parser
import os
from typing import Iterator

import config as C

import requests

Incident = dict[str, str | dict[str, str]]
IncidentList = Iterator[tuple[Incident, datetime, datetime | None, bool]]


def call_api(endpoint: str, **kwargs) -> dict:
    response = requests.get(
        C.API_BASE_URL + endpoint,
        headers={"Authorization": f"Bearer {C.API_TOKEN}"},
        timeout=30,
        **kwargs,
    )
    return response.json()


def list_incidents(duration: timedelta = timedelta(minutes=1)) -> IncidentList | None:
    current_incidents = call_api("incidents")["data"]
    for incident in current_incidents:
        start_time = parser.parse(incident["attributes"]["started_at"])
        if start_time > datetime.now(tz=timezone.utc) - duration:
            yield incident, start_time, None, False

        if incident["attributes"]["resolved_at"] is None:
            continue
        resolve_time = parser.parse(incident["attributes"]["resolved_at"])
        if resolve_time > datetime.now(tz=timezone.utc) - duration:
            yield incident, start_time, resolve_time, True

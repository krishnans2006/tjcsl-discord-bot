from datetime import datetime, timedelta, timezone
from dateutil import parser
import os
from typing import Iterator

import config as C

import requests

Incident = dict[str, str | dict[str, str]]
IncidentList = Iterator[tuple[Incident, datetime, datetime | None, bool]]

pending_incidents = set()
resolved_incidents = set()


def call_api(endpoint: str, **kwargs) -> dict:
    response = requests.get(
        C.API_BASE_URL + endpoint,
        headers={"Authorization": f"Bearer {C.API_TOKEN}"},
        timeout=30,
        **kwargs,
    )
    return response.json()


def list_incidents(duration: timedelta) -> IncidentList | None:
    current_incidents = call_api("incidents")["data"]
    for incident in current_incidents:
        # Warning: Confusing logic
        if incident["id"] in resolved_incidents:
            continue

        start_time = parser.parse(incident["attributes"]["started_at"])

        if incident["attributes"]["resolved_at"] is None:
            if start_time > datetime.now(tz=timezone.utc) - duration:
                if incident["id"] in pending_incidents:
                    continue
                pending_incidents.add(incident["id"])
                yield incident, start_time, None, False
            continue

        resolve_time = parser.parse(incident["attributes"]["resolved_at"])
        if resolve_time > datetime.now(tz=timezone.utc) - duration:
            resolved_incidents.add(incident["id"])
            yield incident, start_time, resolve_time, True

import os
from typing import Iterator

import requests

BASE_URL = "https://uptime.betterstack.com/api/v2/"
Incident = dict[str, str | dict[str, str]]

sent_incidents = []


def call_api(endpoint: str, **kwargs) -> dict:
    response = requests.get(
        BASE_URL + endpoint,
        headers={"Authorization": f"Bearer {os.getenv('API_TOKEN')}"},
        timeout=30,
        **kwargs,
    )
    return response.json()


def fetch_incidents() -> None:
    global sent_incidents
    with open("incidents.txt", "r", encoding="utf-8") as f:
        sent_incidents = f.read().splitlines()


def list_incidents() -> Iterator[Incident] | None:
    current_incidents = call_api("incidents")["data"]
    for incident in current_incidents:
        if incident["id"] not in sent_incidents:
            sent_incidents.append(incident["id"])
            with open("incidents.txt", "a", encoding="utf-8") as f:
                f.write(incident["id"] + "\n")
            yield incident

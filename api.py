import os

import requests

BASE_URL = "https://uptime.betterstack.com/api/v2/"

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


def list_incidents() -> dict:
    current_incidents = call_api("incidents")["data"]
    print(current_incidents)

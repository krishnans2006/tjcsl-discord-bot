# TJCSL Discord Bot

A Discord bot for the TJ CSL Discord Server, emulating Better Stack webhooks using the Better Stack API.


## Setup

```bash
poetry install
```

## Required Configs
Set these variables in `tjcsl-discord-bot/config/secret.py`

- `TOKEN` - Discord Bot Token
- `API_TOKEN` - Better Stack API Token

## Run

```bash
poetry shell
python tjcsl-discord-bot/main.py
```

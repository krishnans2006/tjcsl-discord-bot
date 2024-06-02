# This file stores default config settings
# To override, set any variable in config/secret.py

# Important things to change:
BOT_TOKEN = ""
API_TOKEN = ""

# Control settings
TASK_LOOP_INTERVAL_SECONDS = 1
STATUS_CHANGE_INTERVAL_SECONDS = 300
PAST_INCIDENT_SECONDS = 60

# API settings
API_BASE_URL = "https://uptime.betterstack.com/api/v2/"

# Message location
GUILD_ID = 1037482630838489179
CHANNEL_ID = 1127402489013076038

# Message constants
ROLE_PING_ID = 1127698117370851552
BETTERSTACK_LOGO = "https://pbs.twimg.com/profile_images/1380564657505718275/TToZVzli_400x400.jpg"
STATUSPAGE_URL = "https://status.tjhsst.edu"
BETTERSTACK_TEAM_URL = "https://uptime.betterstack.com/team/58077"

# Message structures
NEW_INCIDENT_DESCRIPTION = """\u200B
**{name}** - {url}

**Cause:** {cause}

**Start:** <t:{start}:f> (<t:{start}:R>)
\u200B
"""

RESOLVED_INCIDENT_DESCRIPTION = """\u200B
**{name}** - {url}

**Cause:** {cause}

**Start:** <t:{start}:f> (<t:{start}:R>)
**End:** <t:{end}:f> (<t:{end}:R>)
**Duration:** `{duration}`
\u200B
"""

# Import overrides from secret.py
try:
    from .secret import *
except ImportError:
    pass

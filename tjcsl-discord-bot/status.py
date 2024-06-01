import random

STATUSES = {
    "services": ("dns", "ipa", "ceph", "slurm"),
    "sites": (
        "ion",
        "director",
        "webmail",
        "tin",
        "jupyterhub",
        "mattermost",
        "matterless",
        "gitlab",
        "gitbook",
        "runbooks",
        "grafana",
        "netbox",
    ),
    "legendary": ("karel", "wumpus", "stobar", "core0", "asm"),
    "epic": (
        "altair",
        "antipodes",
        "chatham",
        "cocos",
        "galapagos",
        "gandalf",
        "gorgona",
        "overlord",
        "sirius",
        "torch",
        "vega",
        "waverider",
        "NAND",
        "NOR",
        "XNAND",
        "XNOR",
        "XOR",
    ),
    "rare": (
        "duplication",
        "firebreath",
        "flight",
        "immortality",
        "invisibility",
        "mindcontrol",
        "omnipresence",
        "speed",
        "timetravel",
        "xrayvision",
    ),
    "common": tuple(f"borg{i}" for i in range(1, 41)) + tuple(f"hpc{i}" for i in range(1, 13)),
}

STATUS_WEIGHTS = {
    "services": 30,
    "sites": 15,
    "legendary": 10,
    "epic": 5,
    "rare": 5,
    "common": 1,
}


def select_status():
    total_weight = sum(STATUS_WEIGHTS.values())
    choice = random.randint(1, total_weight)
    for status, weight in STATUS_WEIGHTS.items():
        if choice <= weight:
            return random.choice(STATUSES[status])
        choice -= weight
    return None

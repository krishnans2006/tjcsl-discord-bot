# fmt: off
services = ["dns", "ipa", "ceph", "slurm"]
sites = ["ion", "director", "webmail", "tin", "jupyterhub", "mattermost", "matterless", "gitlab", "gitbook", "runbooks", "grafana", "netbox"]

# cluster
common_machines = ["borg1", "borg2", "borg3", "borg4", "borg5", "borg6", "borg7", "borg8", "borg9", "borg10", "borg11", "borg12", "borg13", "borg14", "borg15", "borg16", "borg17", "borg18", "borg19", "borg20", "borg21", "borg22", "borg23", "borg24", "borg25", "borg26", "borg27", "borg28", "borg29", "borg30", "borg31", "borg32", "borg33", "borg34", "borg35", "borg36", "borg37", "borg38", "borg39", "borg40", "hpc1", "hpc2", "hpc3", "hpc4", "hpc5", "hpc6", "hpc7", "hpc8", "hpc9", "hpc10", "hpc11", "hpc12"]

# ups
rare_machines = ["duplication", "firebreath", "flight", "immortality", "invisibility", "mindcontrol", "omnipresence", "speed", "timetravel", "xrayvision"]

# vmservers, switches
epic_machines = ["altair", "antipodes", "chatham", "cocos", "galapagos", "gandalf", "gorgona", "overlord", "sirius", "torch", "vega", "waverider", "NAND", "NOR", "XNAND", "XNOR", "XOR"]

# op
legendary_machines = ["karel", "wumpus", "stobar", "core0", "asm"]

statuses = services * 100 + sites * 50 + legendary_machines * 50 + epic_machines * 10 + rare_machines * 5 + common_machines
# fmt: on

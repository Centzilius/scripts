#!/usr/bin/env python3

import requests
from subprocess import call
from time import sleep

def get_latest_version():
    versions = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    assert versions["versions"][0]["id"] in versions["latest"].values()
    return versions["versions"][0]

def get_server_url(version):
    return requests.get(version["url"]).json()["downloads"]["server"]["url"]

with open("VERSION", "r") as f:
    current_version = f.read()

latest_version = get_latest_version()
if latest_version["id"] != current_version:
    return_code = call(["screen", "-S", "corona", "-p", "0", "-X", "stuff", "say Updating to {}^Msave-all^Mstop^M".format(latest_version["id"])])
    if return_code:
        exit()
    sleep(10)
    r = requests.get(get_server_url(latest_version), stream=True)
    if r.status_code == 200:
        with open("server.jar", 'wb') as f:
            for chunk in r:
                f.write(chunk)
        with open("VERSION", "w") as f:
            f.write(latest_version["id"])
    call(["screen", "-dmS", "corona", "java", "-jar", "server.jar"])

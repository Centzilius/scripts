#!/usr/bin/env python3

import requests

from time import sleep
from subprocess import call, check_output, CalledProcessError

def get_latest_version():
    versions = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    assert versions["versions"][0]["id"] in versions["latest"].values()
    return versions["versions"][0]

def get_server_url(version):
    return requests.get(version["url"]).json()["downloads"]["server"]["url"]

def get_tmux_windows(session):
    try:
        output = check_output(["tmux", "list-windows", "-t", "coronacraft", "-F", "#W"]).decode().split("\n")
        output.remove("")
        return output
    except CalledProcessError:
        return []

def get_tmux_session_existence(session):
    return not call(["tmux", "has-session", "-t", session])

def send_tmux_keys(session, window, cmd_list, pane=0):
    return not call(["tmux", "send-keys", "-t", "{}:{}.{}".format(session, window, pane)] + cmd_list)

def stop_server():
    if get_tmux_session_existence("coronacraft"):
        if "mc" in get_tmux_windows("coronacraft"):
            if send_tmux_keys("coronacraft", "mc", ["say Updating", "Enter", "save-all", "Enter", "stop", "Enter"]):
                while "mc" in get_tmux_windows("coronacraft"):
                    sleep(1)
            else:
                raise Exception("WTF!")

def start_server():
    if get_tmux_session_existence("coronacraft"):
        if call(["tmux", "new-window", "-d", "-n", "mc", "-t", "coronacraft", "java -jar server.jar"]):
            raise Exception("WTF2!")
    else:
        if call(["tmux", "new-session", "-d", "-s", "coronacraft", "-n", "mc", "java -jar server.jar"]):
            raise Exception("WTF3!")

try:
    with open("VERSION", "r") as f:
        current_version = f.read()
except FileNotFoundError:
        current_version = "dummy"

latest_version = get_latest_version()
if latest_version["id"] != current_version:
    stop_server()
    r = requests.get(get_server_url(latest_version), stream=True)
    if r.status_code == 200:
        with open("server.jar", "wb") as f:
            for chunk in r:
                f.write(chunk)
        with open("VERSION", "w") as f:
            f.write(latest_version["id"])
    start_server()

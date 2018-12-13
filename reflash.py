#!/usr/bin/python3
import json
import time
import sys
import os

network = {
    "type": "station",
    "ip": "10.1.0.113",
    "ssid": "Hackafe",
    "psk": "correcthorsebatterystaple",
    "server": "10.1.0.110",
    "gateway": "10.1.0.1",
    "subnet": "255.255.0.0",
    "dns": "8.8.8.8"
}
sensor = {
    "type": "alcohol",
    "read_rate": 2,
    "pin": 0
}

with open("./conf.json", "r") as FILE:
    nodes = json.loads(FILE.read())["nodes"]

only_flash = ""
if len(sys.argv) > 1:
    only_flash = sys.argv[1]

for node in nodes:
    if only_flash:
        if only_flash != node["ip"]:
            continue
    config = {}
    config["network"] = dict(network)
    config["network"]["ip"] = node["ip"]
    config["sensor"] = dict(sensor)
    config["sensor"].update(node["sensor"])
    with open("node_conf.json", "w") as FILE:
        FILE.write(json.dumps(config))
    flaship = node["ip"]
    if len(sys.argv) > 2:
        flaship = sys.argv[2]
    resp = os.system("ping -c 2 {} >/dev/null".format(flaship))
    if resp == 0:
        if "--html" in sys.argv:
            os.system("./webrepl/webrepl_cli.py -p admin index.html {}:/index.html".format(flaship))
            sys.exit(0)
        os.system("./webrepl/webrepl_cli.py -p admin node_conf.json {}:/conf.json".format(flaship))
        time.sleep(0.2)
        os.system("./webrepl/webrepl_cli.py -p admin boot.py {}:/boot.py".format(flaship))
        if node["ip"] == config["network"]["server"]:
            time.sleep(0.2)
            os.system("./webrepl/webrepl_cli.py -p admin servernode.py {}:/servernode.py".format(flaship))
            time.sleep(0.2)
            os.system("./webrepl/webrepl_cli.py -p admin index.html {}:/index.html".format(flaship))
            for path in ['ws_connection.py', 'ws_server.py']:
                time.sleep(0.2)
                os.system("./webrepl/webrepl_cli.py -p admin upy-websocket-server/{} {}:/{}".format(path, flaship, path))
            os.system("./webrepl/webrepl_cli.py -p admin reconnecting-websocket.min.js {}:/reconnecting-websocket.min.js".format(flaship))
        else:
            time.sleep(0.2)
            os.system("./webrepl/webrepl_cli.py -p admin sensors.py {}:/sensors.py".format(flaship))
    else:
        print("Could not connect to {}".format(flaship))

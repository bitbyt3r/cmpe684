import network
import webrepl
import json

with open("conf.json", "r") as CONF:
    config = json.loads(CONF.read())
print("Read configuration from file.")
print(config)

if config['network']['type'] == "station":
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(config['network']['ssid'], config['network']['psk'])
    print("Connecting to {}".format(config['network']['ssid']))
    while not sta_if.isconnected():
        pass
    print("Connected to network:", sta_if.ifconfig())
    sta_if.ifconfig((
        config['network']['ip'],
        config['network']['subnet'],
        config['network']['gateway'],
        config['network']['dns']
    ))
    print("IP Changed to:", sta_if.ifconfig())
    webrepl.start()
else:
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=config['network']['ssid'], password=config['network']['ssid'])
    print("Running Access Point:", ap_if.ifconfig())
    ap_if.ifconfig((
        config['network']['ip'],
        config['network']['subnet'],
        config['network']['gateway'],
        config['network']['dns']
    ))
    print("IP Changed to:", ap_if.ifconfig())
    webrepl.start()

if config['network']['ip'] == config['network']['server']:
    print("This node is the server.")
    import servernode
    servernode.run(config)
else:
    print("This node is a sensor.")
    import sensors
    sensors.run(config)
import neopixel
import machine
import network
import webrepl
import socket
import json
import time
import dht
import os

def run(config):
    np = neopixel.NeoPixel(machine.Pin(3), 4)
    
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((config['network']['ip'], 684))
    def report_sensor_reading(reading):
        s.sendto(json.dumps(reading), (config['network']['server'], 684))

    if config['sensor']['type'] == "pulse":
        adc = machine.ADC(0)
        readings = []
        state = False
        beat_time = time.ticks_ms()
        while True:
            try:
                reading = adc.read()
                readings.append(reading)
                readings = readings[max(0,len(readings)-100):]
                maxima, minima = max(readings), min(readings)
                if state and reading > 0.8*maxima:
                    state = False
                elif not(state) and reading < 0.5*maxima:
                    state = True
                    now = time.ticks_ms()
                    delta = now-beat_time
                    beat_time = now
                    report_sensor_reading({
                        "value": 60000/delta,
                        "type": "bpm"
                    })
                report_sensor_reading({
                    "value": reading,
                    "type": "pulse"
                })
                for i in range(4):
                    if reading-minima > (i+1)*((maxima-minima)/3):
                        np[i] = (10,0,0)
                    else:
                        np[i] = (0,0,0)
                np.write()
                time.sleep(1/config['sensor']['read_rate'])
            except:
                print("Failed to report sensor value.")
    if config['sensor']['type'] == "dht22":
        d = dht.DHT22(machine.Pin(config['sensor']['pin']))
        while True:
            try:
                d.measure()
                report_sensor_reading({
                    "value": d.temperature(),
                    "type": "temperature"
                })
                report_sensor_reading({
                    "value": d.humidity(),
                    "type": "humidity"
                })
                time.sleep(1/config['sensor']['read_rate'])
            except:
                print("Failed to report sensor value.")
    if config['sensor']['type'] == "alcohol":
        adc = machine.ADC(0)
        while True:
            try:
                reading = adc.read()
                report_sensor_reading({
                    "value": reading,
                    "type": "alcohol"
                })
                for i in range(4):
                    if reading > (i+1)*200:
                        np[i] = (0,10,0)
                    else:
                        np[i] = (0,0,0)
                np.write()
                time.sleep(1/config['sensor']['read_rate'])
            except:
                print("Failed to report sensor value.")
    if config['sensor']['type'] == "flex":
        adc = machine.ADC(0)
        maxima, minima = 0, 1024
        while True:
            try:
                reading = adc.read()
                maxima, minima = max(reading, maxima), min(reading, minima)
                report_sensor_reading({
                    "value": (reading-minima)/(maxima-minima),
                    "type": "flex"
                })
                for i in range(4):
                    if reading > (i+1)*200:
                        np[i] = (0,0,10)
                    else:
                        np[i] = (0,0,0)
                np.write()
                time.sleep(1/config['sensor']['read_rate'])
            except:
                print("Failed to report sensor value.")
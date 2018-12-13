from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import neopixel
import machine
import socket
import time
import json

def run(config):
    np = neopixel.NeoPixel(machine.Pin(3), 4)
    subscribers = []

    def publish(data):
        for subscriber in subscribers:
            try:
                subscriber.connection.write(data)
            except ClientClosedError:
                subscriber.connection.close()
                subscribers.remove(subscriber)

    class WebServer(WebSocketServer):
        def __init__(self):
            super().__init__("index.html", 2)

        def _make_client(self, conn):
            client = WebSocketClient(conn)
            subscribers.append(client)
            return client

    server = WebServer()
    server.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((config['network']['server'], 684))
    while True:
        raw_data, addr = s.recvfrom(512)
        for i in range(4):
            np[i] = (0,0,0)
        np.write()
        time.sleep(0.01)
        for i in range(4):
            np[i] = (0,10,0)
        np.write()
        publish(raw_data)

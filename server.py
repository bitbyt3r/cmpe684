#!/usr/bin/python3
from socket import *
import json
import sys

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 684))
while True:
  rawdata, addr = s.recvfrom(1024)
  data = json.loads(rawdata)
  if len(sys.argv) > 1:
    if data["type"] in sys.argv:
      print(data)
  else:
    print(data)

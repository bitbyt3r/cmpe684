#!/bin/bash
echo "Reboot esp in programmer mode"
read
esptool --port /dev/ttyUSB0 erase_flash
echo "Reboot esp in programmer mode"
read
esptool --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.bin

sleep 5

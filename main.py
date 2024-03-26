import network
# Commented for future use.
# import json
# import urequests
# import sys
import machine
import onewire
import ds18x20
import time
import secrets

CONNECTED = False

wlan = network.WLAN(network.STA_IF)

def connect():
    wlan.active(True)
    wlan.connect(secrets.WIFI_NETWORK, secrets.WIFI_PASSWORD)
    while wlan.isconnected() == False:
        time.sleep(5)
        continue
    ip = wlan.ifconfig()[0]
    print("Connected on " + ip)
    return ip

connect()

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
# print('Found DS devices: ', roms)

while True:
  if wlan.isconnected() is False:
      connect()
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    # print(rom)
    tempC = ds_sensor.read_temp(rom)
    print('temperature (ºC):', "{:.2f}".format(tempC))
    # tempF = tempC * (9/5) +32
    # print('temperature (ºF):', "{:.2f}".format(tempF))
    print()
  time.sleep(1)


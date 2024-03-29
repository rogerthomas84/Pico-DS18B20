# Commented for future use.
import json
import urequests
import sys
import machine
import onewire
import ds18x20
import time
import secrets
from wifi_connection import WiFiConnection

connection = WiFiConnection(secrets.WIFI_NETWORK, secrets.WIFI_PASSWORD)
connection.connect()


def send_data(send_payload):
    try:
        if connection.isconnected() is False:
            connection.connect()
        request = urequests.post(
            secrets.API_URL,
            headers=secrets.HEADERS,
            timeout=5,
            data=json.dumps(send_payload)
        )
        res = request.content
        request.close()
        data = json.loads(res)
        if data['status'] == 'ok':
            print('Data sent successfully')
            return True
        print('Error sending data')
    except Exception as e:
        print(e)
        time.sleep(1)
    return False


ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
# print('Found DS devices: ', roms)

while True:
    if connection.isconnected() is False:
        connection.connect()
    try:
        ds_sensor.convert_temp()
        time.sleep(1)
        for rom in roms:
            # print(rom)
            tempC = ds_sensor.read_temp(rom)
            print('temperature (ºC):', "{:.2f}".format(tempC))
            # tempF = tempC * (9/5) +32
            # print('temperature (ºF):', "{:.2f}".format(tempF))
            temp = "{:.2f}".format(tempC)
            payload = {
                "data": temp,
                "device": secrets.DEVICE_KEY,
                "ip": connection.get_ip()
            }
            send_data(payload)
        time.sleep(29)
    except Exception as e:
        print(e)
        time.sleep(29)
        continue

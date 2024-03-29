import network
import time


class WiFiConnection:

    def __init__(self, ssid, password):
        self.ip = None
        self.wlan = None
        self.ssid = ssid
        self.password = password

    def connect(self):
        print(f"Connecting to {self.ssid}...")
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected():
            time.sleep(5)
            continue
        self.ip = self.wlan.ifconfig()[0]
        print(f"Connected on {self.ip}")
        return self.ip

    def get_ip(self):
        return self.ip

    # noinspection SpellCheckingInspection
    def isconnected(self):
        return self.wlan is not None and self.wlan.isconnected()

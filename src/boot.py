import network
from machine import Pin
from config import Config

# Turn off vendor OS debugging messages
import esp
esp.osdebug(None)

import gc
gc.collect()

config = Config()

wifiConfig = config.wifiConfig
ssid = wifiConfig.getSSID()
password = wifiConfig.getPassword()

# Set the ESP as a Wifi station. This enables the esp to exist on
# the existing wifi network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# do not proceed until the ESP is connected to the network
while station.isconnected() == False:
  pass
print('Connection successful')

deskIpConfig = config.deskIpConfig
station.ifconfig((deskIpConfig.getIp(), '255.255.255.0', deskIpConfig.getGateway(), '8.8.8.8'))

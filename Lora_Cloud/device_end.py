# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import time
import machine
from machine import Timer
from machine import Pin

from network import LoRa
import socket
import time

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.sEU868
# United States = LoRa.US915

py = Pysense()
lt = LTR329ALS01(py)

def run() :
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    previous_light = 0

    while True:
		ch0_value, ch1_value = lt.light()
		if ch0_value != previous_light :
			s.send(b''+str(ch0_value))
			print(ch0_value)
			previous_light = ch0_value


'''
    while True:
        data = s.recv(64)
        if data[0:4] == b'Ping':
            print(data)
            s.send(b'Pong')
        time.sleep(3)

'''
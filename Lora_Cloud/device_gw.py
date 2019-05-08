from network import LoRa
import network
import time
import machine
import os
import socket 
from lib.mqtt import MQTTClient 
from machine import Timer
import pycom
from lib.pysense import Pysense
from lib.LTR329ALS01 import LTR329ALS01
from lib.LIS2HH12 import LIS2HH12
from lib.SI7006A20 import SI7006A20
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from machine import Pin

def run():

	def sub_cb(topic, msg): 
		print(msg)

	chrono = Timer.Chrono()
	chrono.start()

	################################################################# Connection to Wifi #####################################################

	wlan = network.WLAN(mode=network.WLAN.STA)
	nets = wlan.scan()
	print (wlan.ifconfig())

	if wlan.isconnected() == False:
		for net in nets:
			print(net.ssid)
			if net.ssid == 'Xperia XA2_83f4':
				wlan.connect(net.ssid, auth=(net.sec, 'jujujacq0611'), timeout=5000)
				break


	while not wlan.isconnected():
		print(chrono.read())
		pass

	print ('wlan connection succeeded!')
	print (wlan.ifconfig())

	while wlan.isconnected():

############################################################ MQTT connection/Sending ##############################################

	
		client = MQTTClient(client_id="example_client", server="io.adafruit.com", user="Dragos123", password="0af871aaeb2f4341b43ccd92f745a8d0", port=1883) 
		client.set_callback(sub_cb) 
		client.connect()
		client.subscribe(topic="Dragos123/feeds/lights") 

		############################################################### LoRa Connection ###########################################

		# Please pick the region that matches where you are using the device:
		# Asia = LoRa.AS923
		# Australia = LoRa.AU915
		# Europe = LoRa.EU868
		# United States = LoRa.US915

		py = Pysense()
		lt = LTR329ALS01(py)

		chrono2 = Timer.Chrono()
		chrono2.start()

		lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
		s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
		s.setblocking(False)
		previous_light = 0

		while chrono2.read_ms()<5000:
			data = s.recv(64)
			if data != b'':
				data2 = str(data).strip("b'")
				print("Light : " + data2)
				client.publish(topic="Dragos123/feeds/lights", msg=data2)
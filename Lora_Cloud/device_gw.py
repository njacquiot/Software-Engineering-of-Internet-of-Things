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
from machine import RTC
import json


def run():




#	localtime = time.asctime( time.localtime(time.time()) )
#	print ("Local current time :" + localtime)

	#date = datetime.datetime.now()
	#str(date)

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


	with open('userInput.json') as json_file:  
		userData = json.load(json_file)
		print(userData)

	print ('wlan connection succeeded!')
	print (wlan.ifconfig())
	rtc = RTC()
	rtc.ntp_sync('dk.pool.ntp.org',20)
	time.sleep(1)
	if(rtc.synced()):
		datetime = rtc.now()
		t = str(datetime[3])+":"+str(datetime[4])
		print(t)

	while wlan.isconnected():

############################################################ MQTT connection/Sending ##############################################

	
		client = MQTTClient(client_id="example_client", server="io.adafruit.com", user="Dragos123", password="0af871aaeb2f4341b43ccd92f745a8d0", port=1883) 
		client.set_callback(sub_cb) 
		client.connect()
		client.subscribe(topic="Dragos123/feeds/lights") 
		client.subscribe(topic="Dragos123/feeds/temperature") 

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

		s.send(b''+userData["rateOfSampling"])

		while True:
			data = s.recv(64)
			datetime = rtc.now()
			now = str(datetime[3])+":"+str(datetime[4])
			#print(now)
			#now = "15:00"

			found = userData["data"][0]
			for i in range(len(userData["data"])):
				current = userData["data"][i]
				if (i==len(userData["data"])):
					found = current
					break
				else:
					nextOne = userData["data"][i+1]
					if (now<current["time"] or now>=userData["data"][len(userData["data"])-1]["time"]):
						found = userData["data"][len(userData["data"])-1]
						break
					
					if (current["time"] <= now and now < nextOne["time"]) :
						found = current
						break


			if data != b'':
				print(now)
				print(found)
				payload = str(data).strip("b'")
				array = payload.split("|")
				light = array[0]
				temperature = array[1]
				#humidity = array[2]
				#print("chrono : "+ str(chrono2.read_ms()))
				print("Light : " + light)
				print("Temperature : "+temperature)

				if(float(temperature)<float(found['temperature'])-float(userData["temperatureAcceptedOffset"])):
					client.publish(topic="Dragos123/feeds/termostate-status", msg="#00ffff")
				elif(float(temperature)>float(found['temperature'])+float(userData["temperatureAcceptedOffset"])):
					client.publish(topic="Dragos123/feeds/termostate-status", msg="#ff0000")
				else :
					client.publish(topic="Dragos123/feeds/termostate-status", msg="#00ff00")
				
				client.publish(topic="Dragos123/feeds/lights", msg=light)
				client.publish(topic="Dragos123/feeds/temperature", msg=temperature)
				data = b''
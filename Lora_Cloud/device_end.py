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
import math

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.sEU868
# United States = LoRa.US915




def run() :
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    previous_light = 0
    chrono = Timer.Chrono()
    chrono.start()
    time_step = 5


    py = Pysense()
    lt = LTR329ALS01(py) #Light

    adc = machine.ADC() 
    p_out = Pin('P19', mode= Pin.OUT)#, pull=Pin.PULL_UP) #mode out et HIGH
    p_out.value(1)
    p_in = Pin('P16', mode= Pin.IN)
    #apin = adc.channel(pin = p_out)
    apin = adc.channel(pin = p_in)

    si = SI7006A20(py)

    
    while True:
        ch0_value, ch1_value = lt.light()
        val = apin()
        millivolts = apin.voltage()
        degC = (millivolts-501.29)/8.2289 #10mV/°C + offset of 500mV

        #humidity = si.humidity() 

        payload = str(ch0_value) + "|" + str(degC) #+ "|" + str(humidity)

        time.sleep(5)
        s.send(b''+payload)
        print("send")

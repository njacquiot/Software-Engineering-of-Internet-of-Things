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
    print(lora.power_mode())
    #print(lora.tx_ower())
    print(lora.sf())
    
    chrono = Timer.Chrono()
    chrono.start()

    py = Pysense()
    lt = LTR329ALS01(py) #Light

    adc = machine.ADC() 
    p_out = Pin('P19', mode= Pin.OUT)#, pull=Pin.PULL_UP) #mode out et HIGH
    p_out.value(1)
    p_in = Pin('P16', mode= Pin.IN)
    #apin = adc.channel(pin = p_out)
    apin = adc.channel(pin = p_in)

    rateOfSampling = 30 # default value
    numberForAverage = 10
    lightValues = []
    millivoltValues = []
    
    while True:

        # recieving rateOfSampling from gateway when it arrives
        data = s.recv(64)
        if data != b'':
            payload = str(data).strip("b'")
            rateOfSampling = float(payload)
        
        ch0_value, ch1_value = lt.light()
        lightValues.append(ch0_value)

        val = apin()
        millivolts = apin.voltage()
        #print(millivolts)
        millivoltValues.append(millivolts)

        if (len(lightValues) == numberForAverage or len(millivoltValues) == numberForAverage):

            lightAverage = Average(lightValues)
            millivoltAverage = Average(millivoltValues)
            print(millivoltAverage)
            degC = convertMillivoltsToCelcius(millivoltAverage)
            #humidity = si.humidity()
            room = convertIdtoRoom(machine.unique_id()) 

            payload = str(lightAverage) + "|" + str(degC) +"|" + room #+ "|" + str(humidity)
            s.send(b''+payload)
            print("sending payload: ")
            print(payload)

            lightValues = []
            millivoltValues = []
            lightAverage = 0
            millivoltAverage = 0
            time.sleep(rateOfSampling)

    
def convertMillivoltsToCelcius(millivolts):
    degC = 0
    if (machine.unique_id() == b'\x80}:\xc2\xde\xe4'):
        # dark plastic
        degC = (millivolts-500.43)/8.7587
    elif (machine.unique_id() == b'0\xae\xa4NYx'):
        # light plastic
        degC = (millivolts-500.73)/8.2135
    return degC

def convertIdtoRoom(device_id):
    if (device_id == b'\x80}:\xc2\xde\xe4'):
        # dark plastic
        room = "room-1"
    elif (device_id == b'0\xae\xa4NYx'):
        # light plastic
        room = "room-2"
    return room

def Average(lst): 
    return sum(lst) / len(lst)
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

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

chrono = Timer.Chrono()
chrono.start()

def freeze(sec = 0):
    time.sleep(sec)

file = open('data.txt', 'a')


adc = machine.ADC() 
p_out = Pin('P19', mode= Pin.OUT)#, pull=Pin.PULL_UP) #mode out et HIGH
p_out.value(1)
p_in = Pin('P16', mode= Pin.IN)
#apin = adc.channel(pin = p_out)
apin = adc.channel(pin = p_in)

def convertMillivoltsToCelcius(millivolts):
    degC = 0
    if (machine.unique_id() == b'\x80}:\xc2\xde\xe4'): 
        # dark plastic
        degC = (millivolts-500.43)/8.7587
    elif (machine.unique_id() == b'0\xae\xa4NYx'):
        # light plastic
        degC = (millivolts-500.73)/8.2135
    return degC

def run():
    while True:
        #print("Temperature: " + str(si.temperature()*0.75))
        # #file.write(str(mp.temperature()*0.75))
        val = apin()
        millivolts = apin.voltage()
        degC = convertMillivoltsToCelcius(millivolts)
        
        print("V : " + str(millivolts))
        print("T : " + str(degC))
        #print(degF)
        #print(volt)
        freeze(1)

        #print("Altitude: " + str(mp.altitude()))
        #mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
        #print("Pressure: " + str(mpp.pressure()))

        #print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
        #print("Dew point: "+ str(si.dew_point()) + " deg C")
        #t_ambient = 24.4
        #print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

        #print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

        #print("Acceleration: " + str(li.acceleration()))
        #print("Roll: " + str(li.roll()))
        #print("Pitch: " + str(li.pitch()))

        #print("Battery voltage: " + str(py.read_battery_voltage()))
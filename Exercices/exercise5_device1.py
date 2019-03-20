import pycom
import time
import utime
from lib.pysense import Pysense
from lib.LTR329ALS01 import LTR329ALS01
from lib.LIS2HH12 import LIS2HH12
from lib.SI7006A20 import SI7006A20
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import logger

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
mpp = MPL3115A2(py,mode=PRESSURE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
# https://github.com/pycom/pycom-libraries/blob/master/pysense/main.py

led_on = True
LED_DEFAULT = 0xFFFFFF

pycom.heartbeat(False)

def freeze(sec = 0):
    time.sleep(sec)

file = open('log/data.txt', 'w+')

def shift_led():
    global led_on
    pycom.rgbled(LED_DEFAULT if led_on else ~LED_DEFAULT)
    logger.log_time(file)
    led_on = not(led_on)

def run():
    while True:
        shift_led()
        freeze(0.1)  # 10 Hz  

        # 100 Hz -> 0.01 sec
        # By having the light blinking at the rate of 100 Hz there was no visible 
        # change in the light, kind of like it was always on
        # We therefore tried lowering the rate to get some data
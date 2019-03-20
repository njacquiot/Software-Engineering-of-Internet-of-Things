import pycom
import time
import utime
from lib.pysense import Pysense
from lib.LTR329ALS01 import LTR329ALS01
from lib.LIS2HH12 import LIS2HH12
from lib.SI7006A20 import SI7006A20
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
#import logger

py = Pysense()
lt = LTR329ALS01(py)
# https://github.com/pycom/pycom-libraries/blob/master/pysense/main.py

pycom.heartbeat(False)
previous_light = 0

file = open('data.txt', 'a+')

def listen_light_sensor():
    global previous_light
    # http://www.mouser.com/ds/2/239/Lite-On_LTR-329ALS-01%20DS_ver1.1-348647.pdf
    # Channel 0 adapted for short wavelengths (400 - 800 nm) / Channel 1 adapted for higher wavelengths (500 - 1000 nm)
    ch0_value, ch1_value = lt.light()
    if ch0_value != previous_light :
        file.write(str(utime.ticks_ms()) + "\n")
        print(utime.ticks_ms())
    previous_light = ch0_value

def run():
    while True:
        listen_light_sensor()



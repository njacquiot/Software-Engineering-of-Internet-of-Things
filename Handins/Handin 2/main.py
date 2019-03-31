'''
Objective: Design an experiment to calibrate the thermistor attached to your board.
Hint: Use a (trusted) thermometer to collect ground truth.

Questions to answer:
1. Which parameterized function is suitable for converting the raw value to a
temperature?
2. What are the parameters for your setup?
3. If a single reading converted using that calibration reports a temperature of T,
what can you state about the actual temperature?



import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P4'))
temp = DS18X20(ow)

while True:
    print(temp.read_temp_async())
    time.sleep(1)
    temp.start_conversion()
    print(temp.start_conversion())
    time.sleep(1)


'''


# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import device

device.run()


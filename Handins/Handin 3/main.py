'''
Handin 3: Wireless Uplink
Precondition: You have a program which can sample a temperature and push it out
over a wireless link at some frequency
Tasks:
1. Update the program to additionally sample the light level
2. Update the program to keep track of the number of transmissions
3. Transmit temperature, light level and number of transmissions in a single frame
Run it for a week
Questions to answer:
1. At which frequency did you receive data?
2. How precise are the reception times?
3. Are there any missing frames, and if so are there patternss?

'''

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import device_send
import device_rcv

#device_send.run()
device_rcv.run()


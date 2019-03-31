'''
Handin 1: Full-Circle Latency
Setup: A laptop is attached to two IoT devices.
I One device is positioned so that its light sensor is pointing at the LED of the other
device
I The laptop generates a signal which one device uses to drive its LED
I The other device outputs the state of its light sensor on its serial line
I The laptop logs both serial lines
In this handin you need to answer:
I How would you expect the distribution of the latency through the whole system to
look like?
I What is the distribution of the latency through the whole system?
I Why the deviation?
Deadline: Wednesday, Mar 6, 2019 (may be extended due to lack of hardware)
Handin Procedure: Send as PDF to asjo@mmmi.sdu.dk with subject
"SDU IoT 2019f: Handin 1 - Full-Circle Latency"
'''

import pycom
import time
from lib.LTR329ALS01 import LTR329ALS01
import device1
import device2
#import Exercices.logger

# flashing device
# os.mkfs('/flash')

# We switch between the two devices
#device1.run()
device2.run()
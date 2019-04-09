import pycom
import time
from lib.LTR329ALS01 import LTR329ALS01
import Exercices.exercise5_device1
import Exercices.exercise5_device2
import Handins.Handin2.device
#import Exercices.logger

# flashing device
# os.mkfs('/flash')

# We switch between the two devices
#Exercices.exercise5_device1.run()
#Exercices.exercise5_device2.run()
Handins.Handin2.device.run()
import pycom
import time
#from datetime import datetime
from lib.LTR329ALS01 import LTR329ALS01


LED_DEFAULT = 0xFFFFFF
led_on = True
previous_light = 0


lux = LTR329ALS01()
pycom.heartbeat(False)


def freeze(sec = 0):
    time.sleep(sec)

# Turn the led on/off depending on its status
def shift_led():
    global led_on
    pycom.rgbled(LED_DEFAULT if led_on else ~LED_DEFAULT)
    led_on = not(led_on)

while True:
    shift_led()
    freeze(0.5)

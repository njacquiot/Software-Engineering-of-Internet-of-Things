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

def light_sensor():
    global previous_light
    # http://www.mouser.com/ds/2/239/Lite-On_LTR-329ALS-01%20DS_ver1.1-348647.pdf
    # Channel 0 adapted for short wavelengths (400 - 800 nm) / Channel 1 adapted for higher wavelengths (500 - 1000 nm)
    ch0_value, ch1_value = lux.light()
    if ch0_value != previous_light :
        print("\rLignt Sensor: " + str(ch0_value))
        print (time.gmtime())
        # print("\rLignt Sensor: " + str(ch0_value) + "  ", end = "")
    previous_light = ch0_value


while True:
    shift_led()

    if not(led_on):
        light_sensor()

    freeze(0.5)

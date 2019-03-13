import pycom
from lib.pysense import Pysense
from lib.LTR329ALS01 import LTR329ALS01
from lib.LIS2HH12 import LIS2HH12
from lib.SI7006A20 import SI7006A20
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE


py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
mpp = MPL3115A2(py,mode=PRESSURE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
# https://github.com/pycom/pycom-libraries/blob/master/pysense/main.py

# Definitely not a perfect implementation but is testing all of the sensors so ..

TURN_LED_ON = "Turn led on"
TURN_LED_OFF = "Turn led off"
TEST_TEMPERATURE = "Test temperature"
TEST_LIGHT_SENSOR = "Test light sensor"
TEST_HUMIDITY = "Test humidity sensor"
TEST_ALTIDUDE = "Test altitude sensor"
TEST_PRESSURE = "Test pressure sensor"
TEST_ACCELERATION = "Test acceleration"
TEST_ROLL = "Test roll"
TEST_PITCH = "Test pitch"

ALLOWED_COMMANDS = [TURN_LED_ON, TURN_LED_OFF, TEST_TEMPERATURE, TEST_LIGHT_SENSOR, TEST_HUMIDITY, TEST_ALTIDUDE, TEST_PRESSURE, TEST_ACCELERATION, TEST_ROLL, TEST_PITCH]

LED_DEFAULT = 0xFFFFFF

def led_on():
    pycom.rgbled(LED_DEFAULT)

def led_off():
    pycom.rgbled(~LED_DEFAULT)

def get_temp():
    # https://docs.pycom.io/pytrackpysense/apireference/pysense.html
    return str(si.temperature()) + " deg C"

def get_light():
    return lt.light()[0]

def get_humidity():
    return str(si.humidity()) + " %RH"

def get_altidude():
    return str(mp.altitude()) + " m"

def get_pressure():
    return str(mpp.pressure()) + " Pa"

def get_acceleration(): 
    return li.acceleration()

def get_roll():
    return li.roll()

def get_pitch():
    return li.pitch()


while True:
    command = input("What would you like the board to do? ")

    if (command == TURN_LED_ON):
        led_on()
    elif (command == TURN_LED_OFF): 
        led_off()
    elif (command == TEST_TEMPERATURE):
        print(get_temp())
    elif (command == TEST_LIGHT_SENSOR):
        print(get_light())
    elif(command == TEST_HUMIDITY):
        print(get_humidity())
    elif(command == TEST_ALTIDUDE):
        print(get_altidude())
    elif(command == TEST_PRESSURE):
        print(get_pressure())
    elif(command == TEST_ACCELERATION):
        print(get_acceleration())
    elif(command == TEST_ROLL):
        print(get_roll())
    elif(command == TEST_PITCH):
        print(get_pitch())
    else:
        print("You need to write one of the following commands: ")
        for c in ALLOWED_COMMANDS:
            print(" -> \"" + c + "\"")

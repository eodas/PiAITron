"""
Executive Order Corporation - Raspberry Pi Tron MQTT Telemetry Transport Machine-to-Machine(M2M)/Internet of Things(IoT)
Raspberry Pi Tron Drools-jBPM :: Executive Order Raspberry Pi Tron Sensor AI-IoTBPM Client using AI-IoTBPM Drools-jBPM
Raspberry Pi Tron AI-IoTBPM :: Internet of Things Drools-jBPM Expert System using Raspberry Pi Tron AI-IoTBPM Processing
Executive Order Corporation
Copyright (c) 1978, 2021: Executive Order Corporation, All Rights Reserved
"""

import json
import threading
import time

# importing the requests library
import requests

try:
    import RPi.GPIO as GPIO
    """This is trapped so you can still run without RPi.GPIO

    GPIO will be checked before use
    """
    pi_interface = True
except:
    pi_interface = False
    pass

# Update these with Raspberry Pi Tron service IP address and unique unit id values
URL = "http://10.0.0.2:5055/"  # Set EOSpy server IP address
id = "100111"  # Raspberry Pi Tron Device unique unit id

# Above are all the fields you need to provide values, the remaining fields are used in the RPi Tron application
setup = True  # Init setup GPIO.setmode() once

#     Raspberry Pi Pinout
#      3V3  (1)  (2) 5V
#    GPIO2  (3)  (4) 5V
#    GPIO3  (5)  (6) GND
#    GPIO4  (7)  (8) GPIO14
#      GND  (9) (10) GPIO15
#   GPIO17 (11) (12) GPIO18
#   GPIO27 (13) (14) GND
#   GPIO22 (15) (16) GPIO23
#      3V3 (17) (18) GPIO24
#   GPIO10 (19) (20) GND
#    GPIO9 (21) (22) GPIO25
#   GPIO11 (23) (24) GPIO8
#      GND (25) (26) GPIO7
#    GPIO0 (27) (28) GPIO1
#    GPIO5 (29) (30) GND
#    GPIO6 (31) (32) GPIO12
#   GPIO13 (33) (34) GND
#   GPIO19 (35) (36) GPIO16
#   GPIO26 (37) (38) GPIO20
#      GND (39) (40) GPIO21

# BerryClip+ - 6 LED - 2 Switch - 1 Buzzer Board
# Hardware Reference
# =============================
# The components are connected to the main Pi GPIO header (P1)
# LED 1    - P1-07 - GPIO4
# LED 2    - P1-11 - GPIO17
# LED 3    - P1-15 - GPIO22
# LED 4    - P1-19 - GPIO10
# LED 5    - P1-21 - GPIO9
# LED 6    - P1-23 - GPIO11
# Buzzer   - P1-24 - GPIO8
# Switch 1 - P1-26 - GPIO7
# Swtich 2 - P1-22 - GPIO25

# Jam HAT - 6 LED - 2 Switch - 1 Buzzer Board
# The table below shows the pin numbers for BCM, Board and the matching GPIO Zero objects.
# |Component |GPIO.BCM | BOARD  |GPIO Zero object | Notes |
# |----------|---------|--------|-----------------|-------|
# | LED1     | GPIO 5  | Pin 29 | lights_1.red    |   |
# | LED2     | GPIO 6  | Pin 31 | lights_2.red    |   |
# | LED3     | GPIO 12 | Pin 32 | lights_1.yellow |   |
# | LED4     | GPIO 13 | Pin 33 | lights_2.yellow |   |
# | LED5     | GPIO 16 | Pin 36 | lights_1.green  |   |
# | LED6     | GPIO 17 | Pin 11 | lights_2.green  |   |
# | Button 1 | GPIO 19 | Pin 35 | button_1        | Connected to R8/R10 |
# | Button 2 | GPIO 18 | Pin 12 | button_2        | Connected to R7/R9 |
# | Buzzer   | GPIO 20 | Pin 38 | buzzer          |   |

LedPin0 = 5  # GPIO pin GPIO05 (LED pin29)

SwitchPin0 = 19  # GPIO pin GPIO19 (Switch pin12)
SwitchPin1 = 18  # GPIO pin GPIO18 (Switch pin38)


# def do_SETUP():
# void setup(void) 
GPIO.setmode(GPIO.BCM) # Tell GPIO library to use GPIO references
GPIO.setup(LedPin0, GPIO.OUT)  # Set pin mode as output
GPIO.output(LedPin0, GPIO.LOW)  # Set pin to high(+3.3V) to off the led
GPIO.setup(SwitchPin0, GPIO.IN)  # Set pin mode as input
GPIO.setup(SwitchPin1, GPIO.IN)  # Set pin mode as input
print("Setup GPIO pins as inputs and outputs")


# $GPGGA GPS Log header
utc = "0"  # UTC time status of position (hours/minutes/seconds/decimal seconds)
# Update these with your LAT/LON GPS position values
# You can find LAT/LON from an address https://www.latlong.net/convert-address-to-lat-long.html
address = "National_Air_Space_Museum_600_Independence_Ave_Washington_DC_20560"
latstr = "38.888160"  # lat Latitude
lngstr = "-77.019868"  # lng Longitude
speed = "0"  # speed Km - Speed over ground, knots
course = "0.00"  # track true - Track made good, degrees True as bearing
altitude = "0"  # altitude Antenna altitude above/below mean sea level
message = "0"  # total number of messages in this transmission
accuracy = "0.0"  # GPS device accuracy
valid = "V"  # data status - Data status: A = Data valid, V = Data invalid
batt = "89.7"  # GPS device batteryLevel
light = "53.4"  # photocell value

# Raspberry Pi Tron currently supports these additional data fields in the Server Event data model:

# id=6&event=allEvents&protocol=osmand&servertime=<date>&timestamp=<date>&fixtime=<date>&outdated=false&valid=true
# &lat=38.85&lon=-84.35&altitude=27.0&speed=0.0&course=0.0&address=<street address>&accuracy=0.0&network=null
# &batteryLevel=78.3&textMessage=Message_Sent&temp=71.2&ir_temp=0.0&humidity=0.0&mbar=79.9
# &accel_x=-0.01&accel_y=-0.07&accel_z=9.79&gyro_x=0.0&gyro_y=-0.0&gyro_z=-0.0&magnet_x=-0.01&magnet_y=-0.07&magnet_z=9.81
# &light=91.0&keypress=0.0&alarm=Temperature&distance=1.6&totalDistance=3.79&motion=false

# You can add more additional fields to the data model and transmit via any device to the Raspberry Pi Tron Drools-jBPM processing

# Values for the DHT11 digital temperature/humidity sensor; &temp= and &humidity= fields
temp = "0.0"
humidity = "0.0"

# Values to send in &keypress= field
keypress = "1.0"

# Values to send in &textMessage= filed
textMessage = "text_message"

# Values to send in &keypress= field
TYPE_ALLEVENTS = "allEvents"  # allEvents
TYPE_KEYPRESS_1 = "1.0"  # keypress_1
TYPE_KEYPRESS_2 = "2.0"  # keypress_2
TYPE_REED_RELAY = "4.0"  # reedRelay
TYPE_PROXIMITY = "8.0"  # proximity

# Values to send in &alarm= field
alarm = "none"

# Values to send in &alarm= field
ALARM_GENERAL = "general"
ALARM_SOS = "sos"
ALARM_VIBRATION = "vibration"
ALARM_MOVEMENT = "movement"
ALARM_LOW_SPEED = "lowspeed"
ALARM_OVERSPEED = "overspeed"
ALARM_FALL_DOWN = "fallDown"
ALARM_LOW_POWER = "lowPower"
ALARM_LOW_BATTERY = "lowBattery"
ALARM_FAULT = "fault"
ALARM_POWER_OFF = "powerOff"
ALARM_POWER_ON = "powerOn"
ALARM_DOOR = "door"
ALARM_GEOFENCE = "geofence"
ALARM_GEOFENCE_ENTER = "geofenceEnter"
ALARM_GEOFENCE_EXIT = "geofenceExit"
ALARM_GPS_ANTENNA_CUT = "gpsAntennaCut"
ALARM_ACCIDENT = "accident"
ALARM_TOW = "tow"
ALARM_ACCELERATION = "hardAcceleration"
ALARM_BRAKING = "hardBraking"
ALARM_CORNERING = "hardCornering"
ALARM_FATIGUE_DRIVING = "fatigueDriving"
ALARM_POWER_CUT = "powerCut"
ALARM_POWER_RESTORED = "powerRestored"
ALARM_JAMMING = "jamming"
ALARM_TEMPERATURE = "temperature"
ALARM_PARKING = "parking"
ALARM_SHOCK = "shock"
ALARM_BONNET = "bonnet"
ALARM_FOOT_BRAKE = "footBrake"
ALARM_OIL_LEAK = "oilLeak"
ALARM_TAMPERING = "tampering"
ALARM_REMOVING = "removing"


blink_active = False
"""bool: to controll weather blink continues to be active

This will not start the blinking it will only be important once blinking
has started.  This is currently only used in testing.
"""

GPIO_STATE = {}
""" This is an object of tracking GPIO"""

GPIO_ON = {}
""" This maps functions to gpio activit

These functions will be called when the GPIO is changed in any way.
"""


is_imported = True
"""Used as a flag to show that GPIO was imported"""

def serverSendPost(keypress_parm, textMessage_parm, alarm_parm):
    global utc
    # utc = int(string)
    utc = int(time.time())

    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'id': id,
              'timestamp': utc,
              'keypress': keypress_parm,
              'textMessage': textMessage_parm,
              'alarm': alarm_parm}

    # Raspberry Pi Tron currently supports these additional data fields in the Server Event data model:
    # 'lat': latstr,
    # 'lon': lngstr,
    # 'speed': speed,
    # 'bearing': bearing,
    # 'altitude': altitude,
    # 'accuracy': accuracy,
    # 'valid': bvalid,
    # 'batt': batt,
    # 'temp': temp,
    # 'humidity': humidity,
    # 'keypress': TYPE_KEYPRESS_1
    # 'textMessage: textMessage,
    # 'alarm': ALARM_TEMPERATURE,
    # 'light': light,

    # sending get request and saving the response as response object 
    resp = requests.get(url=URL, params=PARAMS)

    print(">>> Connection Status:", resp.status_code)
    return

def ButtonHandeler(channel):
    """This handels the button press and sets the state

    Args:
        channel(int):  The RPi GPIO channel used for monitoring the button
    """
    if GPIO.input(channel) == GPIO.HIGH:
        set("Button","Pressed")
    else:
        set("Button","Released")

"""This is the setup for the RPi GPIO"""
if pi_interface:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(18,GPIO.IN)
    GPIO.add_event_detect(18,GPIO.BOTH,ButtonHandeler)

def set(key,value):
    """This is used to set values for GPIO

    This function is used to set values for each of GPIO's Will also call
    the GPIO's function if it exisits.

    Args:
        key(int or str): Used to identify the gpio to interface
        value(int or str): The value to set the gpio to.
    """
    GPIO_STATE[key] = value
    if (key=="GPIO1") and pi_interface:
        if value.upper()=="ON":
            GPIO.output(5,GPIO.HIGH)
            keypress = "1.0"
            textMessage = "Device_is_On";
            alarm = ALARM_TEMPERATURE
            serverSendPost(keypress, textMessage, alarm)
        else:
            GPIO.output(5,GPIO.LOW)
            keypress = "2.0"
            textMessage = "Device_is_Off";
            alarm = ALARM_MOVEMENT
            serverSendPost(keypress, textMessage, alarm)
    if key in GPIO_ON:
        GPIO_ON[key]()

def get(key):
    """ Returns the value of the givien GPIO

    Args:
        key(int or str): Used to identify the gpio to interface
    """
    return GPIO_STATE[key]

def on(key,function):
    """Used to set the function for the GPIO interface

    Args:
        key(int or str): Used to identify the gpio to interface
        function(function): The function for the gpio
    """
    GPIO_ON[key]= function

def json():
    """Returns a json object of the GPIO info"""
    return json.dumps(GPIO_STATE)


if __name__=="__main__":
    """This is console testing of the GPIO.  Not ment for automated testing

    This should show that everything is working to the developer and allow
    for changes going forward
    """
    def printgpio():
        print(GPIO_STATE)

    def blink_led():
        if blink_active:
            threading.Timer(0.5, blink_led).start()
        if get("GPIO1")!="On":
            set("GPIO1","On")
        else:
            set("GPIO1","Off")

    on("GPIO1",printgpio)

    set("GPIO1","On")
    blink_active = True
    blink_led()
    time.sleep(10)
    blink_active = False
    if pi_interface:
        print("GPIO is valid")


#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from gpiozero import Button

from Adafruit_IO import MQTTClient

import serial
import time
import json

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6

<<<<<<< HEAD
ADAFRUIT_IO_KEY = 'aio_WMPt83AJCkeOoSZzoMtG4fdhHWh2'
=======
ADAFRUIT_IO_KEY = 'aio_IYbl715s7zcS2eOnWTftgc0UohMp'
>>>>>>> 8ddc4711d09ee0ef45cd36681c5b64465c646545
ADAFRUIT_IO_USERNAME = 'Nakshath'
ADAFRUIT_FEED = 'gpstracker/json'

#Important User-Defined function to make talking to the HAT easier
def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')
	
def send_command(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 'ERR'
        else:
            print(command + ' Response:\t' + str(rec_buff.decode()))
            return str(rec_buff.decode())
    else:
        return 'ERR'

def get_gps_location(location):
<<<<<<< HEAD
    json_data = {
        'key': 'gpstracker',
        'value': 1,
        'lat': 0,
        'lon': 0,
        'ele': 112,
    }
    if len(location) > 50:
        GPSDATA = location
        Cleaned = GPSDATA[25:]
        #print(Cleaned)
        Lat = Cleaned[:2]
        SmallLat = Cleaned[2:11]
        NorthOrSouth = Cleaned[12]
        #print(Lat, SmallLat, NorthOrSouth)
        Long = Cleaned[14:17]
        SmallLong = Cleaned[17:26]
        EastOrWest = Cleaned[27]
        #print(Long, SmallLong, EastOrWest)
        FinalLat = float(Lat) + (float(SmallLat)/60)
        FinalLong = float(Long) + (float(SmallLong)/60)

        if NorthOrSouth == 'S': FinalLat = -FinalLat
        if EastOrWest == 'W': FinalLong = -FinalLong

        FinalLongText = round(FinalLong, 6)
        FinalLatText = round(FinalLat, 6)

        StringFinalLongText = str(FinalLongText)
        StringFinalLatText = str(FinalLatText)

        #print(FinalLat, FinalLong)
        #print(FinalLat, FinalLong)
        #print(rec_buff.decode())
        json_data.lat = FinalLatText,
        json_data.lon = FinalLongText,
    else:
        print ('No Gps Data: ' + location)
=======
    global GPSDATA
    GPSDATA = location
    Cleaned = GPSDATA[25:]
    #print(Cleaned)
    Lat = Cleaned[:2]
    SmallLat = Cleaned[2:11]
    NorthOrSouth = Cleaned[12]
    #print(Lat, SmallLat, NorthOrSouth)
    Long = Cleaned[14:17]
    SmallLong = Cleaned[17:26]
    EastOrWest = Cleaned[27]
    #print(Long, SmallLong, EastOrWest)
    FinalLat = float(Lat) + (float(SmallLat)/60)
    FinalLong = float(Long) + (float(SmallLong)/60)

    if NorthOrSouth == 'S': FinalLat = -FinalLat
    if EastOrWest == 'W': FinalLong = -FinalLong

    FinalLongText = round(FinalLong, 6)
    FinalLatText = round(FinalLat, 6)

    StringFinalLongText = str(FinalLongText)
    StringFinalLatText = str(FinalLatText)

    #print(FinalLat, FinalLong)
    #print(FinalLat, FinalLong)
    #print(rec_buff.decode())
    json_data = {
        'key': 'gpstracker',
        'value': 1,
        'lat': FinalLatText,
        'lon': FinalLongText,
        'ele': 112,
    }
>>>>>>> 8ddc4711d09ee0ef45cd36681c5b64465c646545
    return json.dumps(json_data)

def mqtt_connect(client):
    print('Connected to Adafruit IO!')

def mqtt_disconnect(client):
    print('Disconnected from Adafruit IO!')
    
def publish_gps_data(client, gps_data):
    print('Publishing {0} to {1}.'.format(gps_data, ADAFRUIT_FEED))
    client.publish(ADAFRUIT_FEED, gps_data)
    
# main body of the code using the above functions

power_on(power_key)
print('Start GPS session...')
send_command('AT+CGPS=1,1','OK',1)
time.sleep(2)

# create an MQTT client instance
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = mqtt_connect
client.on_disconnect = mqtt_disconnect

button = Button(22)
<<<<<<< HEAD
print('Wating for button press ...')
=======
>>>>>>> 8ddc4711d09ee0ef45cd36681c5b64465c646545
button.wait_for_press()
print("The button was pressed!")

# connect to the Adafruit IO server
client.connect()

print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    print('Get GPS location...')
    response = send_command('AT+CGPSINFO','+CGPSINFO: ',1)
    if 'ERR' != response:
        gps_location = get_gps_location(response)
        publish_gps_data(client, gps_location)
    else:
        print('GPS is not ready')
    time.sleep(10)


print('Stop GPS Session....')
send_command('AT+CGPS=0','OK',1)
power_down(power_key) 

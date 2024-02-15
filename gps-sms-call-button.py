#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from gpiozero import Button

import serial
import time

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 6
phone_number = '6284687669'


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
    return StringFinalLatText +',' + StringFinalLongText

def create_sms_message(location):
    global text_message
    text_message = ('I am at this location https://maps.google.com/?q=' + location)
    print(text_message)
    return text_message

def send_sms_message(phone_number, message):
    print("Setting SMS mode...")
    response = send_command("AT+CMGF=1","OK",1)
    print("Sending Short Message")
    response = send_command("AT+CMGS=\""+phone_number+"\"",">",2)
    #power_down(power_key)
    if response != 'ERR':
        ser.write(text_message.encode())
        ser.write(b'\x1A')
        response = send_command('','OK',20)
        if 'ERR' != response:
            print('sent successfully')
        else:
            print('error')
    else:
        print('error%d'%response)
        #power_down(power_key)

def call_phone():
    send_command('ATD'+phone_number+';','OK',1)
    time.sleep(100)

# main body of the code using the above functions

power_on(power_key)
print('Start GPS session...')
send_command('AT+CGPS=1,1','OK',1)
time.sleep(2)

button = Button(22)
button.wait_for_press()
print("The button was pressed!")

print('Get GPS location...')
response = send_command('AT+CGPSINFO','+CGPSINFO: ',1)
if 'ERR' != response:
    gps_location = get_gps_location(response)
    message = create_sms_message(gps_location)
    send_sms_message(phone_number, message)
    call_phone()
else:
    print('GPS is not ready')

print('Stop GPS Session....')
send_command('AT+CGPS=0','OK',1)
power_down(power_key) 

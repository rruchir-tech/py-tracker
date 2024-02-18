#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from gpiozero import Button

import serial
import time

power_key = 6
phone_number = '6284687669'

class GpsSMSCall:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0',115200)
        self.ser.flushInput()

#Important User-Defined function to make talking to the HAT easier
    def power_on(self, power_key):
        print('SIM7600X is starting:')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(power_key,GPIO.OUT)
        time.sleep(0.1)
        GPIO.output(power_key,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(power_key,GPIO.LOW)
        time.sleep(20)
        self.ser.flushInput()
        print('SIM7600X is ready')

    def power_down(self,power_key):
        print('SIM7600X is loging off:')
        GPIO.output(power_key,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(power_key,GPIO.LOW)
        time.sleep(18)
        print('Good bye')

    def send_command(self,command,back,timeout):
        rec_buff = ''
        self.ser.write((command+'\r\n').encode())
        time.sleep(timeout)
        if self.ser.inWaiting():
            time.sleep(0.01 )
            rec_buff = self.ser.read(self.ser.inWaiting())
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

    def get_gps_location(self,location):
        data = {}
        if len(location) > 50:
            GPSDATA = location
            Cleaned = GPSDATA[25:]

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

            data.long = round(FinalLong, 6)
            data.lat = round(FinalLat, 6)
        else:
            print('No GPS Data:' + location)
        return data


    def create_sms_message(self, location):
        text_message = ('I am at this location https://maps.google.com/?q=' + location)
        print(text_message)
        return text_message

    def send_sms_message(self, phone_number, message):
        print("Setting SMS mode...")
        response = self.send_command("AT+CMGF=1","OK",1)
        print("Sending Short Message")
        response = self.send_command("AT+CMGS=\""+phone_number+"\"",">",2)
        #power_down(power_key)
        if response != 'ERR':
            self.ser.write(message.encode())
            self.ser.write(b'\x1A')
            response = self.send_command('','OK',20)
            if 'ERR' != response:
                print('sent successfully')
            else:
                print('error')
        else:
            print('error%d'%response)
            #power_down(power_key)

    def call_phone(self):
        print('Calling mobile ...' + phone_number)
        self.send_command('ATD'+phone_number+';','OK',1)
        time.sleep(20)
        self.send_command('AT+CHUP','OK',1)
        print('phone call completed')

# main body of the code using the above functions
    def setup(self):
        self.power_on(power_key)
        print('Start GPS session...')
        self.send_command('AT+CGPS=1,1','OK',1)
        time.sleep(2)

#button = Button(22)
#button.wait_for_press()
#print("The button was pressed!")

    def gps_sms_call(self):
        print('Get GPS location...')
        response = self.send_command('AT+CGPSINFO','+CGPSINFO: ',1)
        if 'ERR' != response:
            data = self.get_gps_location(response)
            if 'lat' in data.keys() and 'long' in data.keys(): 
                message = self.create_sms_message(str(data.lat) + ',' + str(data.long))
                self.send_sms_message(phone_number, message)
            self.call_phone()
        else:
            print('GPS is not ready')

    def shutdown(self):
        print('Stop GPS Session....')
        self.send_command('AT+CGPS=0','OK',1)
        self.power_down(power_key) 

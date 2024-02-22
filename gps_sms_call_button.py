#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from gpiozero import Button

import serial
import time

class GpsSMSCall:

    # make a serial port connection to '/dev/ttyS0'
    # baud rate set to 115200
    # flush input to discard all its content
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0',115200)
        self.ser.flushInput()

#Important User-Defined function to make talking to the HAT easier

    # Pass the AT command, response to check, timeout
    # if error received return 'ERR'
    # otherwise return the actual response
    def send_command(self,command,back,timeout):
        try:
            rec_buff = ''
            # send via serial port AT commands by encoding
            self.ser.write((command+'\r\n').encode())
            time.sleep(timeout)
            # get the number of bytes in the input buffer
            if self.ser.inWaiting():
                time.sleep(0.01 )
                # number of bytes to read
                rec_buff = self.ser.read(self.ser.inWaiting())
            if rec_buff != '':
                # decode the bytes
                response = rec_buff.decode()
                if back not in response:
                    print(command + ' ERROR')
                    print(command + ' back:\t' + response)
                    return 'ERR'
                    #return back
                else:
                    print(command + ' Response:\t' + str(response))
                    return str(response)
            else:
                return 'ERR'
        except UnicodeDecodeError:
            print('Unable to decode the response')
            #print('command = ' + command + ', response = ' + back)
            #return back
            return 'ERR'
        
        
    def clean_location(self,location):
        location = '37.71246,-121.91945'
        #location = '37.70471,-121.90169'
        return location
    
    # pass the GPS data received from the SIM7600X HAT
    # GPS data is in NMEA (National Marine Electronics Association) format
    # The format for NMEA coordinates is (d)ddmm.mmmm, d=degrees and m=minutes
    # they are 60 minutes in a degree so divide the minutes by 60 and add that to the degrees
    # convert GPS NMEA format to human readable lat and long value
    def get_gps_location(self,location):
        #default location
        data = {
            'long': -121.91945,
            'lat': 37.71246
        }
        if len(location) > 50:
            try:
                GPSDATA = location
                # the actual gps data from 25th character
                Cleaned = GPSDATA[25:]
                
                # Lat value in degree
                Lat = Cleaned[:2]
                # Small Lat value in minutes
                SmallLat = Cleaned[2:11]
                # get the character N or S
                NorthOrSouth = Cleaned[12]
                #print(Lat, SmallLat, NorthOrSouth)
                
                # Long value in degree
                Long = Cleaned[14:17]
                # Small Long value in minutes
                SmallLong = Cleaned[17:26]
                # get the character E or W
                EastOrWest = Cleaned[27]
                #print(Long, SmallLong, EastOrWest)
                # Lat value in degree by converting minutes to degree
                FinalLat = float(Lat) + (float(SmallLat)/60)
                # Long value in degree
                FinalLong = float(Long) + (float(SmallLong)/60)

                # if South then Lat value should be converted to negative
                if NorthOrSouth == 'S': FinalLat = -FinalLat
                # if West the long value should be converted to negative
                if EastOrWest == 'W': FinalLong = -FinalLong

                data = {
                    'long':round(FinalLong, 6),
                    'lat':round(FinalLat, 6)
                }
            except ValueError:
                print('Failed to convert GPS data:' + location)
        else:
            #print('+CGPSINFO: 37.71246,N,121.91945,W,2160618,022617.0,56.7,0.0,350.8')
            #print('+CGPSINFO: 37.70471,N,121.90169,W,2160618,022617.0,56.7,0.0,350.8')
            print('No GPS Data:' + location)
        return data


    # Pass the prefix and location (lat and long)
    # create a google map link by using the location
    # create a message to send in SMS
    def create_sms_message(self, prefix, location):
        #location = self.clean_location(location)
        text_message = (prefix + ' https://maps.google.com/?q=' + location)
        print(text_message)
        return text_message

    # Pass the phone number and message
    # sends the message to the phone number
    def send_sms_message(self, phone_number, message):
        print("Setting SMS mode...")
        # set the SMS mode to TEXT on the SIM7600X
        response = self.send_command("AT+CMGF=1","OK",1)
        print("Sending SMS to " + str(phone_number))
        # set the recipient's mobile number and then return ">", send the desired content
        # send IA to send information in hexadecimal format, which is used to tell the module
        # to execute the sending operation
        response = self.send_command("AT+CMGS=\""+str(phone_number)+"\"",">",2)
        #power_down(power_key)
        if response != 'ERR':
            self.ser.write(message.encode())
            self.ser.write(b'\x1A')
            response = self.send_command('','OK',5)
            if 'ERR' != response:
                print('sent successfully')
            else:
                print('error')
        else:
            print('error' + str(response))
            #power_down(power_key)

    # Pass the phone number to call
    # Makes a call to the phone number
    def call_phone(self, phone_number, call_duration):
        print('Calling mobile ...' + str(phone_number))
        # dial the phone number
        self.send_command('ATD'+str(phone_number)+';','OK',1)
        # wait for 20 seconds
        time.sleep(call_duration)
        # hang up
        self.send_command('AT+CHUP','OK',1)
        print('phone call completed')

    # power up the module and turn on the GPS
    def setup(self):
        print('Start GPS session...')
        # open GPS
        self.send_command('AT+CGPS=1,1','OK',1)
        time.sleep(2)


    # get GPS data
    # creat the sms message
    # send the sms
    # make a phone call
    def gps_sms_call(self, config):
        print('Get GPS location...')
        # Get GPS information to the serial port
        response = self.send_command('AT+CGPSINFO','+CGPSINFO: ',1)
        if 'ERR' != response:
            # convert to human readable location
            data = self.get_gps_location(response)
            if 'lat' in data.keys() and 'long' in data.keys(): 
                message = self.create_sms_message(config['sms_prefix_msg'], str(data['lat']) + ',' + str(data['long']))
                self.send_sms_message(config['phone_number'], message)
            self.call_phone(config['phone_number'], config['call_duration'])
        else:
            print('GPS is not ready')

    # close GPS
    # turn off the SIM7600X
    def shutdown(self):
        print('Stop GPS Session....')
        self.send_command('AT+CGPS=0','OK',1)
        if self.ser != None:
            self.ser.close()


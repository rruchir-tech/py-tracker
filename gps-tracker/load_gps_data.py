#!/usr/bin/python
# -*- coding:utf-8 -*-

from Adafruit_IO import MQTTClient

import serial
import time
import json
from datetime import datetime, timedelta


ADAFRUIT_IO_KEY = 'aio_YRQK42arsADAlygAnVQEL3OK4vow'
ADAFRUIT_IO_USERNAME = 'Nakshath'
ADAFRUIT_FEED = 'gpstest2/json'

data = [
    { 'lat':37.702251, 'long':-121.908574},
{ 'lat':37.702022, 'long':-121.910841},
{ 'lat':37.702060, 'long':-121.912721},
{ 'lat':37.702060, 'long':-121.914578},
{ 'lat':37.702072, 'long':-121.916857},
{ 'lat':37.701633, 'long':-121.920273},
{ 'lat':37.701875, 'long':-121.920441},
{ 'lat':37.703789, 'long':-121.923681},
{ 'lat':37.705557, 'long':-121.925176},
{ 'lat':37.706988, 'long':-121.926405},
]

mt_data = [
{ 'lat':37.704357, 'long':-121.982537},
{ 'lat':37.704213, 'long':-121.982111},
{ 'lat':37.703940, 'long':-121.981996},
{ 'lat':37.703726, 'long':-121.982037},
{ 'lat':37.703512, 'long':-121.982145},
{ 'lat':37.703282, 'long':-121.982267},
{ 'lat':37.703084, 'long':-121.982436},
{ 'lat':37.702876, 'long':-121.982652},
{ 'lat':37.702710, 'long':-121.982888},
{ 'lat':37.702507, 'long':-121.983132},
{ 'lat':37.702277, 'long':-121.983064},
{ 'lat':37.702106, 'long':-121.982800},
{ 'lat':37.701956, 'long':-121.982625},
{ 'lat':37.701812, 'long':-121.982341},
{ 'lat':37.701683, 'long':-121.982003},
{ 'lat':37.701576, 'long':-121.981652},
{ 'lat':37.701523, 'long':-121.981293},
{ 'lat':37.701582, 'long':-121.980976},
{ 'lat':37.701673, 'long':-121.980705},
{ 'lat':37.701833, 'long':-121.980415},
{ 'lat':37.702004, 'long':-121.980219},
{ 'lat':37.702159, 'long':-121.979989},
{ 'lat':37.702357, 'long':-121.979942},
{ 'lat':37.702608, 'long':-121.979948},
{ 'lat':37.702817, 'long':-121.979854},
{ 'lat':37.703031, 'long':-121.979752},
{ 'lat':37.703287, 'long':-121.979604},
{ 'lat':37.703469, 'long':-121.979509},
]

def get_gps_location(lat, long):
    json_data = {
        'key': 'gpstest2',
        'value': 1,
        'lat': lat,
        'lon':  long,
        'ele': 112,
        'created_at': str(datetime.now() + timedelta(days=-9, hours=-5))
    }
    return json.dumps(json_data)

def mqtt_connect(client):
    print('Connected to Adafruit IO!')

def mqtt_disconnect(client):
    print('Disconnected from Adafruit IO!')
    
def publish_gps_data(client, gps_data):
    print('Publishing {0} to {1}.'.format(gps_data, ADAFRUIT_FEED))
    client.publish(ADAFRUIT_FEED, gps_data)
    
# create an MQTT client instance
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = mqtt_connect
client.on_disconnect = mqtt_disconnect

# connect to the Adafruit IO server
client.connect()

for x in mt_data:
    gps_location = get_gps_location(x['lat'], x['long'])
    publish_gps_data(client, gps_location)
    time.sleep(10)


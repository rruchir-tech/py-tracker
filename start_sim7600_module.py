#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

power_key = 6


class Sim7600Module:


    # start SIM7600X HAT
    # GPIO: General Purpose Input Output
    # setting the numbering system to BCM
    # disable the warnings
    # setup power key as output channel
    # set the output state of power key to High and LOW
    def power_on(self):
        print('SIM7600X is starting:')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(power_key,GPIO.OUT)
        time.sleep(0.1)
        GPIO.output(power_key,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(power_key,GPIO.LOW)
        time.sleep(20)
        print('SIM7600X is ready')

    # set output state of power key to High and LOW
    def power_down(self):
        print('SIM7600X is loging off:')
        GPIO.output(power_key,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(power_key,GPIO.LOW)
        time.sleep(18)
        GPIO.cleanup()
        print('Good bye')

sim = Sim7600Module()
sim.power_on()


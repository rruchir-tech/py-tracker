#!/usr/bin/python3

from gpiozero import Button
import time
from datetime import datetime

from gps_sms_call_button import GpsSMSCall

config = {
    'phone_number': 6284687669,
    'sms_prefix_msg': 'I am at this location',
    'call_duration': 20
}

# Button Push Class which is using GPIO pin 22 to detect the button press
class ButtonPush:
    def __init__(self):
        self.button = Button(22)
    
    # create the object of GpsSMSCall class
    # Start the SIM7600X module
    def setup(self):
        self.gpsSmsCall = GpsSMSCall()
        self.gpsSmsCall.setup()
    
    # Turn off the SIM7600X module
    def close(self):
        self.gpsSmsCall.shutdown()

    # While loop which waits for button press and invokes to
    # send the GPS location and make phone call to the configured
    # phone number
    def buttonPush(self):
        try:
            while(True):
                print('Waiting for button press...')
                self.button.wait_for_press()
                print('[%s] button pressed' % (str(datetime.now())))
                 #try:
                self.gpsSmsCall.gps_sms_call(config)
                #except:
                    #print('Failed to sms or call')
                time.sleep(1)
        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            self.close()
            
bp = ButtonPush()
bp.setup()
bp.buttonPush()
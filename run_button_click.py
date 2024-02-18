#!/usr/bin/python3

from gpiozero import Button
import time
from datetime import datetime

from gps_sms_call_button import GpsSMSCall

class ButtonPush:
    def __init__(self):
        self.button = Button(22)
        
    def setup(self):
        self.gpsSmsCall = GpsSMSCall()
        self.gpsSmsCall.setup()
    
    def close(self):
        self.gpsSmsCall.shutdown()
        
    def buttonPush(self):
        try:
            while(True):
                print('Waiting for button press...')
                self.button.wait_for_press()
                print('[%s] button pressed' % (str(datetime.now())))
                 #try:
                self.gpsSmsCall.gps_sms_call()
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
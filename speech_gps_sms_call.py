from datetime import datetime
import os
import struct

import pvporcupine
from pvrecorder import PvRecorder

from gps_sms_call_button import GpsSMSCall

# Speech Recognizer class 
class SpeechRecognizer:
    # ACCESS KEY for PicoVoice
    ACCESS_KEY = 'kmLSiatpWXsVBkfKJ2Xm2JA9+FZPWnVt5Vv2cScu/7bvsQqZzZiisw=='
    # keyword file path
    keyword_paths = ['/home/avengers/rruchir-tech/keywork_files/icecream_en_raspberry-pi_v3_0_0.ppn']
    
    # setup process
    def setup(self):
        # create a object of the GpsSMSCall class
        self.gpsSmsCall = GpsSMSCall()
        # call the setup to start the SIM7600X and open GPS
        self.gpsSmsCall.setup()
        # initialize wake keywords list
        self.keywords = list()
        
        # create porcupine connection 
        self.porcupine = pvporcupine.create(
            access_key=self.ACCESS_KEY,
            keyword_paths=self.keyword_paths
        )
        # collec the wake keywords
        for x in self.keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn','').split('_')
            if len(keyword_phrase_part) > 6:
                self.keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                self.keywords.append(keyword_phrase_part[0])
        print('Porcupine version: %s' % self.porcupine.version)

    # delte recorder and percupine
    def close(self):
        self.recorder.delete()
        self.porcupine.delete()
        self.gpsSmsCall.shutdown()


    # create a recorder and start listening to the user speech
    def startListeningAndProcess(self):
        # create a recorder
        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=0)
        # start the recorder to listen
        self.recorder.start()
        try:
            while True:
                print('Listening ...(press Ctrl+C to exit)')
                # read chunks of recorder
                pcm = self.recorder.read()
                # pass the recorder to porcupine to check if it had wake keyword
                result = self.porcupine.process(pcm)
            
                # if keyword exists then trigger the gps and sms & call  
                if result >= 0:
                    print('[%s] Detected %s' % (str(datetime.now()), self.keywords[result]))
                    #try:
                    self.gpsSmsCall.gps_sms_call()
                    #except:
                        #print('Failed to sms or call')
                
        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            self.close()
    

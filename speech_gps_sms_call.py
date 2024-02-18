from datetime import datetime
import os
import struct

import pvporcupine
from pvrecorder import PvRecorder

from gps_sms_call_button import GpsSMSCall

class SpeechRecognizer:
    ACCESS_KEY = 'kmLSiatpWXsVBkfKJ2Xm2JA9+FZPWnVt5Vv2cScu/7bvsQqZzZiisw=='
    keyword_paths = ['/home/avengers/rruchir-tech/keywork_files/icecream_en_raspberry-pi_v3_0_0.ppn']
    
    def setup(self):
        self.gpsSmsCall = GpsSMSCall()
        self.gpsSmsCall.setup()
        self.keywords = list()
        self.porcupine = pvporcupine.create(
            access_key=self.ACCESS_KEY,
            keyword_paths=self.keyword_paths
        )
        for x in self.keyword_paths:
            keyword_phrase_part = os.path.basename(x).replace('.ppn','').split('_')
            if len(keyword_phrase_part) > 6:
                self.keywords.append(' '.join(keyword_phrase_part[0:-6]))
            else:
                self.keywords.append(keyword_phrase_part[0])
        print('Porcupine version: %s' % self.porcupine.version)

    def close(self):
        self.recorder.delete()
        self.porcupine.delete()
        self.gpsSmsCall.shutdown()


    def startListeningAndProcess(self):
        self.recorder = PvRecorder(
            frame_length=self.porcupine.frame_length,
            device_index=0)
        self.recorder.start()
        try:
            while True:
                print('Listening ...(press Ctrl+C to exit)')
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)
            
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
    

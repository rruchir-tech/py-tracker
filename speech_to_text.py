#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
from datetime import datetime

from vosk import Model, KaldiRecognizer

from gps_sms_call_button import GpsSMSCall

class SpeechToText:

    # setup process
    def setup(self):
        """ Setup function for initialization. """
        self.queue = queue.Queue()
        
        # create a parser
        self.parser = argparse.ArgumentParser(add_help=False)       
        self.parser.add_argument(
            "-l", "--list-devices", action="store_true",
            help="show list of audio devices and exit")
        self.args, self.remaining = self.parser.parse_known_args()
        # query and display sound devices
        if self.args.list_devices:
            print(sd.query_devices())
            self.parser.exit(0)
        
        self.parser.add_argument(
            "-d", "--device", type=self.int_or_str,
            help="input device (numeric ID or substring)")
        self.parser.add_argument(
            "-r", "--samplerate", type=int, help="sampling rate")
        self.parser.add_argument(
            "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
        self.args = self.parser.parse_args(self.remaining)
        
        # create a object of the GpsSMSCall class
        self.gpsSmsCall = GpsSMSCall()
        # call the setup to start the SIM7600X and open GPS
        self.gpsSmsCall.setup()

    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    # insert the audio block in the queue
    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        #if status:
            #print('status =' + str(status), file=sys.stderr)
        self.queue.put(bytes(indata))


    def listenAndDetect(self, config):
        """"This listens to the audio block and converts to text and detects the safeword"""

        device = self.args.device
        if 'audio_device' in config.keys():
            device = config['audio_device']
              
        # set the default sample rate from the device
        if self.args.samplerate is None:
            device_info = sd.query_devices(device, "input")
            print('audio device = ' + device_info["name"])

            # soundfile expects an int, sounddevice provides a float:
            self.args.samplerate = int(device_info["default_samplerate"])
            print('Default sample rate = ' + str(self.args.samplerate))
        
        # set the default language as engliash
        if self.args.model is None:
            if 'model_lang' in config.keys():
                self.model = Model(lang=config["model_lang"])
            else:
                self.model = Model(lang="en-us")
        else:
            self.model = Model(lang=args.model)
        print('Model Language = ' + config['model_lang'])    

        try:
            sd.never_drop_input = True
            with sd.RawInputStream(
                samplerate=self.args.samplerate,
                blocksize = 8000,
                device=device,
                dtype="int16",
                channels=1,
                callback=self.callback):
                
                print("#" * 80)
                print("Press Ctrl+C to stop the listening...")
                print("#" * 80)

                rec = KaldiRecognizer(self.model, self.args.samplerate)
                while True:
                    data = self.queue.get()
                    if rec.AcceptWaveform(data):
                        output= rec.FinalResult()
                        #print(output + ", safe word = " + config['safeword'] + ", detected = " + str(config['safeword'] in output))
                        if config['safeword'] in output:
                            print('[%s] Detected safeword : %s' % (str(datetime.now()), config['safeword']))
                            try:
                               self.gpsSmsCall.gps_sms_call(config)
                            except Exception as e:
                               print(e)
                    #else:
                        #print(rec.PartialResult())
        except KeyboardInterrupt:
            print("\nDone")
            self.gpsSmsCall.shutdown()
            self.parser.exit(0)
        except Exception as e:
            self.gpsSmsCall.shutdown()        
            self.parser.exit(type(e).__name__ + ": " + str(e))

config = {
    'audio_device': 1,
    'model_lang': 'en-us',
    'safeword': 'ice cream',
    'phone_number': 6284687669,
    'sms_prefix_msg': '[Emergency Alert]:safeword detection. Person is currently at this location',
    'call_duration': 20,
    }

sp = SpeechToText()
sp.setup()
sp.listenAndDetect(config)

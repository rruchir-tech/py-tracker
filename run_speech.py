#!/usr/bin/python3

from speech_gps_sms_call import SpeechRecognizer

sr = SpeechRecognizer()
sr.setup()
sr.startListeningAndProcess()

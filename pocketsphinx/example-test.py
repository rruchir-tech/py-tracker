import os
from pocketsphinx import LiveSpeech, get_model_path

#    while(True):
print('Listening ...')
speech = LiveSpeech(lm=False, keyphrase='mango', kws_threshold=1e-20)
for phrase in speech:
    try:
        print(phrase.segments(detailed=True))
    except:
        print('None')

    
print('Completed')
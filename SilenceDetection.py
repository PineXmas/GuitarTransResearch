__author__ = 'nghia'

import pyaudio
import wave
import sys
from time import sleep
from pylab import *


CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

wf = wave.open('01.Twinkle.wav', 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(1024)
print(data.__len__())
print(p.get_format_from_width(wf.getsampwidth()))
print(wf.getnchannels())

print(wf.getframerate())

while data != '':
    stream.write(data)
    #sleep(0.001)
    #for i in range(len(data)):
    #    print(ord(data[1])),
    #print()
    data = wf.readframes(1024)

stream.stop_stream()
stream.close()

p.terminate()

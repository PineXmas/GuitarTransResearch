__author__ = 'pinexmas'

import pyaudio
import wave
from array import array
import sys
from time import sleep

CHUNK = 1
# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

wf = wave.open('01.Twinkle.wav', 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

# my_str = "hello world"
# bytes = str.encode(my_str)
# type(bytes) # insures its bytes
# my_decoded_str = str.decode(bytes)
# type(my_decoded_str) # insures its string

print(type(data))
count = 1;
while data != '':
    noise = False
    for aByte in data:
        if ord(aByte) > 50 and ord(aByte) < 0:
            noise = True
    ++count
    #if not noise then play
    if noise:
        stream.write(data)
    #sleep(0)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()


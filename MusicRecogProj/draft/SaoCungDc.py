__author__ = 'pinexmas'

import pyaudio
import wave
from array import array
import sys


def trim(snd_data):
    FLAG = 0

    snd_started = False
    r = array('h')

    for i in snd_data:
        # if not snd_started and abs(i) > FLAG:
        #     snd_started = True
        #     r.append(i)
        #
        # elif snd_started:
            r.append(i)
    return r
"-----------------------------------------------"
CHUNK = 1024
# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

wf = wave.open('08.Jungle Bell.wav', 'rb')

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


while data != '':
    byteArr = str.encode(data, 'utf_32')
    trimmed = trim(byteArr)
    trimmedStr = str.decode(data, 'utf_32')
    stream.write(trimmedStr)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()


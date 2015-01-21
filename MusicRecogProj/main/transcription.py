__author__ = 'nghia'

from tools import *
from reference import frequency_estimator
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

readWav = read_wav("input/removed_02.hb.wav", 15)
(rate, data) = wavfile.read("input/removed_02.hb.wav")
hps = []
for i in range(len(readWav[0])):
    print "Processing window " + str(i) + "..."
    hps.append(frequency_estimator.freq_from_hps(readWav[0][i], readWav[1].sampleRate))

print hps

# plot the first 1024 samples
plt.plot(hps)

# label the axes
plt.ylabel("Frequency")
plt.xlabel("Time (samples)")

# set the title
plt.title("Frequency Estimator with Harmonic Product Spectrum")
# display the plot
plt.show()
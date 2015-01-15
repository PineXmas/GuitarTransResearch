__author__ = 'nghia'

from pymir import AudioFile
import numpy as np
import matplotlib.pyplot as plt

def read_wav(filePath, windowTime):
    wavData = AudioFile.open(filePath)
    windows = wavData.frames(wavData.sampleRate*windowTime/1000)
    return windows


def spectral_centroid(window):
    return window.spectrum().centroid()


def short_term_energy(window):
    xi = 0  # the short-term energy for the i-th window
    for m in range(0, len(window) - 1):
        hamming = 0.54 + 0.46 * np.cos(2 * np.pi * (len(window) - m - 1) / (len(window) - 1))  # use hamm)ing window
        xi += np.power(window[m], 2) * np.power(hamming, 2)
    return xi

windows = read_wav("input/example.wav", 10)
X = [short_term_energy(window) for window in windows]
Y = [spectral_centroid(window) for window in windows]

# plot the first 1024 samples
plt.plot(Y)

# label the axes
plt.ylabel("Amplitude")
plt.xlabel("Time (samples)")

# set the title
plt.title("Flute Sample")
# display the plot
plt.show()
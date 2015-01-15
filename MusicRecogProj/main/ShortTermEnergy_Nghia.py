__author__ = 'nghia'

import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt



#read audio samples
input_data = wav.read('02.Happy Birthday.wav')
audio = input_data[1]
x = audio[:, 0]

# initialize parameter
timeframe = 100  # 10ms
N = input_data[0]/timeframe  # each window width is the timeframe
n = N  # the index of current window
X = []

# calculate short-term energy of each window
def short_term_energy(x, n, N):
    """
    calculate short-term-energy for the n-th window in the given audio x

    x: array
        the audio
    n: int
        index of window
    N: int
        number of frames in a window
    """
    Xi = 0  # the short-term energy for the i-th window
    for m in range(n - N + 1, n):
        hamming = 0.54 + 0.46 * np.cos(2 * np.pi * (n - m) / (N - 1))  # use hamm)ing window
        Xi = Xi + np.power(x[m], 2) * np.power(hamming, 2)
    return Xi

while n <= len(x):
    Xi = short_term_energy(x, n, N)
    X.append(Xi)
    n += N

# plot the first 1024 samples
plt.plot(X[:])

# label the axes
plt.ylabel("Amplitude")
plt.xlabel("Time (samples)")

# set the title
plt.title("Flute Sample")
# display the plot
plt.show()
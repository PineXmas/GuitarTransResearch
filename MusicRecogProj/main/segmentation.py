import numpy
from scipy.signal import argrelmax
import scipy.io.wavfile as wav
import matplotlib.pyplot as plot

from main.tools import *
from ShortTermEnergy import short_term_energy


# settings
timeframe = 100  # 10ms
isSmooth = True # smooth input before finding maximas or not
nBins = 1000 # number of total bins in histogram
smooth_win_len = 7
songName = '02.Happy Birthday.wav'

# histogram: array of floats
listEnergy = []
listSpectral = []

# read audio samples
input_data = wav.read(songName)
audio = input_data[1]
x = audio[:, 0] # get channel 0 only

# calculate numbe of
N = input_data[0]/timeframe  # each window width is the timeframe

# gather values for histograms
# for window in windows:
#     # calculate feature values
#     valEngergy = short_term_energy(window, N, N)
#     valSpectral = 0
#     # append list
#     listEnergy.append(valEngergy)
#     listSpectral.append(valSpectral)

n = N
while n <= len(x):
    Xi = short_term_energy(x, n, N)
    listEnergy.append(Xi)
    n += N

# sort list of values
listEnergy.sort()
# listSpectral.sort()

# create histograms
binStep = (listEnergy[len(listEnergy)-1] - listEnergy[0]) / nBins
gramEnergy = gen_histogram(listEnergy, binStep)
# gramSpectral = gen_histogram(listSpectral, binStep)

# find local maximas
arrayEnergy = numpy.asarray(gramEnergy) # convert to ndarray
# methods = ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
methods = ['hanning']

# plot
plot.plot(arrayEnergy[:100])
plot.hold(True)
if isSmooth:
    for method in methods:
        plot.plot(smooth(arrayEnergy, smooth_win_len, method)[:100])
plot.ylabel("Frequency")
plot.xlabel("Bin")
plot.title("Histogram, window_len=" + smooth_win_len.__str__())
legend = ['original']
legend.extend(methods)
plot.legend(legend)
plot.show()

result = argrelmax(arrayEnergy)
a = 0
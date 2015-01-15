import numpy
from scipy.signal import argrelmax
import scipy.io.wavfile as wav
import matplotlib.pyplot as plot
from tools import *
from ShortTermEnergy import short_term_energy
from extract_features import *
from scipy.io.wavfile import write


# settings
timeframe = 10  # miliseconds
isSmooth = True # smooth input before finding maximas or not
nBins = 1000 # number of total bins in histogram
smooth_win_len = 7
thresWeight = 1.5
path = 'input/'
fileName = '08.jb.wav'
filePath = path + fileName

# read audio & split to windows
readAudio = read_wav(filePath, timeframe)
windows = readAudio[0]

# calculate thresholds
threshold = calculate_threshold(windows, nBins, isSmooth, smooth_win_len, thresWeight)

# print thresholds
tE = threshold[0]
tS = threshold[1]
listE = threshold[2]
listS = threshold[3]
print 'Energy Threshold = ' + str(tE)
print 'SpecCT Threshold = ' + str(tS)

# recognize note
noiseRemoved = []
noNoise = []
for i in range(0, len(listE)-1):
    e = listE[i]
    s = listS[i]
    if e >= tE and s >= tS:
        # copy
        noiseRemoved.extend(windows[i])
        noNoise.extend(windows[i])
    else:
        for j in range(0, len(windows[i])-1):
            noiseRemoved.append(0)

# plot
plot.subplot(311)
plot.plot(listE)
plot.title('Energy')
plot.subplot(312)
plot.plot(listS)
plot.title('Spectral')
plot.subplot(313)
plot.plot(noiseRemoved)
plot.title('Noise removed')
plot.show()

# create wav file
noNoise = np.asarray(noNoise)
scaled = np.int16(noNoise/np.max(np.abs(noNoise)) * 32767)  # 32767 means 16 signed bit
write(path + 'removed_' + fileName, readAudio[1].sampleRate, scaled)
import numpy
from scipy.signal import argrelmax
import scipy.io.wavfile as wav
import matplotlib.pyplot as plot
from tools import *
from ShortTermEnergy import short_term_energy
from extract_features import *


# settings
timeframe = 10  # 10ms
isSmooth = True # smooth input before finding maximas or not
nBins = 1000 # number of total bins in histogram
smooth_win_len = 7
filePath = 'input/02.hb.wav'

# read audio & split to windows
windows = read_wav(filePath, timeframe)

# calculate thresholds
threshold = calculate_threshold(windows, nBins, isSmooth, smooth_win_len, thresWeight=1)

# print thresholds
print 'Energy Threshold = ' + str(threshold[0])
print 'SpecCT Threshold = ' + str(threshold[1])

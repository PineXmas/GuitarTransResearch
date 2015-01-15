import numpy
from scipy.signal import argrelmax
import scipy.io.wavfile as wav
import matplotlib.pyplot as plot

from tools import *
from ShortTermEnergy import short_term_energy


# settings
timeframe = 100  # 10ms
isSmooth = True # smooth input before finding maximas or not
nBins = 1000 # number of total bins in histogram
smooth_win_len = 7
songName = '02.Happy Birthday.wav'

# read audio samples
input_data = wav.read(songName)
audio = input_data[1]
x = audio[:, 0] # get channel 0 only

# calculate number of frame in one window
N = input_data[0]/timeframe  # each window width is the timeframe

# calculate thresholds
energyThreshold = calculate_threshold(N, x, nBins, isSmooth, smooth_win_len, thresWeight=1)

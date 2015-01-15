__author__ = 'pinexmas'


def gen_histogram(listVal, binStep):
    binMax = listVal[0] + binStep
    binCount = 0
    histogram = []
    for val in listVal:
        if val <= binMax:
            binCount += 1
        else:
            # add curr bin to histogram
            histogram.append(binCount)
            # next bin
            binMax += binStep
            binCount = 1

    # add the last bin
    histogram.append(binCount)

    return histogram


import numpy


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = numpy.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    # print(len(s))
    if window == 'flat':  #moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = eval('numpy.' + window + '(window_len)')

    y = numpy.convolve(w / w.sum(), s, mode='valid')
    return y

import numpy
from scipy.signal import argrelmax
import scipy.io.wavfile as wav
import matplotlib.pyplot as plot
from extract_features import *


def calculate_threshold(windows, nBins, isSmooth, smooth_win_len, thresWeight):
    '''
    calculate 2 threshold values
    :return: list [t1, t2]
    '''

    # histogram: array of floats
    listEnergy = []
    listSpectral = []

    # gather values for histograms
    print 'Calculating feature values...'
    for window in windows:
        Ei = short_term_energy(window)
        Si = spectral_centroid(window)
        # Yi = spectral_centroid()
        listEnergy.append(Ei)
        listSpectral.append(Si)

    # sort list of values
    listEnergy.sort()
    listSpectral.sort()

    # create histograms
    print 'Generating histograms...'
    binStep = (listEnergy[len(listEnergy)-1] - listEnergy[0]) / nBins
    gramEnergy = gen_histogram(listEnergy, binStep)
    gramSpectral = gen_histogram(listSpectral, binStep)

    # (smooth if need) find local maximas
    # ENERGY
    print 'Smooth & Find local maximas...'
    gramEnergy = numpy.asarray(gramEnergy) # convert to ndarray
    method = 'flat'
    if isSmooth:
        gramEnergySmooth = smooth(gramEnergy, smooth_win_len, method)
    else:
        gramEnergySmooth = gramEnergy
    resultE = argrelmax(gramEnergySmooth)
    # SPECTRAL
    gramSpectral = numpy.asarray(gramSpectral) # convert to ndarray
    method = 'flat'
    if isSmooth:
        gramSpectralSmooth = smooth(gramSpectral, smooth_win_len, method)
    else:
        gramSpectralSmooth = gramSpectral
    resultS = argrelmax(gramEnergySmooth)

    # plot
    plot.subplot(211)
    plot.plot(gramEnergy)
    plot.hold(True)
    legend = ['original']
    if isSmooth:
        plot.plot(gramEnergySmooth)
        legend.append('smoothed')
    plot.ylabel("Frequency")
    plot.xlabel("Bin")
    plot.title("EnergyHistogram, window_len=" + smooth_win_len.__str__())
    plot.legend(legend)
    plot.subplot(212)
    plot.plot(gramSpectral)
    plot.hold(True)
    legend = ['original']
    if isSmooth:
        plot.plot(gramSpectralSmooth)
        legend.append('smoothed')
    plot.ylabel("Frequency")
    plot.xlabel("Bin")
    plot.title("SpectralCentroidHistogram, window_len=" + smooth_win_len.__str__())
    plot.legend(legend)
    plot.show()

    # retrieve 2 first maximas
    e1 = gramEnergySmooth[resultE[0][0]]
    e2 = gramEnergySmooth[resultE[0][1]]
    s1 = gramEnergySmooth[resultS[0][0]]
    s2 = gramEnergySmooth[resultS[0][1]]

    # print
    print 'Done.'
    print 'Energy: 2 first maximas: ' + str(e1) + ', ' + str(e2)
    print 'SpecCT: 2 first maximas: ' + str(s1) + ', ' + str(s2)

    # calculate threshold: short term energy
    thresWeight = float(thresWeight)
    e = (thresWeight * e1 + e2) / (thresWeight + 1)

    # calculate threshold: spectral centroid
    s = (thresWeight * s1 + s2) / (thresWeight + 1)

    return [e, s]
__author__ = 'nghia'

import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

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
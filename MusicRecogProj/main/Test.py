from math import *

from pylab import *
from numpy.random import *

from main.tools import smooth


t=linspace(-4,4,100)
x=sin(t)
xn=x+random(len(t))*0.1

ws=31

subplot(212)
plot(ones(ws))

windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']

hold(True)
for w in windows[1:]:
    eval('plot('+w+'(ws) )')

axis([0,30,0,1.1])

legend(windows)
title("The smoothing windows")

subplot(211)
plot(x)
plot(xn)
for w in windows:
    plot(smooth(xn,10,w))
l=['original signal', 'signal with noise']
l.extend(windows)

legend(l)
title("Smoothing a noisy signal")
show()
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from warnings import warn
fs, data = wavfile.read('ProprietaryMusic/MusicTest.wav') # load the data
sub = int(fs/30)
if len(data.T) == 2:
	b = data.T[0] #only reads single track
	warn("reading single audio track")
else:
	b = data.T
#b = data.T[0] # this is a two channel soundtrack, I get the first track
#b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
c = fft(b) # calculate fourier transform (complex numbers list)
d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
mediate = abs(c[:(d-1)])
plt.plot(mediate,'r')

k = np.arange(len(data))
T = len(data)/fs  # where fs is the sampling frequency
frqLabel = k/T 

max_ind = np.argmax(mediate)
max_val = np.max(mediate)
print(max_val)
mediate[max_ind]=0
max_ind = np.argmax(mediate)
max_val = np.max(mediate)
print(max_val)
mediate[max_ind]=0
max_ind = np.argmax(mediate)
max_val = np.max(mediate)
print(max_val)
 
plt.show()
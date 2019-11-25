import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import serial
import array
import struct

def process_to_color( fft_plot , frequencies):
	max_ind = np.argmax(fft_plot)
	#max_val = np.max(fft_plot)
	if frequencies[max_ind] != 0:
		pitch = 12 * np.log2( frequencies[max_ind] / 16.35)
	else: 
		pitch = 1.0
	#map 0-12 0-360
	#probably map 0-65535 to 0-1
	h = pitch % 12
	h = h / 12
	color = hsv_to_rgb(h, 1, 1)
	return color, pitch

RATE    = 44100
CHUNK   = int(44100/7)

k = np.arange(CHUNK)
T = CHUNK/RATE  # where fs is the sampling frequency
frqLabel = k/T

p = pyaudio.PyAudio()

#player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

ser = serial.Serial('COM12',115200)

running = True

while running:

	b = np.frombuffer(stream.read(CHUNK),dtype=np.int16)

	c = fft(b) # calculate fourier transform (complex numbers list)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	proc = abs(c[:(d-1)])
	color, pitch = process_to_color(proc,frqLabel)
	color_buf = np.array( np.multiply(255,color) ).astype(int)
	write_bytes = struct.pack('<' + 'B' * len(color_buf),  *color_buf) 
	print(write_bytes)
	ser.write(write_bytes)


#for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
#	print(np.fromstring(stream.read(CHUNK),dtype=np.int16))

stream.stop_stream()
stream.close()
p.terminate()
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from colorsys import hsv_to_rgb
import pygame
import serial
import struct

def audio_to_color( audio_chunk , frequencies):
	c = fft(audio_chunk)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	proc = abs(c[:(d-1)])
	max_ind = np.argmax(proc)
	#max_val = np.max(fft_plot)
	if frequencies[max_ind] != 0:
		#pitch is half-steps above C0
		pitch = 12 * np.log2( frequencies[max_ind] / 16.35)
	else: 
		#log of zero is imaginary, and sometimes that is a value that is returned so /shrug
		pitch = 1.0
	#map 0-12 0-360deg (0-1 for hsv fucntion input)
	h = pitch % 12 #only look at octaves
	color = hsv_to_rgb(h/12, 1, 1)
	return color

filename = "TestFiles/ColorTest5.wav"

fs, data = wavfile.read(filename) # load the data
division = 14 #division of audio
chunk_size = int(fs/division) #the subdivisions to take the fft of 
b = data.T[0] # this is a two channel soundtrack, I get the first track

#k = np.arange(chunk_size)
#T = chunk_size/fs  # where fs is the sampling frequency same as 1/division
#frqLabel = k/T
frqLabel = division*np.arange(chunk_size) #magic I am not fully able to explain yet

color_array = []
#This is to pre-process the wav file
for chunk in range(0,len(b)-chunk_size,chunk_size):
	color = audio_to_color( b[chunk:chunk+chunk_size] ,frqLabel)
	color_array.append(np.multiply(255,color))

#opens serial port to arduino. Change COM12 for whatever you need
ser = serial.Serial('COM12',115200)

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for color in color_array:
	color_buf = np.array( color ).astype(int)
	#forces the values to be bytes so it can be sent over serial
	write_bytes = struct.pack('<' + 'B' * len(color_buf),  *color_buf) 
	print(write_bytes)
	ser.write(write_bytes)

	#Tries to colors in sync, but not perfect
	pygame.time.wait(round(1000/division))
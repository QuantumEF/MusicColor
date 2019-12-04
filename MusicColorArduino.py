from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from colorsys import hsv_to_rgb
import pygame
import serial
import struct
import MusicColorLib as mcl

wavcolor = mcl.wavcolor("TestFiles/ColorTest5.wav")

#opens serial port to arduino. Change COM12 for whatever you need
ser = serial.Serial('COM12',115200)

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for color in wavcolor.colors:
	color_buf = np.array( color ).astype(int)
	#forces the values to be bytes so it can be sent over serial
	write_bytes = struct.pack('<' + 'B' * len(color_buf),  *color_buf) 
	print(write_bytes)
	ser.write(write_bytes)

	#Tries to colors in sync, but not perfect
	pygame.time.wait(round(1000/division))
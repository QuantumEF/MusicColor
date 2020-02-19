import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import serial
import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import pygame
import MusicColorLib as mcl
import struct

sample_rate = 44100
division = 7
chunk_size = int(44100/division)

#This opens an audio stream from the mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

color_stream = mcl.LiveColor(sample_rate, chunk_size)
#color_stream.add_band('low', 20, 150)
#color_stream.add_band('lowmid', 150, 500)
color_stream.add_band('mid', 500, 1200)
#color_stream.add_band('highmid', 1200, 6000)
#color_stream.add_band('high', 6000, 20000)

#opens serial port to arduino, change COM12 to whatever you need to 
ser = serial.Serial('COM5',115200)

while True:

	b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	color_bands = color_stream.color_band_buffer(b)
	print(color_bands)
	#b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	#color = color_stream.color_buffer(b)

	color_buf = np.array( color_bands["mid"] ).astype(int)
	write_bytes = struct.pack('<' + 'B' * len(color_buf),  *color_buf) 
	print(write_bytes)
	ser.write(write_bytes)

stream.stop_stream()
stream.close()
p.terminate()
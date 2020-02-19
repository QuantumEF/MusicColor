import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import serial
import array
import struct
import MusicColorLib as mcl

fs = 41000
chunk_size = int(41000/7)

color_stream = mcl.LiveColor(fs, chunk_size)

#This opens an audio stream from the mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=chunk_size)

#opens serial port to arduino, change COM12 to whatever you need to 
ser = serial.Serial('COM5',115200)

while True:

	b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	color = color_stream.color_buffer(b)

	color_buf = np.array( color ).astype(int)
	write_bytes = struct.pack('<' + 'B' * len(color_buf),  *color_buf) 
	print(write_bytes)
	ser.write(write_bytes)

stream.stop_stream()
stream.close()
p.terminate()
import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import pygame

def audio_to_color( audio_chunk_size , frequencies):
	c = fft(audio_chunk_size)
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

fs = 44100
division = 7
chunk_size = int(44100/division)

#k = np.arange(chunk_size)
#T = chunk_size/fs  # where fs is the sampling frequency
#frqLabel = k/T
frqLabel = division*np.arange(chunk_size) #magic I am not fully able to explain yet

#This opens an audio stream from the mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=chunk_size)

#pygame screen setup
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
running = True

#Color Display
while running:
	b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	color = audio_to_color(b,frqLabel)

	background_colour = np.multiply(255,color)
	screen.fill(background_colour)
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

stream.stop_stream()
stream.close()
p.terminate()
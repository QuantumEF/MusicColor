from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame

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

#pygame scren setup
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for color in color_array:
	print(color)
	screen.fill(color)
	pygame.display.flip()

	#Tries to show colors in sync with sound, but isn't perfect
	pygame.time.wait(round(1000/division)) 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
from colorsys import hsv_to_rgb
import pygame

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

filename = "Piano1.wav"

fs, data = wavfile.read(filename) # load the data
div = 14
sub = int(fs/div) #the subdivisions to take the fft of 
b = data.T[0] # this is a two channel soundtrack, I get the first track
k = np.arange(len(data[:sub]))
T = len(data[:sub])/fs  # where fs is the sampling frequency
frqLabel = k/T


counter = 0;
color_array = [] #will store the colors 
while not(counter>len(b)):
	c = fft(b[counter:counter+sub]) # calculate fourier transform (complex numbers list)
	counter += sub
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	proc = abs(c[:(d-1)])
	color, pitch = process_to_color(proc,frqLabel)
	color_array.append(np.multiply(255,color))

(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
running = True
counter = 0

pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)
while running:

	background_colour = color_array[counter]
	print(background_colour)
	counter += 1
	screen.fill(background_colour)

	pygame.display.flip()

	pygame.time.wait(round(1000/div))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False




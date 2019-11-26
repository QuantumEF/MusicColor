#20-150 Low 150-500 LowMid 500-1200 Mid 1200-6000 HighMid 6000-20000 High
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame
import MusicColorLib as mcl

"""
def audio_fft(audio_chunk):
	c = fft(audio_chunk)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	return abs(c[:(d-1)])

def audio_fft_to_color( audio_fft_chunk , frequencies):
	#proc = audio_fft(audio_chunk)
	max_ind = np.argmax(audio_fft_chunk)
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
	return np.multiply(255,color)

def audio_fft_range_to_color(audio_fft, sample_rate, division, lower_freq, upper_freq):
	frequencies = division*np.arange(int(sample_rate/division))
	freq_bounds = [round(lower_freq/division),round(upper_freq/division)]
	freq_range = frequencies[ freq_bounds[0]:freq_bounds[1] ]
	fft_range = audio_fft[ freq_bounds[0]:freq_bounds[1] ]
	color = audio_fft_to_color(fft_range,freq_range)
	return color
"""

def audio_fft_to_standard_range(audio_fft, sample_rate, division):
	low_color = mcl.audio_fft_range_to_color(audio_fft, sample_rate, division, 20, 150)
	lowmid_color = mcl.audio_fft_range_to_color(audio_fft, sample_rate, division, 150, 500)
	mid_color = mcl.audio_fft_range_to_color(audio_fft, sample_rate, division, 500, 1200)
	highmid_color = mcl.audio_fft_range_to_color(audio_fft, sample_rate, division, 1200, 6000)
	high_color = mcl.audio_fft_range_to_color(audio_fft, sample_rate, division, 6000, 20000)
	return (low_color,lowmid_color,mid_color,highmid_color,high_color)

filename = "ProprietaryMusic/MusicTest.wav"
division = 7 #division of audio
color_array = []
fs, fft_array = mcl.wav_to_fft(filename, division)

for fft in fft_array:
	color = audio_fft_to_standard_range(fft, fs, division)
	color_array.append(color)

#pygame scren setup
(width, height) = (500, 100)
screen = pygame.display.set_mode((width, height))

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for colors in color_array:
	pygame.draw.rect(screen, colors[0], (0,0,100,100), 0)
	pygame.draw.rect(screen, colors[1], (100,0,100,100), 0)
	pygame.draw.rect(screen, colors[2], (200,0,100,100), 0)
	pygame.draw.rect(screen, colors[3], (300,0,100,100), 0)
	pygame.draw.rect(screen, colors[4], (400,0,100,100), 0)
	pygame.display.flip()

	#Tries to show colors in sync with sound, but isn't perfect
	pygame.time.wait(round(1000/division)) 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
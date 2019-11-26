from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame
import MusicColorLib as mcl

filename = "ProprietaryMusic/MusicTest.wav"
division = 14 #division of audio
color_array = []
fs, fft_array = mcl.wav_to_fft(filename, division)

for fft in fft_array:
	color = mcl.audio_fft_to_color(fft, fs, division)
	color_array.append(color)

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
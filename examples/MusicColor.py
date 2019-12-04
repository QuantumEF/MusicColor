from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame
from MusicColorLib import WavColor

filename = "ProprietaryMusic/MusicTest2.wav"
wavtest = WavColor(filename)
wavtest.process_colors()

#pygame scren setup
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for color in wavtest.colors:
	print(color)
	screen.fill(color)
	pygame.display.flip()

	#Tries to show colors in sync with sound, but isn't perfect
	pygame.time.wait(round(1000/wavtest.division)) 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
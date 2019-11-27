#20-150 Low 150-500 LowMid 500-1200 Mid 1200-6000 HighMid 6000-20000 High
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame
from MusicColorLib import WavColor

filename = "ProprietaryMusic/MusicTest.wav"

wavtest = WavColor(filename)
wavtest.add_band('low', 20, 150)
wavtest.add_band('lowmid', 150, 500)
wavtest.add_band('mid', 500, 1200)
wavtest.add_band('highmid', 1200, 6000)
wavtest.add_band('high', 6000, 20000)
wavtest.process_all_band_colors()

#pygame scren setup
(width, height) = (500, 100)
screen = pygame.display.set_mode((width, height))

#audio playback
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play(-1)

#color display
for i in range(len(wavtest.color_bands["low"])):
	pygame.draw.rect(screen, wavtest.color_bands["low"][i], (0,0,100,100), 0)
	pygame.draw.rect(screen, wavtest.color_bands["lowmid"][i], (100,0,100,100), 0)
	pygame.draw.rect(screen, wavtest.color_bands["mid"][i], (200,0,100,100), 0)
	pygame.draw.rect(screen, wavtest.color_bands["highmid"][i], (300,0,100,100), 0)
	pygame.draw.rect(screen, wavtest.color_bands["high"][i], (400,0,100,100), 0)
	pygame.display.flip()

	#Tries to show colors in sync with sound, but isn't perfect
	pygame.time.wait(round(1000/wavtest.division)) 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
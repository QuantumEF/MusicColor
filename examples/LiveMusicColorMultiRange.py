import pyaudio
import numpy as np
from scipy.fftpack import fft
from colorsys import hsv_to_rgb
import pygame
import MusicColorLib as mcl

sample_rate = 44100
division = 7
chunk_size = int(44100/division)

#This opens an audio stream from the mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

#pygame screen setup
(width, height) = (500, 100)
screen = pygame.display.set_mode((width, height))
running = True

color_stream = mcl.LiveColor(sample_rate, chunk_size)
color_stream.add_band('low', 20, 150)
color_stream.add_band('lowmid', 150, 500)
color_stream.add_band('mid', 500, 1200)
color_stream.add_band('highmid', 1200, 6000)
color_stream.add_band('high', 6000, 20000)


#Color Display
while running:
	b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	color_bands = color_stream.color_band_buffer(b)
	print(color_bands)
	pygame.draw.rect(screen, color_bands["low"], (0,0,100,100), 0)
	pygame.draw.rect(screen, color_bands["lowmid"], (100,0,100,100), 0)
	pygame.draw.rect(screen, color_bands["mid"], (200,0,100,100), 0)
	pygame.draw.rect(screen, color_bands["highmid"], (300,0,100,100), 0)
	pygame.draw.rect(screen, color_bands["high"], (400,0,100,100), 0)
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

stream.stop_stream()
stream.close()
p.terminate()
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
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
running = True

#Color Display
while running:
	b = np.frombuffer(stream.read(chunk_size),dtype=np.int16)
	audio_fft = mcl.audio_fft(b)
	color = mcl.audio_fft_to_color(audio_fft, sample_rate, division)
	screen.fill(color)
	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

stream.stop_stream()
stream.close()
p.terminate()
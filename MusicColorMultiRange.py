#20-150 Low 150-500 LowMid 500-1200 Mid 1200-6000 HighMid 6000-20000 High
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame

def audio_fft(audio_chunk):
	c = fft(audio_chunk)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	return abs(c[:(d-1)])

def audio_to_color( audio_fft_chunk , frequencies):
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

def audio_to_multicolor(audio_fft, sample_rate, division):
	#proc = audio_fft(audio_chunk)
	audio_dict = {}

	frequencies = division*np.arange(int(sample_rate/division))

	low = [round(20/division),round(150/division)]
	lowmid = [round(150/division),round(500/division)]
	mid = [round(500/division),round(1200/division)]
	highmid = [round(1200/division),round(6000/division)]
	high = [round(6000/division),round(20000/division)]

	low_freq = frequencies[ low[0]:low[1] ]
	lowmid_freq = frequencies[ lowmid[0]:lowmid[1] ]
	mid_freq = frequencies[ mid[0]:mid[1] ]
	highmid_freq = frequencies[ highmid[0]:highmid[1] ]
	high_freq = frequencies[ high[0]:high[1] ]

	low_fft = audio_fft[ low[0]:low[1] ]
	lowmid_fft = audio_fft[ lowmid[0]:lowmid[1] ]
	mid_fft = audio_fft[ mid[0]:mid[1] ]
	highmid_fft = audio_fft[ highmid[0]:highmid[1] ]
	high_fft = audio_fft[ high[0]:high[1] ]

	low_color = audio_to_color(low_fft,low_freq)
	lowmid_color = audio_to_color(lowmid_fft,lowmid_freq)
	mid_color = audio_to_color(mid_fft,mid_freq)
	highmid_color = audio_to_color(highmid_fft,highmid_freq)
	high_color = audio_to_color(high_fft,high_freq)

	return (low_color,lowmid_color,mid_color,highmid_color,high_color)

filename = "ProprietaryMusic/MusicTest.wav"

fs, data = wavfile.read(filename) # load the data
division = 14 #division of audio
chunk_size = int(fs/division) #the subdivisions to take the fft of 
b = data.T[0] # this is a two channel soundtrack, I get the first track

#k = np.arange(chunk_size)
#T = chunk_size/fs  # where fs is the sampling frequency same as 1/division
#frqLabel = k/T
frqLabel = division*np.arange(chunk_size) #magic I am not fully able to explain yet

#This is to pre-process the wav file
color_array = []
for chunk in range(0,len(b)-chunk_size,chunk_size):
	proc_audio = audio_fft(b[chunk:chunk+chunk_size])
	colors = audio_to_multicolor( proc_audio , fs, division)
	print(colors)
	color_array.append(colors)

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
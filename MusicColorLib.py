from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
import pygame
from warnings import warn

def audio_fft(audio_chunk):
	c = fft(audio_chunk)
	d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
	return abs(c[:(d-1)])

class AudioFFT:
	def __init__(self, audio_chunk, sample_rate, division):
		if audio_chunk != 0:
			c = fft(audio_chunk)
			d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
			self.fft = abs(c[:(d-1)])
			self.frequency_range = division*np.arange(int(sample_rate/division))
			self.division = division
			self.sample_rate = sample_rate


def audio_fft_to_color( audio_fft ):
	#frequencies = division*np.arange(int(sample_rate/division))
	max_ind = np.argmax(audio_fft_chunk.fft)
	#max_val = np.max(fft_plot)
	if audio_fft.frequency_range[max_ind] != 0:
		#pitch is half-steps above C0
		pitch = 12 * np.log2( audio_fft.frequency_range[max_ind] / 16.35)
	else: 
		#log of zero is imaginary, and sometimes that is a value that is returned so /shrug
		pitch = 1.0
	#map 0-12 0-360deg (0-1 for hsv fucntion input)
	h = pitch % 12 #only look at octaves
	color = hsv_to_rgb(h/12, 1, 1)
	return np.multiply(255,color)

def audio_fft_range_to_color(audio_fft, lower_freq, upper_freq):
	#frequencies = division*np.arange(int(sample_rate/division))
	fft_range = AudioFFT(0, audio_fft.sample_rate, audio_fft.division)
	freq_bounds = [round(lower_freq/audio_fft.division),round(upper_freq/audio_fft.division)]
	fft_range.frequency_range = audio_fft.frequency_range[ freq_bounds[0]:freq_bounds[1] ]
	fft_range.fft = audio_fft.fft[ freq_bounds[0]:freq_bounds[1] ]
	return audio_fft_to_color(fft_range)

'''
def wav_to_fft(filename, division):
	fs, data = wavfile.read(filename) # load the data
	chunk_size = int(fs/division) #the subdivisions to take the fft of 
	if len(data.T) == 2:
		b = data.T[0] # this is a two channel soundtrack, I get the first track
	else:
		b = data.T

	fft_array = []
	#This is to pre-process the wav file
	for chunk in range(0,len(b)-chunk_size,chunk_size):
		audio_proc = audio_fft(b[chunk:chunk+chunk_size])
		fft_array.append(audio_proc)

	return fs, fft_array
'''

class WavColor:
	def __init__(self, filename, division=7):
		#self.sample_rate, data = wavfile.read(filename) # load the data
		sample_rate, data = wavfile.read(filename) # load the data
		self.filename = filename
		#self.division = division
		self.chunk_size = int(fs/division) #the subdivisions to take the fft of 
		self.freq_scale = self.division*np.arange(int(self.sample_rate/self.division))
		self.channels = {}

		if len(data.T) == 2:
			self.audio = data.T[0] #only reads single track
			warn("Stero file detected, using only track[0]")
		else:
			self.audio = data.T

		self.fft_array = []
		#This is to pre-process the wav file
		for chunk in range(0,len(self.audio)-self.chunk_size,self.chunk_size):
			processed_audio = AudioFFT( b[chunk:chunk+self.chunk_size], sample_rate, division)
			self.fft_array.append(processed_audio)

	def create_channel(self, channel_name, lower_freq, upper_freq):
		if (lower_freq < 0) or (lower_freq > self.sample_rate):
			raise Exception('lower freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq > self.sample_rate) or (upper_freq < 0):
			raise Exception('upper freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq <= lower_freq):
			raise Exception('improper frequency range defined.')

		freq_bounds = [round(lower_freq/self.division),round(upper_freq/self.division)]
		#freq_range = self.freq_scale[ freq_bounds[0]:freq_bounds[1] ]
		self.channels[channel_name] =  freq_bounds
		#self.channels[channel_name] = [lower_freq, upper_freq]

	def process_all_channel_colors(self):
		for channel in channels.values():
			for fft in fft_array:
					#frequencies = division*np.arange(int(sample_rate/division))
					#freq_bounds = [round(lower_freq/division),round(upper_freq/division)]
					#freq_range = frequencies[ freq_bounds[0]:freq_bounds[1] ]
					return audio_fft_range_to_color(fft, channel[0], channel[1])

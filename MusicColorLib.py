from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from colorsys import hsv_to_rgb
from warnings import warn

class AudioFFT:
	def __init__(self, audio_chunk = None, sample_rate = 44100, division = 7, frequency_range = np.full([8,1],None)):
		if frequency_range.all() != None:
			c = fft(audio_chunk)
			d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
			self.fft = abs(c[:(d-1)])
			self.frequency_range =frequency_range
			self.sample_rate = sample_rate
			self.division = division
		elif audio_chunk.all() != None:
			c = fft(audio_chunk)
			d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
			self.fft = abs(c[:(d-1)])
			self.frequency_range = division*np.arange(int(sample_rate/division))
			self.division = division
			self.sample_rate = sample_rate
		else:
			self.fft = []
			self.frequency_range = frequency_range
			self.division = division
			self.sample_rate = sample_rate

#this takes an input of class AudioFFT
def audio_fft_to_color( audio_fft ):
	max_ind = np.argmax(audio_fft.fft)
	#max_val = np.max(fft_plot)
	if audio_fft.frequency_range[max_ind] != 0:
		#pitch is half-steps above C0
		pitch = 12 * np.log2( audio_fft.frequency_range[max_ind] / 16.35)
	else: 
		#log of zero is imaginary, and sometimes that is a value that is returned so /shrug
		pitch = 0
	#map 0-12 0-360deg (0-1 for hsv fucntion input)
	h = pitch % 12 #only look at octaves
	color = hsv_to_rgb(h/12, 1, 1)
	return np.multiply(255,color)

#This takes an input of class AudioFFT and a lover and upper frequency bounds
def audio_fft_range_to_color(audio_fft, lower_freq = None, upper_freq = None, freq_bounds = np.full([8,1],None) ):
	if freq_bounds.all() == None:
		freq_bounds = [round(lower_freq/audio_fft.division),round(upper_freq/audio_fft.division)]
	fft_range = AudioFFT(np.full([8,1],None), audio_fft.sample_rate, audio_fft.division, audio_fft.frequency_range[ freq_bounds[0]:freq_bounds[1] ])
	#fft_range.frequency_range = audio_fft.frequency_range[ freq_bounds[0]:freq_bounds[1] ]
	fft_range.fft = audio_fft.fft[ freq_bounds[0]:freq_bounds[1] ]
	return audio_fft_to_color(fft_range)

class WavColor:
	def __init__(self, filename, division=7):
		self.sample_rate, data = wavfile.read(filename) # load the data
		self.filename = filename
		self.chunk_size = int(self.sample_rate/division) #the subdivisions to take the fft of 
		self.freq_scale = division*np.arange(self.chunk_size)
		self.division = division

		#color channels
		self.bands = {}
		self.color_bands = {}
		self.colors = []

		if len(data.T) == 2:
			self.audio = data.T[0] #only reads single track
			warn("Stero file detected, using only track[0]")
		else:
			self.audio = data.T

		self.fft_array = []
		#This is to pre-process the wav file
		for chunk in range(0,len(self.audio)-self.chunk_size,self.chunk_size):
			processed_audio = AudioFFT( self.audio[chunk:chunk+self.chunk_size], self.sample_rate, division )
			self.fft_array.append(processed_audio)

	def add_band(self, band_name, lower_freq, upper_freq):
		if (lower_freq < 0) or (lower_freq > self.sample_rate):
			raise Exception('lower freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq > self.sample_rate) or (upper_freq < 0):
			raise Exception('upper freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq <= lower_freq):
			raise Exception('improper frequency range defined.')

		freq_bounds = [round(lower_freq/self.division),round(upper_freq/self.division)]
		self.bands[band_name] =  freq_bounds

	def process_all_band_colors(self):
		if len(self.bands) == 0:
			raise Exception("No bands have been defined, use process_colors() instead.")
		for name, bounds in self.bands.items():
			self.color_bands[name] = []
			for fft in self.fft_array:
				self.color_bands[name].append( audio_fft_range_to_color(fft, bounds[0], bounds[1]) )

	def process_colors(self):
		for fft in self.fft_array:
			self.colors.append( audio_fft_to_color(fft) )


class LiveColor:
	def __init__(self, sample_rate, chunk_size):
		self.sample_rate = sample_rate
		self.chunk_size = chunk_size
		self.division = int(sample_rate/chunk_size)
		self.bands = {}
		self.freq_scale = self.division*np.arange(self.chunk_size)

	def add_band(self, band_name, lower_freq, upper_freq):
		if (lower_freq < 0) or (lower_freq > self.sample_rate):
			raise Exception('lower freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq > self.sample_rate) or (upper_freq < 0):
			raise Exception('upper freqency is out of bounds: 0-' + str(self.sample_rate)+'.')
		elif (upper_freq <= lower_freq):
			raise Exception('improper frequency range defined.')

		freq_bounds = [round(lower_freq/self.division),round(upper_freq/self.division)]
		frequency_range = self.freq_scale[ freq_bounds[0]:freq_bounds[1] ]
		self.bands[band_name] = [freq_bounds, frequency_range]

	def __live_fft(self, audio_chunk):
		c = fft(audio_chunk)
		d = int(len(c)/2)  # you only need half of the fft list (real signal symmetry)
		return abs(c[:(d-1)])

	def color_band_buffer(self, stream_chunk):
		return None
		processed_audio = AudioFFT(stream_chunk, self.sample_rate, self.division, self.freq_scale)
		color_bands = {}
		for band_name, band_data in self.bands.items():
			color_bands[band_name] = audio_fft_range_to_color(processed_audio, band_data[0][0], band_data[0][1], band_data[1])

		return color_bands

	def color_buffer(self, stream_chunk):
		processed_audio = AudioFFT(stream_chunk, self.sample_rate, self.division, self.freq_scale)
		print(processed_audio.fft)
		return audio_fft_to_color( processed_audio )
	
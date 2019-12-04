# MusicColor
 The main library is MusicColorLib.py. 
 This library will take audio anc convert it into s series of color.

 ## Classes and Functions

  ##### WavColor( filename, division = 7 )

   This class just needs to be given a filename to process. It can also take the argument "divisions" which determines the color samples per second.

   - The method process_colors() will convert the wave file into an array of colors accesible by WavColor.colors[]
   - The method add_band( name, lower_frequency, upper_frequency ) will only process the color with respect to the frequency range defined by lower and upper frequency.
   - The method process_all_band_colors() will convert the bands defined from add_band() to a dictionary with key names and the color array for each band accesible from WavColor.color_bands[]

  ##### LiveColor( sample_rate, chunk_size )

  This class needs the sample rate of the audio and the chunk size of the audio that it will be processing each time the color_buffer() or color_band_buffer() methods are called
  - The method add_band( name, lower_frequency, upper_frequency ) will only process the color with respect to the frequency range defined by lower and upper frequency.
  - The method color_buffer( stream_chunk ) takes a chunk from the audio stream and converts it into a color
  - The method color_band_buffer( stream_chunk ) takes a chunk from the audio stream and divides it according to the bands defined from add_band() to a dictionary with key names and the color for each band

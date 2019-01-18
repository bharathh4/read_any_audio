'''
This is a cheap silence padding detection program in audio files. Just silence
detection at the beginning.
'''

from os.path import join

import numpy as np
from read_audio import read_audio

def has_padding(filepath, padding_in_seconds=0.1):
    
    y, fs = read_audio(filepath)
    N = y.size
    window_seconds = 0.0125 # 12.5 ms
    window_sample_size = int(window_seconds * fs)
    number_of_windows = int(N/window_sample_size)
    reshaped_y = y[:number_of_windows * window_sample_size].reshape(number_of_windows, window_sample_size)
    y_windowed_var = np.var(reshaped_y, axis=1)
    
    num_sil_windows_in_samples = int(padding_in_seconds/window_seconds)
    
    return np.sum(y_windowed_var[:num_sil_windows_in_samples - 1]) <  num_sil_windows_in_samples * 20 # why -1 -- just need to get this almost right # why 20 what if is not really true absolute silence

if __name__ == "__main__":
    
    filepath = join('audio', 'aaron.wav')
    print(has_padding(filepath))
    filepath = join('audio', 'aaron_has_padding.wav')
    print(has_padding(filepath))
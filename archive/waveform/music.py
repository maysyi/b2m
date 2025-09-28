import pandas as pd
import numpy as np
from scipy.io import wavfile
import pyaudio

import oscillator

df = pd.read_csv("freq.csv")

# Access as dictionary
freq3_dict = dict(zip(df['NOTE'], df['FREQ3']))
freq4_dict = dict(zip(df['NOTE'], df['FREQ4']))
freq5_dict = dict(zip(df['NOTE'], df['FREQ5']))

def get_samples(osc):
    return [int(next(osc) * 32767) for i in range(44100)]

def get_octave(octave):
    if octave == 3:
        freq_dict = freq3_dict
    elif octave == 4:
        freq_dict = freq4_dict
    elif octave == 5:
        freq_dict = freq5_dict
    else:
        freq_dict = freq3_dict
    return freq_dict

def get_note(note, freq_dict):
    note_freq = freq_dict.get(note)
    print(note_freq)
    gen = oscillator.WaveAdder(
        oscillator.SineOscillator(freq=note_freq, amp=1)
        # oscillator.TriangleOscillator(freq=pot_value, amp=0.8),
        # oscillator.SawtoothOscillator(freq=pot_value, amp=0.6),
        # oscillator.SquareOscillator(freq=pot_value, amp=0.4),
    )
    return gen
    
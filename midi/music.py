import pandas as pd
import numpy as np
from scipy.io import wavfile
import pyaudio
import mido

df = pd.read_csv("midi.csv")

# Access as dictionary
freq3_dict = dict(zip(df['NOTE'], df['FREQ3']))
freq4_dict = dict(zip(df['NOTE'], df['FREQ4']))
freq5_dict = dict(zip(df['NOTE'], df['FREQ5']))

def scale_note(pot_value):
    if pot_value < 85:
        note = "C"
    elif pot_value < 170:
        note = "C#"
    elif pot_value < 256:
        note = "D"
    elif pot_value < 341:
        note = "D#"
    elif pot_value < 426:
        note = "E"
    elif pot_value < 512:
        note = "F"
    elif pot_value < 597:
        note = "F#"
    elif pot_value < 683:
        note = "G"
    elif pot_value < 768:
        note = "G#"
    elif pot_value < 853:
        note = "A"
    elif pot_value < 938:
        note = "A#"
    else:
        note = "B"
    return note

def get_octave(octave):
    if octave == 3:
        midi_dict = freq3_dict
    elif octave == 4:
        midi_dict = freq4_dict
    elif octave == 5:
        midi_dict = freq5_dict
    else:
        midi_dict = freq3_dict
    return midi_dict

def get_note(note, midi_dict):
    note_midi = midi_dict.get(note)
    msg_on = mido.Message('note_on', note=note_midi, velocity=100)
    return msg_on

def off_note(note, midi_dict):
    note_midi = midi_dict.get(note)
    msg_off = mido.Message('note_off', note=note_midi, velocity=0)
    return msg_off
    
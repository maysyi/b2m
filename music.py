import pandas as pd
import numpy as np
from scipy.io import wavfile
import mido

df = pd.read_csv("midi.csv")
df2 = pd.read_csv("chords.csv")

# Access as dictionary
freq3_dict = dict(zip(df['NOTE'], df['FREQ3']))
freq4_dict = dict(zip(df['NOTE'], df['FREQ4']))
freq5_dict = dict(zip(df['NOTE'], df['FREQ5']))
print(freq3_dict)
print(freq4_dict)
print(freq5_dict)

chords_dict = {}
for _, row in df2.iterrows():
    note = row["NOTE"]
    # Drop NaNs and the NOTE column itself
    chords_dict[note] = row.drop(labels=["NOTE"]).dropna().to_dict()

def _to_byte(x):
    # convert numpy/scalars/strings -> int, then clip to 0..127
    if x is None:
        return 0
    else:
        x = int(round(float(x)))
        return max(0, min(127, x))

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

def get_chord(note, option):
    row = chords_dict[note]
    if option == 1:
        return [note, row["MAJ2"], row["MAJ3"]]
    elif option == 2:
        return [note, row["MIN2"], row["MIN3"]]
    elif option == 3:
        return [note, row["DIM2"], row["DIM3"]]
    elif option == 4:
        return [note, row["DOM72"], row["DOM73"], row["DOM74"]]
    elif option == 5:
        return [note, row["MIN72"], row["MIN73"], row["MIN74"]]

def get_note(note, midi_dict):
    if note == "Db": note = "C#"
    if note == "Eb": note = "D#"
    if note == "Gb": note = "F#"
    if note == "Ab": note = "G#"
    if note == "Bb": note = "A#"
    if note == "Cb": note = "B"
    note_midi = midi_dict.get(note)
    note_midi = _to_byte(note_midi)
    msg_on = mido.Message('note_on', note=note_midi, velocity=100)
    return msg_on

def off_note(note, midi_dict):
    if note == "Db": note = "C#"
    if note == "Eb": note = "D#"
    if note == "Gb": note = "F#"
    if note == "Ab": note = "G#"
    if note == "Bb": note = "A#"
    if note == "Cb": note = "B"
    note_midi = midi_dict.get(note)
    note_midi = _to_byte(note_midi)
    msg_off = mido.Message('note_off', note=note_midi, velocity=0)
    return msg_off
    
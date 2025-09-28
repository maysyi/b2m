import serial
import pyaudio
import numpy as np
from music import scale_note, get_octave, get_chord, get_note, off_note
import threading
import time
import mido

# === Setup Serial ===
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=0.1)

outport = mido.open_output()
outport.send(mido.Message('program_change', program=89))

# Shared variables between threads
pot_value = 0
button_state = 0
octave = 3
lock = threading.Lock()
running = True
current_note = "X"

# === Thread 1: Read Arduino ===
def read_arduino():
    global pot_value, button_state, octave, running
    OCTAVE_DEBOUNCE_MS = 300 / 1000
    last_octave_change_time = 0
    while running:
        line = arduino.readline().decode(errors='ignore').strip()
        if not line:
            continue
        now = time.time()
        try:
            if line == "D" and octave > 3:
                if now - last_octave_change_time >= OCTAVE_DEBOUNCE_MS:
                    octave -= 1
                    last_octave_change_time = now
                    print("Octave down:", octave)
            elif line == "U" and octave < 5:
                if now - last_octave_change_time >= OCTAVE_DEBOUNCE_MS:
                    octave += 1
                    last_octave_change_time = now
                    print("Octave up:", octave)
            else:
                pot_str, button_str = line.split(",")
                with lock:
                    pot_value = int(pot_str.strip())
                    button_state = int(button_str.strip())
        except ValueError:
            continue
        time.sleep(0.005)  # small delay to reduce CPU usage

# === Thread 2: Play Audio ===
def play_audio():
    global pot_value, button_state, octave, running, current_note
    pressed = False                  # are we currently in the "button held" state?
    current_note_name = None         # name for debugging
    DEBOUNCE_MS = 30 / 1000.0        # 30 ms debounce
    last_button = 0
    last_change_time = time.time()
    while running:
        with lock:
            current_pot = pot_value
            current_button = button_state
            current_octave = octave # Update with button
        now = time.time()
        if current_button != last_button:
            last_change_time = now
            last_button = current_button
        # only treat change if stable for DEBOUNCE_MS
        stable = (now - last_change_time) >= DEBOUNCE_MS

        if stable and current_button != 0 and not pressed:
            # rising edge -> enter pressed state and play note
            pressed = True
            note_name = scale_note(current_pot)
            midi_dict = get_octave(current_octave)
            chord_name = get_chord(note_name, current_button)
            for note in chord_name:
                print(note)
                msg_on = get_note(note, midi_dict)
                outport.send(msg_on)
            current_note_name = note_name
            current_chord_name = chord_name
        elif pressed and current_button != 0:
            # still pressed — check if pot changed to a different note
            note_name = scale_note(current_pot)
            if note_name != current_note_name:
                # turn off previous
                for note in current_chord_name:
                    msg_off = off_note(note, midi_dict)
                    outport.send(msg_off)
                # turn on new
                chord_name = get_chord(note_name, current_button)
                for note in chord_name:
                    msg_on = get_note(note, midi_dict)
                    outport.send(msg_on)
                current_note_name = note_name
                current_chord_name = chord_name
        elif stable and current_button == 0 and pressed:
            # falling edge -> leave pressed state, turn off note
            for note in current_chord_name:
                msg_off = off_note(note, midi_dict)
                outport.send(msg_off)
            pressed = False
        time.sleep(0.003)

# === Start Threads ===
t1 = threading.Thread(target=read_arduino)
t2 = threading.Thread(target=play_audio)

t1.start()
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    t1.join()
    t2.join()

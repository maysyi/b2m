import serial
import pyaudio
import numpy as np
from music import get_octave, get_note
import threading
import time

# === Setup Serial ===
arduino = serial.Serial(port='COM9', baudrate=115200, timeout=0.1)

# === Setup Audio Stream ===
stream = pyaudio.PyAudio().open(
    rate=44100,
    channels=1,
    format=pyaudio.paInt16,
    output=True
)

# Shared variables between threads
pot_value = 0
button_state = 0
lock = threading.Lock()
running = True
current_note = "X"

# === Thread 1: Read Arduino ===
def read_arduino():
    global pot_value, button_state, running
    while running:
        line = arduino.readline().decode(errors='ignore').strip()
        if not line:
            continue
        try:
            pot_str, button_str = line.split(",")
            with lock:
                pot_value = int(pot_str.strip())
                button_state = int(button_str.strip())
        except ValueError:
            continue
        time.sleep(0.005)  # small delay to reduce CPU usage

# === Thread 2: Play Audio ===
def play_audio():
    global pot_value, button_state, running, current_note
    while running:
        with lock:
            current_button = button_state
            current_octave = 4 # Update with button
        if current_button == 1:
            freq_dict = get_octave(current_octave)
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
            if note != current_note:
                current_note = note
                gen = get_note(note, freq_dict)
            iter(gen)
            samples = [int(next(gen) * 32767) for i in range(128)]
            wav = np.int16(samples).tobytes()
            stream.write(wav)
            print("done")
        else:
            time.sleep(0.01)  # idle when button not pressed

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
    stream.stop_stream()
    stream.close()
    print("Exiting program")

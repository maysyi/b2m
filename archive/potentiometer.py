import serial
import pyaudio

from music import get_octave, get_note

arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)

stream = pyaudio.PyAudio().open(
    rate=44100,
    channels=1,
    format=pyaudio.paInt16,
    output=True
)

while True:
    line = arduino.readline().decode(errors='ignore').strip()
    freq_dict = get_octave(3)
    if line is int: # only process if something was actually sent
        try:
            pot_str, button_str = line.split(",")
            pot_value = int(pot_str.strip())
            button_state = int(button_str.strip())
            wav = get_note(pot_value, freq_dict)
            stream.write(wav)
        except ValueError:
            print("Invalid data:", line)
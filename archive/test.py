# test_pyaudio.py
import numpy as np
import pyaudio

SAMPLE_RATE = 44100
DURATION = 2.0
FREQ = 440.0

t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
samples = 0.5 * np.sin(2 * np.pi * FREQ * t)     # float in [-0.5,0.5]
pcm16 = (samples * 32767).astype('int16').tobytes()
print(pcm16)

p = pyaudio.PyAudio()
stream = p.open(rate=SAMPLE_RATE, channels=1, format=pyaudio.paInt16, output=True)
stream.write(pcm16)
stream.stop_stream()
stream.close()
p.terminate()
print("Done")
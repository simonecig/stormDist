import pyaudio
import struct
import keyboard
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

mic = pyaudio.PyAudio()
INTERVAL = 0.1
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024*10

stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                  input=True, output=True, frames_per_buffer=CHUNK)

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    data_np = np.array(data_int, dtype='b')[::2]
    f, t, Sxx = signal.spectrogram(data_np, fs=CHUNK)
    dBS = 10 * np.log10(Sxx)
    plt.clf()
    plt.pcolormesh(t, f, dBS, vmin=-120, vmax=0)
    plt.colorbar()
    plt.pause(0.001)
    if keyboard.is_pressed('q'):
        break

stream.stop_stream()
stream.close()
mic.terminate()

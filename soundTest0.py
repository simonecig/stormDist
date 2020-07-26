import pyaudio
import struct
import keyboard
import librosa as libr
import librosa.display
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

mic = pyaudio.PyAudio()
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000
CHUNK = 1024 * 50

stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                  input=True, output=False, frames_per_buffer=CHUNK)

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    data_np = np.frombuffer(data, dtype=np.float32)
    plt.clf()
    hop_length = 1024
    D = libr.amplitude_to_db(np.abs(libr.stft(data_np,
                                              hop_length=hop_length)),
                             ref=np.max)
    libr.display.specshow(D, y_axis='log', sr=RATE, hop_length=hop_length,
                          x_axis='time')
    plt.colorbar(format="%+2.f dB")
    plt.pause(0.001)
    if keyboard.is_pressed('q'):
        break

stream.stop_stream()
stream.close()
mic.terminate()

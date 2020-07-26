import pyaudio
import struct
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Set up pyadio
pya = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16    # audio format
CHANNELS = 1                 # single channel for microphone (2 for stereo)
RATE = 20000                # samples per seconds (sampling rate)
CHUNK = int(RATE/20)        # samples per frame
THRESHOLD = 50            # minimun audio recorded

# Create new figure
fig = plt.figure()
# fig, ax = plt.subplots(2)
# x = np.arange(0, 4 * CHUNK, 2)
# y = np.arange(0, 4 * CHUNK, 2)
# ax[0].set_ylim(0, 255)
# plot0, = ax[0].plot(x, y)
plt.show(block=False)

# To record audio a stream needs to be opened
stream = pya.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)
while True:
    data = stream.read(CHUNK)
    data = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')
    f, t, Sxx = signal.spectrogram(data, fs=CHUNK)
    dBS = 10 * np.log10(Sxx)
    #ax[0].plot(x, 10*np.log10(data+128))
    plt.pcolormesh(t, f, dBS)
    plt.pause(0.005)

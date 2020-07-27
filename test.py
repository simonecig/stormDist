import sounddevice as sd
import queue
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

q = queue.Queue()
SAMPLERATE = 44100


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(indata[::10])


def update_plot(frame):
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        # Roll array elements along the x axis
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


length = int(200 * SAMPLERATE / (1000 * 10))
plotdata = np.zeros((length, 1))

fig, ax = plt.subplots()
lines = ax.plot(plotdata)

ax.axis((0, len(plotdata), -1, 1))


stream = sd.InputStream(
    channels=1, samplerate=SAMPLERATE, callback=audio_callback)
ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
with stream:
    plt.show()

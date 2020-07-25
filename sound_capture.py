import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError

#-----constants-----#
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format 
CHANNELS = 1                 # single channel for microphone (2 for stereo)
RATE = 44100                 # samples per second (44.1 kHz)


#-----figure and axes-----#
fig = plt.figure(figsize=(15,8))
# modo un po' tricky per farci stare il titolo di entrambi i plot 
# senza che si sovrappongano in modo orribile e non si capisca più niente,
# praticamente gli sto dicendo:
# dividi la figura in una griglia di 20 righe (e una colonna)
# il primo plot ha spazio dalla riga 0 alla riga 10 però occupa solo 7 righe 
# (in questo modo lascio spazio al titolo del plot sotto)
# il secondo plot ha spazio dalla riga 10 alla riga 20 però occupa anche lui solo 7 righe 
ax1 =  plt.subplot2grid((20, 1), (0, 0), rowspan=7, colspan=1)
ax2 =  plt.subplot2grid((20, 1), (10, 0), rowspan=7, colspan=1)

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
# le costanti definite sopra servono qui per dire a pyaudio di registrare da microfono
# e come registrare (a che rate, in che formato e su quanti canali)
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# linear plot for the audio wafeform
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# log plot for the audio spectrum
# semilog dice di mettere log solo all'asse x che sono le frequenze
# in questo modo si vedono moooolto meglio 
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Amplitude')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_title('AUDIO SPECTRUM')
ax2.set_xlabel('Frequency')
ax2.set_ylabel('Magnitude')
ax2.set_xlim(20, RATE / 2)

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
# faccio partire una specie di clock 
start_time = time.time()

while True:
    
    # binary data
    # pyaudio usa un formato di dati orribile che poi bisogna
    # far diventare plottabile usando struct
    data = stream.read(CHUNK)  
    
    # convert data to integers, make np array, then offset it by 127
    # faccio diventare i dati comprensibili
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    #---- audio waveform ----#
    # setto i dati sull'asse y nel while così si aggiornano
    line.set_ydata(data_np)
    
    #---- audio spectrum ----#
    # faccio la trasformata di fuorier per prendermi le frequenze
    yf = fft(data_int)
    # setto i dati sull'asse y nel while così si aggiornano
    line_fft.set_ydata(np.abs(yf[0:CHUNK])  / (128 * CHUNK))
    
    # aggiorno la figura e incremento conteggio dei frame
    # ogni aggiornamento è un nuovo frame e in base al tempo segnato dal clock
    # posso calcolare gli fps
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        # calcolo gli fps
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
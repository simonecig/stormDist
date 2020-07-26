# STORMdist

## About the project
__STORMdist__ is a mobile app that allows to determine the _distance_ of an upcoming _storm_ from the user by recording the timing between lightning and thunder.  

## How does it work
__STORMdist__ records via camera the flash of the lightning and records via microphone the typical thunder noise: knowing that the light travel at the speed _c = 299 792 458 m / s_ while the sound travels at _v = 343 m / s_ (assuming that the air temperature is _T = 20 ° C_) and measuring the time difference between the recording of lightning (travels at the speed of light) and recording of thunder (travels at the speed of sound), __STORMdist__ is able to determine the distance of the storm from the user.


## Development
The app is entirely developed in Python: the key _modules_ used to achieve the results are the following:
 - [OpenCV](https://opencv.org/)
    - This module has been used to track the lightning via camera
 - [PyAudio](https://pypi.org/project/PyAudio/)
    - This module has been used to record the sound of the thunder via microphone
 - [Kivy](https://kivy.org/)
    - This module has been used to develop the mobile application

### Development breakdown
The first code we wrote is [capture_webcam.py](https://github.com/niklai99/stormDist/blob/master/capture_webcam.py), which allowed us to getting familiar with the OpenCV module: we got access to the camera of the computer and, in [video_histogram.py](https://github.com/niklai99/stormDist/blob/master/video_histogram.py), we managed to extrapolate the greyscale histogram from the video recorded by the camera. The idea behind this is that, when a lightning occurs, the camera will record a spike in the whites: via the histogram is possible to determine whether the lightning occurred or not.

In [frameSubtraction.py](https://github.com/niklai99/stormDist/blob/master/frameSubtraction.py) we wanted to reduce the noise in the greyscale histogram. For this purpose, we decided to subtract the previous frame to the actual recorded one: the camera then records only the pixels changing tone in a colorgray scale from one frame to the next. In this way, the signal of a flash (typical of a lightning) is much a cleaner spike in the whites! 

We then shifted our focus to sound recording: in [sound_capture.py](https://github.com/niklai99/stormDist/blob/master/sound_capture.py) using the PyAudio module we managed to visualize the sound waveform of the signal recived via microphone. By applying a Fast Fourier Trasform we then obtained the frequency of the signal, allowing us to visualize the sound spectrum. 

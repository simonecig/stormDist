# STORMdist

## About the project
__STORMdist__ is a mobile app that allows to determine the _distance_ of an upcoming _storm_ from the user by recording the timing between lightning and thunder.  

## How does it work
__STORMdist__ records via camera the flash of the lightning and records via microphone the typical thunder noise: knowing that the light travels at the speed _c = 299 792 458 m / s_ while the sound travels at _v = 343 m / s_ (assuming that the air temperature is _T = 20 ° C_) and measuring the time difference between the recording of lightning (travel at the speed of light) and recording of thunder (travel at the speed of sound), __STORMdist__ is able to determine the distance of the storm from the user.

## Development
The app is entirely developed in Python: the key _modules_ used to achieve the results are the following:
 - [OpenCV](https://opencv.org/)
 - [Kivy](https://kivy.org/)

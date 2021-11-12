# PID-for-microbit

This is an adjusted version of the Python PID controller by ivmech
https://github.com/ivmech/ivPID/blob/master/README.md

It is adjusted to make it run on a BBC Microbit board runnning MicroPython.
Main changes are in the use of the 'time' functions.

![IMG_2119](https://user-images.githubusercontent.com/93115887/141451462-b9b068a2-d9b7-4999-82c3-78fb18d6209e.jpg)

The great thing about this implementation is the use of a PID-object, in stead of doing the PID calculations in your Main-loop.
This enables more PID controllers at the same time. Great stuff when trying to sync 4 motors in 1 vehicle ;)

You'll find:
1. PIDClass.py					The PID-object code
2. MotorSync.py					The main body syncing 2 motors using the accelerometer
3. MotorSyncUX.py				The main body including the UX for setting the PID parameters interactively

For further explanation please have a look at the YouTube video here:

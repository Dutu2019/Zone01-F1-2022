#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from controls import Controls
import time

# Create your objects here.

controls = Controls(EV3Brick(), Motor(Port.D), Motor(Port.A), Motor(Port.C), ColorSensor(Port.S3), ColorSensor(Port.S2), ColorSensor(Port.S1))

while True:
    controls.runRace()
    
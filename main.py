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
brick = EV3Brick()
a = time.time()
waitingForWheelChange = False
brick.screen.print("Select race version:")
controls = Controls(brick, Motor(Port.A), Motor(Port.D), Motor(Port.C), ColorSensor(Port.S1), ColorSensor(Port.S2), ColorSensor(Port.S3), UltrasonicSensor(Port.S4))
while True:
    controls.main()

    if int(time.time() - a) == 5:
        waitingForWheelChange = True
    if waitingForWheelChange and (-20 < controls.angle < 20):
        controls.changeWheels(100)
        while not Button.UP in brick.buttons.pressed():
            pass
        waitingForWheelChange = False
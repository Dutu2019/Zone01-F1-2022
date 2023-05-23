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
controls = None
option = None
while True:
    for button in brick.buttons.pressed():
        if button == Button.UP:
            controls = Controls(brick, Motor(Port.A), Motor(Port.D), Motor(Port.C), ColorSensor(Port.S1), ColorSensor(Port.S2), ColorSensor(Port.S3))
        elif button == Button.DOWN:
            controls = Controls(brick, Motor(Port.A), Motor(Port.D), Motor(Port.C), ColorSensor(Port.S1), ColorSensor(Port.S2), ColorSensor(Port.S3), 700)
    if controls: controls.runRaceV2()
    # if int(time.time() - a) == 15:
    #     waitingForWheelChange = True
    # if waitingForWheelChange and (-20 < controls.averageAngle() < 20):
    #     controls.changeWheels(100)
    #     waitingForWheelChange = False
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.

class Controller():
    def __init__(self) -> None:
        self.LHreg = 0x44
        self.LVreg = 0x45
        self.RHreg = 0x46
        self.RVreg = 0x47
        self.controller = I2CDevice(Port.S4, 0x02>>1)
        self.maxSpeed = 720
        self.Lspeed = 0
        self.Rspeed = 0
    
    def readRemote(self) -> None:
        self.Lspeed = int((int.from_bytes(self.controller.read(self.LVreg), "little") - 127) * 720/128)
        self.Rspeed = int((int.from_bytes(self.controller.read(self.RVreg), "little") - 127) * 720/128)
    
    def getLspeed(self) -> int: return self.Lspeed
    def getRspeed(self) -> int: return self.Rspeed

controller = Controller()
Lmotor = Motor(Port.A, Direction.CLOCKWISE)
Rmotor = Motor(Port.C, Direction.CLOCKWISE)
while True:
    controller.readRemote()
    print(controller.getLspeed(), controller.getRspeed())
    Rmotor.run(controller.getLspeed())
    Lmotor.run(controller.getRspeed())
    wait(10)
    


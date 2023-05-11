
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time

class Controls():

    def __init__(self, Brick: EV3Brick, LMotor: Motor, RMotor: Motor, MMotor: Motor, LSensor: ColorSensor, MSensor: ColorSensor, RSensor: ColorSensor) -> None:
        self.Brick = Brick
        self.LMotor = LMotor
        self.RMotor = RMotor
        self.MMotor = MMotor
        self.LMotor.reset_angle(0)
        self.RMotor.reset_angle(0)
        self.MMotor.reset_angle(0)
        self.LSensor = LSensor
        self.MSensor = MSensor
        self.RSensor = RSensor
        self.LSensorCalib = 30
        self.MSensorCalib = 25
        self.RSensorCalib = 25
        self.starttime = time.time()
        self.angle = 0
        self.speed = 1000
        self.memory = [0]

    # Activate back motors
    def move(self, speed) -> None:
        self.LMotor.run(speed)
        self.RMotor.run(speed)

        # Proportionnal steering
        if self.angle > 0:
            self.LMotor.run(speed / (1 + self.angle/100))
        if self.angle < 0:
            self.RMotor.run(speed / (1 - self.angle/100))

    # Angle logic
    def increment_angle(self, inc: float):
        self.angle += inc
        if self.angle > 90:
            self.angle = 90
        elif self.angle < -90:
            self.angle = -90
        self.set_angle(self.angle)

    def set_angle(self, angle: float):
        if angle > 200: self.angle = 200
        elif angle < -200: self.angle = -200
        else: self.angle = angle
        self.MMotor.track_target(self.angle)
        if len(self.memory) == 35:
            self.memory.pop(0)
        self.memory.append(self.angle)

    def averageAngle(self) -> int:
        # Not working
        averageAngle = 0
        for i in self.memory:
            averageAngle += i
        averageAngle /= len(self.memory)
        return averageAngle

    def changeWheels(self, angle: int) -> None:
        a = time.time()
        self.move(self.speed/2)
        while time.time() - a < 2:
            self.set_angle(angle)
        while time.time() - a < 4:
            self.set_angle(-angle)
        while time.time() - a < 14:
            self.set_angle(0)
            self.move(0)

    # Main loops
    def runRace(self) -> None:
        # Presets: speed: 720, 1.7, 4.5
        #           speed: 800, 1.0, 4.8

        self.move(self.speed)
        self.Brick.screen.print(self.debug())

        if self.MSensor.reflection() < self.MSensorCalib:
            self.set_angle(1 * (self.LSensorCalib - self.LSensor.reflection()))
        else:
            if self.RSensor.reflection() < self.RSensorCalib:
                self.set_angle(4.8 * (self.LSensorCalib - self.LSensor.reflection()))
            elif self.LSensor.reflection() < self.LSensorCalib:
                self.set_angle(-4.8 * (self.RSensorCalib - self.RSensor.reflection()))
            elif self.RSensor.reflection() > self.RSensorCalib and self.LSensor.reflection() > self.LSensorCalib:
                self.set_angle(10 * self.memory[-1])
    
    def runRaceV2(self) -> None:
        self.move(self.speed)
        self.Brick.screen.print(self.debug())

        # Creates a multiplier in function of the average of the last angles
        turnMult = abs(self.averageAngle()) / 50 + 1

        if self.MSensor.reflection() < self.MSensorCalib:
            self.set_angle(1 * (self.LSensorCalib - self.LSensor.reflection()))
        else:
            if self.RSensor.reflection() < self.RSensorCalib:
                self.set_angle(turnMult * (self.LSensorCalib - self.LSensor.reflection()))
            elif self.LSensor.reflection() < self.LSensorCalib:
                self.set_angle(-turnMult * (self.RSensorCalib - self.RSensor.reflection()))
            elif self.RSensor.reflection() > self.RSensorCalib and self.LSensor.reflection() > self.LSensorCalib:
                self.set_angle(10 * self.memory[-1])
    
    def debug(self) -> list:
        return [self.LSensor.reflection(), self.MSensor.reflection(), self.RSensor.reflection()]
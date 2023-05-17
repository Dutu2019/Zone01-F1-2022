
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time

class Controls():

    def __init__(self, Brick: EV3Brick, LMotor: Motor, RMotor: Motor, MMotor: Motor, LSensor: ColorSensor, MSensor: ColorSensor, RSensor: ColorSensor, USensor: UltrasonicSensor) -> None:
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
        self.USensor = USensor
        self.LSensorCalib = 30
        self.MSensorCalib = 25
        self.RSensorCalib = 25
        self.angle = 0
        self.maxAngle = 200
        self.speed = 2000
        self.memory = [0]
        self.memoryLength = 10
        self.starttime = time.time()

    # Activate back motors
    def move(self, speed: int) -> None:
        self.LMotor.run(speed)
        self.RMotor.run(speed)

        # Proportionnal steering
        if self.angle > 0:
            self.LMotor.run(speed / (1 + self.angle/100))
        if self.angle < 0:
            self.RMotor.run(speed / (1 - self.angle/100))
    
    def moveStraight(self, speed: int) -> None:
        self.LMotor.run(speed)
        self.RMotor.run(speed)
    
    def checkDist(self) -> None:
        self.speed = max(0, 2 * (self.USensor.distance() - 200))

    # Angle logic
    def set_angle(self, angle: float) -> None:
        if angle > self.maxAngle: self.angle = self.maxAngle
        elif angle < -self.maxAngle: self.angle = -self.maxAngle
        else: self.angle = angle
        self.MMotor.track_target(self.angle)
        if len(self.memory) == self.memoryLength:
            self.memory.pop(0)
        self.memory.append(self.angle)

    def averageAngle(self) -> int:
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
    def runRace(self, turnMult = 4.8) -> None:
        self.checkDist()

        # print(self.averageAngle())
        self.move(self.speed)

        if self.MSensor.reflection() < self.MSensorCalib:
            self.set_angle(1 * (self.LSensorCalib - self.LSensor.reflection()))
        else:
            if self.RSensor.reflection() < self.RSensorCalib:
                self.set_angle(turnMult * (self.LSensorCalib - self.LSensor.reflection()))
            elif self.LSensor.reflection() < self.LSensorCalib:
                self.set_angle(-turnMult * (self.RSensorCalib - self.RSensor.reflection()))
            elif self.RSensor.reflection() > self.RSensorCalib and self.LSensor.reflection() > self.LSensorCalib:
                self.set_angle(100 * self.memory[-1])
    
    def runRaceV2(self) -> None:
        # Creates a multiplier in function of the average of the last angles
        turnMult = abs(self.averageAngle()) / 70 + 1
        self.runRace(turnMult)
    
    def runRaceV3(self) -> None:
        if -20 < self.averageAngle() < 20:
            self.runRace()
        else:
           self.runRaceV2()
    
    def debug(self) -> list:
        return self.averageAngle()
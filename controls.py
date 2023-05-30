
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time

class Controls():

    def __init__(self, Brick: EV3Brick, LMotor: Motor, RMotor: Motor, MMotor: Motor, LSensor: ColorSensor, MSensor: ColorSensor, RSensor: ColorSensor, USensor: UltrasonicSensor, maxSpeed=1000) -> None:
        self.Brick = Brick
        self.Brick.screen.clear()
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
        self.LSensorCalib = 20
        self.MSensorCalib = 30
        self.RSensorCalib = 25
        self.angle = 0
        self.maxAngle = 110
        self.memory = [0]
        self.memoryLength = 10 #70 for competition
        self.maxSpeed = maxSpeed
        self.speed = self.maxSpeed/2
        self.isPassing = False
        self.starttime = time.time()

    # Activate back motors
    def move(self) -> None:
        self.LMotor.run(self.speed)
        self.RMotor.run(self.speed)

        # Proportionnal steering
        if self.angle > 0:
            self.LMotor.run(self.speed / (1 + self.angle/45))
        if self.angle < 0:
            self.RMotor.run(self.speed / (1 - self.angle/45))
    
    def checkDist(self) -> None:
        self.speed = max(0, 2 * (self.USensor.distance() - 300))
        if self.USensor.distance() < 100:
            self.LMotor.hold()
            self.RMotor.hold()
            self.set_speed(0)

    # Angle logic
    def changeWheels(self, angle: int) -> None:
        a = time.time()
        self.move()
        while time.time() - a < 0.5:
            self.set_angle(angle)
        while time.time() - a < 1:
            self.set_angle(-angle)
        self.set_angle(0)
        self.set_speed(0)
        self.move()
    
    def averageAngle(self) -> float:
        sum = 0
        for i in self.memory:
            sum += i
        return sum / len(self.memory)
    
    # Setter functions
    def set_angle(self, angle: float) -> None:
        if angle > self.maxAngle: self.angle = self.maxAngle
        elif angle < -self.maxAngle: self.angle = -self.maxAngle
        else: self.angle = angle
        if len(self.memory) == self.memoryLength:
            self.memory.pop(0)
        self.memory.append(self.angle)
        self.MMotor.track_target(self.angle)

    def set_speed(self, speed: float) -> None:
        if speed > self.maxSpeed: self.speed = self.maxSpeed
        else: self.speed = max(0, speed)

    # Main loops
    def runRace(self, turnMult = 4.8) -> None:
        print(self.debug())

        if self.MSensor.reflection() < self.MSensorCalib:
            self.set_angle(0.1 * (self.LSensorCalib - self.LSensor.reflection()))
        else:
            if self.RSensor.reflection() < self.RSensorCalib:
                self.set_angle(turnMult * (self.LSensorCalib - self.LSensor.reflection()))
            elif self.LSensor.reflection() < self.LSensorCalib:
                self.set_angle(-turnMult * (self.RSensorCalib - self.RSensor.reflection()))
            elif self.RSensor.reflection() > self.RSensorCalib and self.LSensor.reflection() > self.LSensorCalib:
                self.set_angle(100 * self.angle)

        self.checkDist()
        self.move()
    
    def runRaceV2(self) -> None:
        # Creates a multiplier in function of the average of the last angles
        turnMult = abs(self.angle) / 160 + 1
        self.runRace(turnMult)
    
    def debug(self) -> float:
        return None
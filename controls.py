
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import time

class Controls():

    def __init__(self, Brick: EV3Brick, LMotor: Motor, RMotor: Motor, MMotor: Motor, LSensor: ColorSensor, MSensor: ColorSensor, RSensor: ColorSensor, maxSpeed=1000) -> None:
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
        # self.USensor = USensor
        self.LSensorCalib = 30
        self.MSensorCalib = 35
        self.RSensorCalib = 35
        self.angle = 0
        self.maxAngle = 80
        self.maxSpeed = maxSpeed
        self.speed = self.maxSpeed/2
        self.starttime = time.time()

    # Activate back motors
    def move(self) -> None:
        self.LMotor.run(self.speed)
        self.RMotor.run(self.speed)

        # Proportionnal steering
        if self.angle > 0:
            self.LMotor.run(self.speed / (1 + self.angle/35))
        if self.angle < 0:
            self.RMotor.run(self.speed / (1 - self.angle/35))
    
    # def checkDist(self) -> None:
    #     self.speed = max(0, 2 * (self.USensor.distance() - 200))

    # Angle logic
    def changeWheels(self, angle: int) -> None:
        a = time.time()
        self.move()
        while time.time() - a < 0.5:
            self.set_angle(angle)
        while time.time() - a < 1:
            self.set_angle(-angle)
        while time.time() - a < 11:
            self.set_angle(0)
            self.set_speed(0)
            self.move()
    
    # Setter functions
    def set_angle(self, angle: float) -> None:
        if angle > self.maxAngle: self.angle = self.maxAngle
        elif angle < -self.maxAngle: self.angle = -self.maxAngle
        else: self.angle = angle
        self.MMotor.track_target(self.angle)
        self.set_speed(self.maxSpeed - 0.3 * ((self.maxSpeed/self.maxAngle) * abs(self.angle)))
        self.move()

    def set_speed(self, speed: float) -> None:
        if speed > self.maxSpeed: self.speed = self.maxSpeed
        else: self.speed = max(0, speed)

    # Main loops
    def runRace(self, turnMult = 4.8) -> None:

        if self.MSensor.reflection() < self.MSensorCalib:
            self.set_angle(0.5 * (self.LSensorCalib - self.LSensor.reflection()))
        else:
            if self.RSensor.reflection() < self.RSensorCalib:
                self.set_angle(turnMult * (self.LSensorCalib - self.LSensor.reflection()))
            elif self.LSensor.reflection() < self.LSensorCalib:
                self.set_angle(-turnMult * (self.RSensorCalib - self.RSensor.reflection()))
            elif self.RSensor.reflection() > self.RSensorCalib and self.LSensor.reflection() > self.LSensorCalib:
                self.set_angle(100 * self.angle)
    
    def runRaceV2(self) -> None:
        # Creates a multiplier in function of the average of the last angles
        turnMult = abs(self.angle) / 135 + 1
        self.runRace(turnMult)
    
    def debug(self) -> float:
        return self.speed

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
        self.angle = 0
        self.speed = 720
        self.runtime = 0
        self.memory = [0]

    # Activate back motors
    def move(self, speed) -> None:
        self.LMotor.run(speed)
        self.RMotor.run(speed)
        self.MMotor.track_target(self.angle)
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
        if len(self.memory) == 200:
            self.memory.pop(0)
        self.memory.append(self.angle)

    def isTurning(self) -> list[bool, int]:
        # Not working
        averageAngle = 0
        for i in self.memory:
            averageAngle += i
        averageAngle /= len(self.memory)
        print(averageAngle)

    # Main loop
    def runRace(self) -> None:
        self.move(self.speed)
        self.Brick.screen.print(self.debug())

        # Not turning counterclockwise
        if self.MSensor.reflection() < 25:
            self.set_angle(1.7 * (25 - self.LSensor.reflection()))
        else:
            self.set_angle(5 * (25 - self.LSensor.reflection()))
    
    def debug(self) -> list:
        return [self.LSensor.reflection(), self.MSensor.reflection(), self.RSensor.reflection()]
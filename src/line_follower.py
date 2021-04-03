from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.truck_module import Truck
import time
import logging


class Joystick:
    def __init__(self) -> None:
        super().__init__()

    def waitForCentralKeyPressed(self):
        pass


class LineSensor(object):
    def calibrate(self):
        pass

    def getTargetValue(self):
        return 0

    def getCurrentValue(self):
        return 0


class PidController:

    def __init__(self, target_value) -> None:
        self._target_value = target_value

    def getOutput(self, current_value):
        return 0


logging.basicConfig(level=logging.INFO)
joystick = Joystick()
joystick.waitForCentralKeyPressed()

line_sensor = LineSensor()
line_sensor.calibrate()
target_value = line_sensor.getTargetValue()
current_value = line_sensor.getCurrentValue()
pid_controller = PidController(target_value)
output = pid_controller.getOutput(current_value)

gpio = GpioWrapper()

leftMotor = LeftMotor(gpio)
rightMotor = RightMotor(gpio)

bot_truck = Truck(leftMotor, rightMotor)

speed_power = 10
'''
for speed_power in range(-100, 100, 10):
    bot_truck.setSpeedPower(speed_power)
    time.sleep(2)
'''

for i in range(1, 10):
    bot_truck.setTurnPower(30)
    time.sleep(0.87)
    bot_truck.stop()
    time.sleep(1)

    bot_truck.setSpeedPower(70)
    time.sleep(1)
    bot_truck.stop()
    time.sleep(2)


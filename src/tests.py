import logging

from alphabot.bot.hardware.gpio_module import GpioWrapper
from alphabot.bot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.bot.truck_module import Truck


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
gpio = GpioWrapper()
truck = Truck(LeftMotor(gpio), RightMotor(gpio))
#bot.turnRight90()
truck.turnLeft90()


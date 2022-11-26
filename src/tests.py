import logging

from alphabot.truck.hardware.gpio_module import GpioWrapper
from alphabot.truck.hardware.motor_module import LeftMotor, RightMotor
from alphabot.truck.truck_module import Truck


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
gpio = GpioWrapper()
truck = Truck(LeftMotor(gpio), RightMotor(gpio))
#truck.turnRight90()
truck.turnLeft90()


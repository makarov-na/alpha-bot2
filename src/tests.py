import logging
import time

from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.truck_module import Truck


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
gpio = GpioWrapper()
truck = Truck(LeftMotor(gpio), RightMotor(gpio))
#truck.turnRight90()
truck.turnLeft90()


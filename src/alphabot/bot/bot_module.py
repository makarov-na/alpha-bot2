from alphabot.bot.hardware.gpio_module import GpioWrapper
from alphabot.bot.hardware.line_sensor_module import LineSensor, LineSensorsAdc
from alphabot.bot.line_sensor_module import LineSensorNormalizer, LineSensorAvgFilter
from alphabot.bot.truck_module import Truck


class Bot:

    def __init__(self, gpio: GpioWrapper = None) -> None:
        self.truck: Truck = Truck(gpio)
        self.sensor: LineSensor = LineSensorNormalizer(LineSensorAvgFilter(LineSensorsAdc(gpio)))

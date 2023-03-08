from alphabot.bot.hardware.camera_module import CameraServo
from alphabot.bot.hardware.frontal_infrared_sensor_module import FrontalInfraredSensor
from alphabot.bot.hardware.gpio_module import GpioWrapper
from alphabot.bot.hardware.line_sensor_module import LineSensor, LineSensorsAdc
from alphabot.bot.line_sensor_module import LineSensorNormalizer, LineSensorAvgFilter
from alphabot.bot.truck_module import Truck


class Bot:

    def __init__(self, gpio: GpioWrapper = None) -> None:
        self.truck: Truck = Truck(gpio)
        self.line_sensor: LineSensor = LineSensorNormalizer(LineSensorAvgFilter(LineSensorsAdc(gpio)))
        self.frontal_sensor: FrontalInfraredSensor = FrontalInfraredSensor(gpio)
        self.camera_servo: CameraServo = CameraServo()

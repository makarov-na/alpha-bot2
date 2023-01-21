from alphabot.bot.hardware.gpio_module import GpioWrapper


class FrontalInfraredSensor:

    def __init__(self, gpio: GpioWrapper, leftSensorPin: int = 19, rightSensorPin: int = 16):
        self._leftSensorPin = leftSensorPin
        self._rightSensorPin = rightSensorPin
        self.gpio = gpio
        self.gpio.setup(self._leftSensorPin, gpio.IN, gpio.PUD_UP)
        self.gpio.setup(self._rightSensorPin, gpio.IN, gpio.PUD_UP)


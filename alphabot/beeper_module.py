import threading
from gpio_module import GpioWrapper


class Beeper:

    def __init__(self, gpio: GpioWrapper, soundPin: int = 4):
        self._soundPin = soundPin
        self.gpio = gpio
        self.gpio.setup(self._soundPin, gpio.OUT)

    def beepOn(self, timeInMilliseconds=None):
        self.gpio.output(self._soundPin, self.gpio.HIGH)
        if timeInMilliseconds is None:
            return
        timeInSeconds = timeInMilliseconds / 1000
        start_time = threading.Timer(timeInSeconds, self.beepOff)
        start_time.start()

    def beepOff(self):
        self.gpio.output(self._soundPin, self.gpio.LOW)

import threading
from gpio_module import GpioWrapper


class Beeper:

    def __init__(self, gpio=None, soundPin=4):
        if gpio is None:
            gpio = GpioWrapper()
        self._soundPin = soundPin
        self.gpio = gpio
        self.gpio.setup(self._soundPin, gpio.OUT)

    def beepOn(self, timeInSeconds=None):
        self.gpio.output(self._soundPin, self.gpio.HIGH)
        if timeInSeconds is None:
            return
        start_time = threading.Timer(timeInSeconds, self.beepOff)
        start_time.start()

    def beepOff(self):
        self.gpio.output(self._soundPin, self.gpio.LOW)

    def beepOn200mls(self):
        self.beepOn(0.2)

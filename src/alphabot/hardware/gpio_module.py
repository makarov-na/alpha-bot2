import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    logging.exception("Can't import GPIO")
    pass


class GpioWrapper:

    def __init__(self):
        self.LOW = GPIO.LOW
        self.HIGH = GPIO.HIGH
        self.OUT = GPIO.OUT
        self.IN = GPIO.IN
        self.PUD_UP = GPIO.PUD_UP
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def setup(self, pin, mode, pull_up_down=None):
        self
        if pull_up_down is None:
            GPIO.setup(pin, mode)
            return
        GPIO.setup(pin, mode, pull_up_down)

    def output(self, pin, value):
        self
        GPIO.output(pin, value)

    def createPwm(self, pin, frequency):
        self
        return GPIO.PWM(pin, frequency)

    def input(self, pin):
        self
        return GPIO.input(pin)

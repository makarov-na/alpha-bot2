try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class GpioWrapper:

    def __init__(self):
        self.LOW = GPIO.LOW
        self.HIGH = GPIO.HIGH
        self.OUT = GPIO.OUT
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def setup(self, pin, mode):
        self
        GPIO.setup(pin, mode)

    def output(self, pin, value):
        self
        GPIO.output(pin, value)

    def createPwm(self, pin, frequency):
        self
        return GPIO.PWM(pin, frequency)

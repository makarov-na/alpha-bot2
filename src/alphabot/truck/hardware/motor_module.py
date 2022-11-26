from alphabot.truck.hardware.gpio_module import GpioWrapper


class Motor:
    _PWM_FREQUENCY = 500
    _INITIAL_POWER_PERCENT = 0
    MAX_VALUE = 100
    MIN_VALUE = 0

    def __init__(self, gpio: GpioWrapper, forwardDirectionPin: int, backwardDirectionPin: int, powerPin: int):
        self._gpio = gpio
        self._forwardDirectionPin = forwardDirectionPin
        self._backwardDirectionPin = backwardDirectionPin
        self._pwmPin = powerPin
        self._dutyCycle = Motor._INITIAL_POWER_PERCENT
        self._gpio.setup(self._forwardDirectionPin, self._gpio.OUT)
        self._gpio.setup(self._backwardDirectionPin, self._gpio.OUT)
        self._gpio.setup(self._pwmPin, self._gpio.OUT)
        self._pwm = self._gpio.createPwm(self._pwmPin, self._PWM_FREQUENCY)
        self._pwm.start(self._dutyCycle)
        self.stop()

    def stop(self):
        self._pwm.ChangeDutyCycle(0)
        self._gpio.output(self._forwardDirectionPin, self._gpio.LOW)
        self._gpio.output(self._backwardDirectionPin, self._gpio.LOW)

    def forward(self, percents=None):
        if percents is None:
            percents = self._dutyCycle
        self._setPower(percents)
        self._gpio.output(self._forwardDirectionPin, self._gpio.LOW)
        self._gpio.output(self._backwardDirectionPin, self._gpio.HIGH)

    def backward(self, percents=None):
        if percents is None:
            percents = self._dutyCycle
        self._setPower(percents)
        self._gpio.output(self._forwardDirectionPin, self._gpio.HIGH)
        self._gpio.output(self._backwardDirectionPin, self._gpio.LOW)

    def _setPower(self, percents):
        if percents < 0 or percents > Motor.MAX_VALUE:
            raise Exception("Power value must be from {} to {}".format(Motor.MIN_VALUE, Motor.MAX_VALUE))
        self._dutyCycle = percents
        self._pwm.ChangeDutyCycle(self._dutyCycle)


class LeftMotor(Motor):

    def __init__(self, gpio):
        super(LeftMotor, self).__init__(gpio, 12, 13, 6)


class RightMotor(Motor):

    def __init__(self, gpio):
        super(RightMotor, self).__init__(gpio, 20, 21, 26)

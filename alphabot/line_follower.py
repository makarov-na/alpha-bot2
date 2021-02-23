import time
from beeper_module import Beeper
from gpio_module import GpioWrapper


class Motor:
    _PWM_FREQUENCY = 500

    def __init__(self, gpio, ain1, ain2, ena):
        self._gpio = gpio
        self._forwardDirectionPin = ain1
        self._backwardDirectionPin = ain2
        self._pwmPin = ena
        self._dutyCycle = 50
        self._gpio.setup(self._forwardDirectionPin, self._gpio.OUT)
        self._gpio.setup(self._backwardDirectionPin, self._gpio.OUT)
        self._gpio.setup(self._pwmPin, self._gpio.OUT)
        self.pwm = self._gpio.createPwm(self._pwmPin, self._PWM_FREQUENCY)
        self.pwm.start(self._dutyCycle)
        self.stop()

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        self._gpio.output(self._forwardDirectionPin, self._gpio.LOW)
        self._gpio.output(self._backwardDirectionPin, self._gpio.LOW)

    def forward(self):
        self.pwm.ChangeDutyCycle(self._dutyCycle)
        self._gpio.output(self._forwardDirectionPin, self._gpio.LOW)
        self._gpio.output(self._backwardDirectionPin, self._gpio.HIGH)

    def backward(self):
        self.pwm.ChangeDutyCycle(self._dutyCycle)
        self._gpio.output(self._forwardDirectionPin, self._gpio.HIGH)
        self._gpio.output(self._backwardDirectionPin, self._gpio.LOW)

    def setSpeed(self, value):
        self._dutyCycle = value
        self.pwm.ChangeDutyCycle(self._dutyCycle)


class LeftMotor(Motor):

    def __init__(self, gpio):
        super(LeftMotor, self).__init__(gpio, 12, 13, 6)


class RightMotor(Motor):

    def __init__(self, gpio):
        super(RightMotor, self).__init__(gpio, 20, 21, 26)


leftMotor = LeftMotor(GpioWrapper())
rightMotor = RightMotor(GpioWrapper())
beeper = Beeper()

print("forward")
leftMotor.forward()
rightMotor.forward()
time.sleep(2)

for speed in range(0, 100, 10):
    beeper.beepOn200mls()
    leftMotor.setSpeed(speed)
    time.sleep(3)

leftMotor.stop()
rightMotor.stop()

while True:
    time.sleep(1)

import time

from alphabot.bot.hardware.gpio_module import GpioWrapper
from alphabot.bot.hardware.motor_module import Motor, LeftMotor, RightMotor
import logging


class Truck:
    STOP_POWER_FACTOR = 2
    STOP_POWER_ONE_WHEEL_FACTOR = 2.5
    POWER_STOP_DURATION = 0.2

    def __init__(self, gpio: GpioWrapper = None, left_motor: Motor = None, right_motor: Motor = None) -> None:
        self._logger = logging.getLogger(__name__)
        if left_motor is None:
            self._left_motor = LeftMotor(gpio)
        else:
            self._left_motor = left_motor

        if right_motor is None:
            self._right_motor = RightMotor(gpio)
        else:
            self._right_motor = right_motor
        self._speed_power = 0
        self._rotation_power = 0

    def setSpeedPower(self, speed_power):
        if abs(speed_power) > Motor.MAX_VALUE:
            raise Exception("Power value must be between {} to {}".format(-Motor.MAX_VALUE, Motor.MAX_VALUE))
        self._speed_power = speed_power
        self._sendOutputToMotors()

    def setTurnPower(self, turn_power):
        if abs(turn_power) > Motor.MAX_VALUE:
            raise Exception("Power value must be between {} to {}. Actual value {}".format(-Motor.MAX_VALUE, Motor.MAX_VALUE, turn_power))
        self._rotation_power = turn_power
        self._sendOutputToMotors()

    def _motorsOff(self):
        self._rotation_power = 0
        self._speed_power = 0
        self._sendOutputToMotors()

    def stop(self):
        self._rotation_power = 0
        if self._speed_power * Truck.STOP_POWER_FACTOR <= Motor.MAX_VALUE:
            self._speed_power = -abs(self._speed_power) * Truck.STOP_POWER_FACTOR
        else:
            self._speed_power = - Motor.MAX_VALUE

        self._sendOutputToMotors()
        self._waitForPowerStop()
        self._motorsOff()

    def powerStopRight(self):
        power = self._speed_power * Truck.STOP_POWER_ONE_WHEEL_FACTOR
        if power > Motor.MAX_VALUE:
            power = Motor.MAX_VALUE
        self._motorsOff()
        self._right_motor.backward(power)
        self._waitForPowerStop()
        self._motorsOff()

    def powerStopLeft(self):
        power = self._speed_power * Truck.STOP_POWER_ONE_WHEEL_FACTOR
        if power > Motor.MAX_VALUE:
            power = Motor.MAX_VALUE
        self._motorsOff()
        self._left_motor.backward(power)
        self._waitForPowerStop()
        self._motorsOff()

    def _waitForPowerStop(self):
        # TODO make duration calculation based on current speed
        time.sleep(Truck.POWER_STOP_DURATION)

    def rotateAroundRightWheel(self, turn_power):
        self._right_motor.stop()
        self._left_motor.forward(turn_power)

    def rotateAroundLeftWheel(self, turn_power):
        self._left_motor.stop()
        self._right_motor.forward(turn_power)

    def _sendOutputToMotors(self):

        if self._speed_power == 0 and self._rotation_power == 0:
            self._logger.info("left motor = {} right motor = {}".format(0, 0))
            self._left_motor.stop()
            self._right_motor.stop()
            return

        left_motor_power, right_motor_power = self._calculateMotorsPower()

        if self._speed_power == 0 and self._rotation_power > 0:
            self._logger.info("left motor = {} right motor = {}".format(left_motor_power, right_motor_power))
            self._left_motor.forward(left_motor_power)
            self._right_motor.backward(right_motor_power)
            return

        if self._speed_power == 0 and self._rotation_power < 0:
            self._logger.info("left motor = {} right motor = {}".format(left_motor_power, right_motor_power))
            self._left_motor.backward(left_motor_power)
            self._right_motor.forward(right_motor_power)
            return

        if self._rotation_power < 0:
            left_motor_power, right_motor_power = self._swapValues(left_motor_power, right_motor_power)

        if self._speed_power > 0:
            self._logger.info("left motor = {} right motor = {}".format(left_motor_power, right_motor_power))
            self._left_motor.forward(left_motor_power)
            self._right_motor.forward(right_motor_power)
            return

        if self._speed_power < 0:
            self._logger.info("left motor = {} right motor = {}".format(left_motor_power, right_motor_power))
            self._left_motor.backward(left_motor_power)
            self._right_motor.backward(right_motor_power)
            return

    def _calculateMotorsPower(self):
        motor_one_power = abs(self._speed_power)
        motor_two_power = abs(self._speed_power)
        if self._speed_power == 0:
            motor_one_power = abs(self._rotation_power) / 2
            motor_two_power = motor_one_power
            return motor_one_power, motor_two_power
        if self._rotation_power != 0:
            motor_one_power = abs(self._speed_power) + abs(self._rotation_power)
            if motor_one_power > Motor.MAX_VALUE:
                motor_two_power = abs(self._speed_power) - (motor_one_power - Motor.MAX_VALUE)
                motor_one_power = Motor.MAX_VALUE
            if motor_two_power < Motor.MIN_VALUE:
                motor_two_power = Motor.MIN_VALUE
        return motor_one_power, motor_two_power

    def _swapValues(self, left_motor_power, right_motor_power):
        return right_motor_power, left_motor_power

    def getSpeedPower(self):
        return self._speed_power

    def getTurnPower(self):
        return self._rotation_power

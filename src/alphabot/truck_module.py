import time

from alphabot.hardware.motor_module import Motor
import logging


class Truck:
    # TODO Values must be calculated in calibration process
    NINETY_DEGREE_RIGHT_TURN_TIME = 0.3
    NINETY_DEGREE_LEFT_TURN_TIME = 0.35
    NINETY_DEGREE_TURN_POWER = 50

    def __init__(self, left_motor: Motor, right_motor: Motor) -> None:
        self._logger = logging.getLogger(__name__)
        self._left_motor = left_motor
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

    def stop(self):
        self._rotation_power = 0
        self._speed_power = 0
        self._sendOutputToMotors()

    def turnLeft90(self):
        self._rotation_power = -Truck.NINETY_DEGREE_TURN_POWER
        self._sendOutputToMotors()
        time.sleep(Truck.NINETY_DEGREE_LEFT_TURN_TIME)
        self._rotation_power = 0

    def turnRight90(self):
        self._rotation_power = Truck.NINETY_DEGREE_TURN_POWER
        self._sendOutputToMotors()
        time.sleep(Truck.NINETY_DEGREE_RIGHT_TURN_TIME)
        self._rotation_power = 0

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

    def rotateAroundRightWheel(self, turn_power):
        self._right_motor.stop();
        self._left_motor.forward(turn_power)

    def rotateAroundLeftWheel(self, turn_power):
        self._left_motor.stop();
        self._right_motor.forward(turn_power)

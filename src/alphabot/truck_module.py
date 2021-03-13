from alphabot.hardware.motor_module import Motor


class Truck:

    def __init__(self, left_motor: Motor, right_motor: Motor) -> None:
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._speed_power = 0
        self._rotation_power = 0

    def setSpeedPower(self, speed_power):
        self._speed_power = speed_power
        self.applyModel()

    def setTurnPower(self, turn_power):
        self._rotation_power = turn_power
        self.applyModel()

    def applyModel(self):

        if self._speed_power > 0:
            left_motor_power = self._speed_power
            right_motor_power = self._speed_power
            if self._rotation_power > 0:
                left_motor_power = self._speed_power + self._rotation_power
                if left_motor_power > Motor.MAX_VALUE:
                    right_motor_power = self._speed_power - (left_motor_power - Motor.MAX_VALUE)
                    left_motor_power = Motor.MAX_VALUE
                if right_motor_power < Motor.MIN_VALUE:
                    right_motor_power = Motor.MIN_VALUE
            if self._rotation_power < 0:
                right_motor_power = self._speed_power + (-self._rotation_power)
                if right_motor_power > Motor.MAX_VALUE:
                    left_motor_power = self._speed_power - (right_motor_power - Motor.MAX_VALUE)
                    right_motor_power = Motor.MAX_VALUE
                if left_motor_power < Motor.MIN_VALUE:
                    left_motor_power = Motor.MIN_VALUE
            self._left_motor.forward(left_motor_power)
            self._right_motor.forward(right_motor_power)
            return
        if self._speed_power < 0:
            left_motor_power = -self._speed_power
            right_motor_power = -self._speed_power
            self._left_motor.backward(left_motor_power)
            self._right_motor.backward(right_motor_power)
            return
        self._left_motor.stop()
        self._right_motor.stop()

    def stop(self):
        pass


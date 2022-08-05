from typing import List

from alphabot.pid_module import PidController


class PidTurnPowerCalculator:

    def __init__(self, KP, KI, KD, TARGET_VALUE_LEFT, TARGET_VALUE_RIGHT, MAX_OUT) -> None:
        self._left_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_LEFT, MAX_OUT)
        self._right_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_RIGHT, MAX_OUT)

    def calculateTurnPower(self, delta_time: float, all_sensors_values: List) -> int:
        left_sensor_value = all_sensors_values[1]
        right_sensor_value = all_sensors_values[3]
        left_sensor_pid_out = self._left_sensor_pid.getOutput(left_sensor_value, delta_time)
        right_sensor_pid_out = self._right_sensor_pid.getOutput(right_sensor_value, delta_time)

        if left_sensor_pid_out is None or right_sensor_pid_out is None:
            return 0

        if left_sensor_pid_out < 0 and right_sensor_pid_out < 0:
            if left_sensor_pid_out < right_sensor_pid_out:
                right_sensor_pid_out = 0
            elif right_sensor_pid_out < left_sensor_pid_out:
                left_sensor_pid_out = 0

        if left_sensor_pid_out < 0:
            return -left_sensor_pid_out

        if right_sensor_pid_out < 0:
            return right_sensor_pid_out

        return 0

    def getTelemetryData(self):
        return {
            'lp': self._left_sensor_pid.getTelemetryData(),
            'rp': self._right_sensor_pid.getTelemetryData()
        }

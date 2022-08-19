from typing import List

from alphabot.pid_module import PidController


class PidTurnPowerCalculator:

    def __init__(self, KP, KI, KD, TARGET_VALUE_LEFT, TARGET_VALUE_RIGHT, MAX_OUT) -> None:
        self._left_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_LEFT, MAX_OUT)
        self._right_sensor_pid = PidController(KP, KI, KD, TARGET_VALUE_RIGHT, MAX_OUT)
        self._left_sensor_pid_out = None
        self._right_sensor_pid_out = None

    def calculateTurnPower(self, delta_time: float, all_sensors_values: List) -> None:
        left_value_three_sensors = all_sensors_values[1] + all_sensors_values[2] + 100 - all_sensors_values[0]
        right_value_three_sensors = all_sensors_values[3] + all_sensors_values[2] + 100 - all_sensors_values[4]
        self._left_sensor_pid_out = self._left_sensor_pid.getOutput(left_value_three_sensors, delta_time)
        self._right_sensor_pid_out = self._right_sensor_pid.getOutput(right_value_three_sensors, delta_time)

    def getLeftPidOut(self):
        return -self._left_sensor_pid_out

    def getRightPidOut(self):
        return self._right_sensor_pid_out

    def getTelemetryData(self):
        return {
            'lp': self._left_sensor_pid.getTelemetryData(),
            'rp': self._right_sensor_pid.getTelemetryData()
        }

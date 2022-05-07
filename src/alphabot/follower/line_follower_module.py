from typing import List

from alphabot.follower.line_sensor_module import LineSensorNormalizer, LineSensorFilter
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc, LineSensor
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.pid_module import PidController
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.truck_module import Truck
import time
import logging


class LineFollowerConfig:
    def __init__(self) -> None:
        self.KP = 0.3
        self.KD = 20
        self.KI = 0
        self.MAX_OUT = 40
        self.SPEED_POWER = 18
        self.SLEEP_TIME = 1 / 1_000_000 * 10
        self.TARGET_VALUE_LEFT = 0
        self.TARGET_VALUE_RIGHT = 0
        self.black_level = range(0, 21)
        self.white_level = range(80, 101)


class LineFollower:

    def __init__(self, config: LineFollowerConfig = LineFollowerConfig(), gpio: GpioWrapper = None):
        self._cfg = config
        self._sensor: LineSensor = LineSensorNormalizer(LineSensorFilter(LineSensorsAdc(gpio)))
        self._logger = logging.getLogger(__name__)
        self._speed_power = config.SPEED_POWER
        self._sleep_time = config.SLEEP_TIME
        self._left_sensor_pid = PidController(config.KP, config.KI, config.KD, config.TARGET_VALUE_LEFT, config.MAX_OUT)
        self._right_sensor_pid = PidController(config.KP, config.KI, config.KD, config.TARGET_VALUE_RIGHT, config.MAX_OUT)
        self._bot_truck = Truck(LeftMotor(gpio), RightMotor(gpio))
        self._telemetry = Telemetry()
        self._prevent_time_ns = None
        self._keep_following = False

    def startFollowing(self):
        self._sleepAndMeasureTime()
        self._keep_following = True
        while self._keep_following:
            delta_time = self._sleepAndMeasureTime()
            all_sensors_values = self._sensor.readSensors()
            self._doFollowingAlgorythm(all_sensors_values, delta_time)
        self._bot_truck.stop()

    def _doFollowingAlgorythm(self, all_sensors_values, delta_time):
        self._correctCourse(all_sensors_values, delta_time)
        self._sendTelemetry(all_sensors_values, delta_time)
        self._stopFollowingWhenBotIsOutOfLine(all_sensors_values)

    def _stopFollowingWhenBotIsOutOfLine(self, all_sensors_values: List):
        if self._isBotOutOfLine(all_sensors_values):
            self._keep_following = False

    def _correctCourse(self, all_sensors_values: List, delta_time):
        self._bot_truck.setSpeedPower(self._speed_power)
        self._bot_truck.setTurnPower(self._calculateTurnPower(delta_time, all_sensors_values))

    def _calculateTurnPower(self, delta_time: float, all_sensors_values: List):
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

    def _sleepAndMeasureTime(self):
        time.sleep(self._sleep_time)
        delta_time_ns = self._calculateDeltaTimeInNanos()
        if delta_time_ns is None:
            return None
        return self._to_ms(delta_time_ns)

    def _calculateDeltaTimeInNanos(self):
        current_time_ns = time.time_ns()
        if self._prevent_time_ns is None:
            self._prevent_time_ns = current_time_ns
            return None
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        return delta_time_ns

    def _to_ms(self, time_ns):
        return time_ns / 1_000_000

    def _to_mcs(self, time_ns):
        return time_ns / 1_000

    def _isBotOutOfLine(self, all_sensors_values):
        for value in all_sensors_values:
            if not self._isWhite(value):
                return False
        return True

    def _isWhite(self, value):
        return value in self._cfg.white_level

    def _isBlack(self, value):
        return value in self._cfg.black_level

    def _sendTelemetry(self, all_sensors_values, delta_time):
        self._telemetry.send(
            {
                'flv':
                    {
                        'tm': time.time_ns(),
                        'dt': delta_time,
                        'sns': all_sensors_values,
                        'sp': self._bot_truck.getSpeedPower(),
                        'tn': self._bot_truck.getTurnPower()
                    },
                'lp': self._left_sensor_pid.getTelemetryData(),
                'rp': self._right_sensor_pid.getTelemetryData()
            }
        )

    @property
    def logger(self):
        return self._logger

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

    def startFollowing(self):
        self._sleepAndMeasureTime()
        while True:
            delta_time = self._sleepAndMeasureTime()
            all_sensors_values = self._sensor.readSensors()

            if self._isBotOutOfline(all_sensors_values):
                self._bot_truck.stop()
                break

            self._correctCourse(delta_time, all_sensors_values)
            self._sendTelemetry(all_sensors_values, delta_time)

    def _correctCourse(self, delta_time: float, all_sensors_values: List):
        left_sensor_value = all_sensors_values[1]
        right_sensor_value = all_sensors_values[3]
        left_sensor_pid_out = self._left_sensor_pid.getOutput(left_sensor_value, delta_time)
        right_sensor_pid_out = self._right_sensor_pid.getOutput(right_sensor_value, delta_time)

        self._bot_truck.setSpeedPower(self._speed_power)

        if left_sensor_pid_out is None or right_sensor_pid_out is None:
            return

        if left_sensor_pid_out < 0 and right_sensor_pid_out < 0:
            if left_sensor_pid_out < right_sensor_pid_out:
                right_sensor_pid_out = 0
            elif right_sensor_pid_out < left_sensor_pid_out:
                left_sensor_pid_out = 0

        if left_sensor_pid_out < 0:
            self._bot_truck.setTurnPower(-left_sensor_pid_out)
            return

        if right_sensor_pid_out < 0:
            self._bot_truck.setTurnPower(right_sensor_pid_out)
            return

        self._bot_truck.setTurnPower(0)

    def _sleepAndMeasureTime(self):
        time.sleep(self._sleep_time)
        delta_time_ns = self._calculateDeltaTimeInNanos()
        return self.to_ms(delta_time_ns)

    def _calculateDeltaTimeInNanos(self):
        current_time_ns = time.time_ns()
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        return delta_time_ns

    def to_ms(self, time_ns):
        return time_ns / 1_000_000

    def to_mcs(self, time_ns):
        return time_ns / 1_000

    def _isBotOutOfline(self, all_sensors_values):
        for value in all_sensors_values:
            if value not in self._cfg.white_level:
                return False
        return True

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

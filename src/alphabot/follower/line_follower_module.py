import logging
import time
from typing import List

from alphabot.follower.line_sensor_module import LineSensorSoft
from alphabot.follower.pid_turn_power_calculator_module import PidTurnPowerCalculator
from alphabot.follower.pose_detector_module import PoseDetector
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.truck_module import Truck


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


class LineFollower:

    def __init__(self, config: LineFollowerConfig = LineFollowerConfig(), gpio: GpioWrapper = None):
        self._cfg = config
        self._pid_turn_power_calculator = PidTurnPowerCalculator(config.KP, config.KI, config.KD, config.TARGET_VALUE_LEFT, config.TARGET_VALUE_RIGHT, config.MAX_OUT)
        self._bot_truck = Truck(LeftMotor(gpio), RightMotor(gpio))
        self._sensor = LineSensorSoft(LineSensorsAdc(gpio))
        self._pose_detector = PoseDetector(self._sensor)
        self._logger = logging.getLogger(__name__)
        self._telemetry = Telemetry()
        self._speed_power = config.SPEED_POWER
        self._sleep_time = config.SLEEP_TIME
        self._prevent_time_ns = None
        self._keep_following = False

    def startFollowing(self):
        self._sleepAndMeasureTime()
        self._keep_following = True
        while self._keep_following:
            delta_time = self._sleepAndMeasureTime()
            all_sensors_values = self._sensor.readSensors()
            self._doFollowingAlgorithm(all_sensors_values, delta_time)
            self._sendTelemetry(all_sensors_values, delta_time)
        self._bot_truck.stop()

    def _doFollowingAlgorithm(self, all_sensors_values, delta_time):
        self._pose_detector.appendSensorValues(all_sensors_values)
        if self._pose_detector.isBotExactlyOnLine():
            self._correctCourse(all_sensors_values, delta_time)
        elif self._pose_detector.isBotPartlyOnLine():
            if self._pose_detector.isOnRightCorner():
                self._handleBotIsOnRightCorner()
        elif self._pose_detector.isBotOutOfLine():
            self._handleBotIsOutOfLine()

    def _handleBotIsOnRightCorner(self):
        if not self._pose_detector.isOnRightCorner():
            return
        # TODO replace for more common algorithm without timings
        time.sleep(0.1)
        self._bot_truck.stop()
        if self._pose_detector.isBotOnLeftTurn():
            self._bot_truck.turnLeft90()
        else:
            self._bot_truck.turnRight90()
        self._bot_truck.setSpeedPower(20)
        time.sleep(0.05)

    def _handleBotIsOutOfLine(self):
        self._keep_following = False

    def _correctCourse(self, all_sensors_values: List, delta_time):
        self._bot_truck.setSpeedPower(self._speed_power)
        self._bot_truck.setTurnPower(self._pid_turn_power_calculator.calculateTurnPower(delta_time, all_sensors_values))

    def _sleepAndMeasureTime(self):
        time.sleep(self._sleep_time)
        current_time_ns = time.time_ns()
        if self._prevent_time_ns is None:
            self._prevent_time_ns = current_time_ns
            return None
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        delta_time_ms = delta_time_ns / 1_000_000
        return delta_time_ms

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
                'pid': self._pid_turn_power_calculator.getTelemetryData()
            }
        )

    @property
    def logger(self):
        return self._logger

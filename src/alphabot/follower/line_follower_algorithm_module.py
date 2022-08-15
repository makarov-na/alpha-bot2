import time
from typing import List

from alphabot.follower.config_module import LineFollowerConfig
from alphabot.follower.pid_turn_power_calculator_module import PidTurnPowerCalculator
from alphabot.follower.pose_detector_module import PoseDetector


class LineFollowingAlgorithm:

    def __init__(self, bot_truck, config=LineFollowerConfig()) -> None:
        self._pid_turn_power_calculator = PidTurnPowerCalculator(config.KP, config.KI, config.KD, config.TARGET_VALUE_LEFT, config.TARGET_VALUE_RIGHT, config.MAX_OUT)
        self._pose_detector = PoseDetector()
        self._bot_truck = bot_truck
        self._speed_power = config.SPEED_POWER
        self._has_next_step = True

    def doFollowingAlgorithm(self, all_sensors_values, delta_time):
        self._pose_detector.appendSensorValues(all_sensors_values)
        if self._pose_detector.isBotOutOfLine():
            self._handleBotIsOutOfLine()
        elif self._pose_detector.isOnRightCorner():
            self._handleBotIsOnRightCorner()
        elif self._pose_detector.isBotPartlyOnLine():
            self._handleBotIsPartlyOnLine()
        elif self._pose_detector.isBotExactlyOnLine():
            self._correctCourse(all_sensors_values, delta_time)

    def _handleBotIsPartlyOnLine(self):
        self._bot_truck.setSpeedPower(0)
        if self._pose_detector.isBotRightToTheLine():
            self._bot_truck.setTurnPower(-20)
        else:
            self._bot_truck.setTurnPower(20)

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
        self._has_next_step = False

    def _correctCourse(self, all_sensors_values: List, delta_time):
        self._bot_truck.setSpeedPower(self._speed_power)
        self._bot_truck.setTurnPower(self._pid_turn_power_calculator.calculateTurnPower(delta_time, all_sensors_values))

    def getTelemetryData(self):
        return self._pid_turn_power_calculator.getTelemetryData()

    def hasNextStep(self):
        return self._has_next_step

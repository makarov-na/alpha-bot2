from typing import List

from alphabot.follower.config_module import LineFollowerConfig
from alphabot.follower.event.event_module import Event
from alphabot.follower.state.linefollow.pid_turn_power_calculator_module import PidTurnPowerCalculator
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.bot.truck_module import Truck


class LineFollowingAlgorithm:

    def __init__(self, bot_truck: Truck, config=LineFollowerConfig()) -> None:
        self._pid_turn_power_calculator = PidTurnPowerCalculator(config.KP, config.KI, config.KD, config.TARGET_VALUE_LEFT, config.TARGET_VALUE_RIGHT, config.MAX_OUT)
        self._bot_truck = bot_truck
        self._speed_power = config.SPEED_POWER
        self._prevent_time_ns = None

    def doAction(self, event: Event):
        if event.pose == Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS:
            self._bot_truck.setSpeedPower(self._speed_power * 1.2)
        elif event.pose == Pose.ON_LINE_WITH_CENTRAL_SENSOR:
            self._bot_truck.setSpeedPower(self._speed_power)
        elif event.pose == Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR:
            self._bot_truck.setSpeedPower(0)
        self._correctCourse(event.sensor_values, self._calculate_delta_time_ms(event.time_ns))

    def _correctCourse(self, all_sensors_values: List, delta_time):
        self._pid_turn_power_calculator.calculateTurnPower(delta_time, all_sensors_values)
        if self._isBotRightToTheLine(all_sensors_values):
            self._bot_truck.setTurnPower(self._pid_turn_power_calculator.getRightPidOut())
        else:
            self._bot_truck.setTurnPower(self._pid_turn_power_calculator.getLeftPidOut())

    def _isBotRightToTheLine(self, all_sensors_values):
        left_side_sensors_sum = all_sensors_values[0] + all_sensors_values[1]
        right_side_sensors_sum = all_sensors_values[3] + all_sensors_values[4]
        return right_side_sensors_sum > left_side_sensors_sum

    def getTelemetryData(self):
        return self._pid_turn_power_calculator.getTelemetryData()

    def _calculate_delta_time_ms(self, current_time_ns):
        if self._prevent_time_ns is None:
            self._prevent_time_ms = current_time_ns
            return 1
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        delta_time_ms = delta_time_ns / 1_000_000
        return delta_time_ms

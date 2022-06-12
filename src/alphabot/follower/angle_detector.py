from enum import Enum
from collections import deque

from alphabot.follower.line_sensor_module import LineSensorSoft


class SensorStatus(Enum):
    BLACK = 'X'
    WHITE = '_'
    MIDDLE = '|'


class RightAngleDetector:

    def __init__(self, line_sensor: LineSensorSoft) -> None:
        self._sensor = line_sensor
        self._left_turn_pattern = [[SensorStatus.MIDDLE, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.WHITE],
                                   [SensorStatus.MIDDLE, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.WHITE],
                                   [SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.WHITE]]
        self._right_turn_pattern = [[SensorStatus.WHITE, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.MIDDLE],
                                    [SensorStatus.WHITE, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.MIDDLE],
                                    [SensorStatus.WHITE, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK, SensorStatus.BLACK]]
        self._current_state = deque(maxlen=3)

    def appendSensorValues(self, all_sensors_values):
        current_line = []
        for curr_value in all_sensors_values:
            current_line.append(self._getStatus(curr_value))
        self._current_state.append(current_line)

    def isBotOnLeftTurn(self):
        if self._left_turn_pattern == list(self._current_state):
            return True
        return False

    def isBotOnRightTurn(self):
        if self._right_turn_pattern == list(self._current_state):
            return True
        return False

    def isOnRightCorner(self):
        return self.isBotOnRightTurn() or self.isBotOnLeftTurn()

    def _getStatus(self, curr_value):
        if self._sensor.isSensorOnBlack(curr_value):
            return SensorStatus.BLACK
        if self._sensor.isSensorOnWhite(curr_value):
            return SensorStatus.WHITE
        return SensorStatus.MIDDLE

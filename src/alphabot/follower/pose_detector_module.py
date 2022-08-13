from collections import deque
from enum import Enum

from alphabot.follower.line_sensor_module import LineSensorLevel


class SensorStatus(Enum):
    BLACK = 'X'
    WHITE = '_'
    MIDDLE = '|'


class PoseDetector:

    def __init__(self) -> None:

        self._sensor_level = LineSensorLevel()

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

    def isBotOutOfLine(self):
        if len(list(self._current_state)) == 0:
            return None
        for sensor in list(self._current_state)[len(list(self._current_state)) - 1]:
            if sensor != SensorStatus.WHITE:
                return False
        return True

    def isBotPartlyOnLine(self):
        if len(list(self._current_state)) == 0:
            return None
        for sensor in list(self._current_state)[len(list(self._current_state)) - 1]:
            if sensor in [SensorStatus.BLACK, SensorStatus.MIDDLE]:
                return True
        return False

    def isBotExactlyOnLine(self):
        if len(list(self._current_state)) == 0:
            return None
        last_sensors = list(self._current_state)[len(list(self._current_state)) - 1]
        return last_sensors[0] == SensorStatus.WHITE and last_sensors[4] == SensorStatus.WHITE and last_sensors[2] == SensorStatus.BLACK

    def _getStatus(self, curr_value):
        if self._sensor_level.isSensorOnBlack(curr_value):
            return SensorStatus.BLACK
        if self._sensor_level.isSensorOnWhite(curr_value):
            return SensorStatus.WHITE
        return SensorStatus.MIDDLE

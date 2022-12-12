from collections import deque
from enum import Enum, Flag, auto

from alphabot.bot.line_sensor_module import LineSensorLevel


class SensorStatus(Enum):
    BLACK = 'X'
    WHITE = '_'
    MIDDLE = '|'


class Pose(Flag):
    OUT_OF_LINE = auto()
    ON_LINE_WITH_TREE_CENTRAL_SENSORS = auto()
    ON_LINE_WITH_CENTRAL_SENSOR = auto()
    ON_LINE_WITHOUT_CENTRAL_SENSOR = auto()
    ON_LEFT_TURN = auto()
    ON_RIGHT_TURN = auto()


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
        self._current_state_raw = deque(maxlen=3)

    def getCurrentPose(self, all_sensors_values) -> Pose:
        self._appendSensorValues(all_sensors_values)
        if self._isBotOutOfLine():
            return Pose.OUT_OF_LINE
        elif self._isBotOnLeftTurn():
            return Pose.ON_LEFT_TURN
        elif self._isBotOnRightTurn():
            return Pose.ON_RIGHT_TURN
        elif self._isBotOnlineWithTreCentralSensors():
            return Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS
        elif self._isBotOnlineWithCentralSensor():
            return Pose.ON_LINE_WITH_CENTRAL_SENSOR
        elif self._isBotOnlineWithoutCentralSensor():
            return Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR
        raise Exception('Unknown pose')

    def _appendSensorValues(self, all_sensors_values):
        current_line = []
        for curr_value in all_sensors_values:
            current_line.append(self._getStatus(curr_value))
        self._current_state_raw.append(all_sensors_values)
        self._current_state.append(current_line)

    def _isBotOnLeftTurn(self):
        if self._left_turn_pattern == list(self._current_state):
            return True
        return False

    def _isBotOnRightTurn(self):
        if self._right_turn_pattern == list(self._current_state):
            return True
        return False

    def isOnRightCorner(self):
        return self._isBotOnRightTurn() or self._isBotOnLeftTurn()

    def _isBotOutOfLine(self):
        if len(list(self._current_state)) == 0:
            return None
        for sensor in self._getLastValues():
            if sensor != SensorStatus.WHITE:
                return False
        return True

    def _isBotOnlineWithoutCentralSensor(self):
        if len(list(self._current_state)) == 0:
            return None
        last_sensors = self._getLastValues()
        return last_sensors[2] == SensorStatus.WHITE and (
                (last_sensors[0] in [SensorStatus.BLACK, SensorStatus.MIDDLE]) or
                (last_sensors[1] in [SensorStatus.BLACK, SensorStatus.MIDDLE]) or
                (last_sensors[3] in [SensorStatus.BLACK, SensorStatus.MIDDLE]) or
                (last_sensors[4] in [SensorStatus.BLACK, SensorStatus.MIDDLE])
        )

    def _isBotOnlineWithCentralSensor(self):
        if len(list(self._current_state)) == 0:
            return None
        last_sensors = self._getLastValues()
        return last_sensors[2] in [SensorStatus.BLACK, SensorStatus.MIDDLE]

    def _isBotOnlineWithTreCentralSensors(self):
        if len(list(self._current_state)) == 0:
            return None
        last_sensors = self._getLastValues()
        return last_sensors[2] in [SensorStatus.BLACK] \
               and last_sensors[1] in [SensorStatus.BLACK, SensorStatus.MIDDLE] \
               and last_sensors[3] in [SensorStatus.BLACK, SensorStatus.MIDDLE]

    def _getLastValues(self):
        last_sensors = list(self._current_state)[len(list(self._current_state)) - 1]
        return last_sensors

    def _getStatus(self, curr_value):
        if self._sensor_level.isSensorOnBlack(curr_value):
            return SensorStatus.BLACK
        if self._sensor_level.isSensorOnWhite(curr_value):
            return SensorStatus.WHITE
        return SensorStatus.MIDDLE

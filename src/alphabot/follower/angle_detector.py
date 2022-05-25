from alphabot.follower.line_sensor_module import LineSensorSoft


class LeftTurnRightAngleDetector:

    def __init__(self, line_sensor: LineSensorSoft) -> None:
        self._sensor = line_sensor

    def isBotOnLeftTurn(self, all_sensors_values):
        return self._sensor.isSensorOnBlack(all_sensors_values[0]) and self._sensor.isSensorOnBlack(all_sensors_values[1]) and self._sensor.isSensorOnBlack(all_sensors_values[2])


class RightTurnRightAngleDetector:

    def __init__(self, line_sensor: LineSensorSoft) -> None:
        self._sensor = line_sensor

    def isBotOnRightTurn(self, all_sensors_values):
        return self._sensor.isSensorOnBlack(all_sensors_values[2]) and self._sensor.isSensorOnBlack(all_sensors_values[3]) and self._sensor.isSensorOnBlack(all_sensors_values[4])


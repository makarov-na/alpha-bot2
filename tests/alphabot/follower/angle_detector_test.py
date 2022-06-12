import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.angle_detector import RightAngleDetector
from alphabot.follower.line_sensor_module import LineSensorSoft


class TestAngleDetector(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    def test_bot_on_left_turn_true(self):
        # GIVEN
        angle_detector = RightAngleDetector(LineSensorSoft(MagicMock()))
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 0, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        angle_detector.appendSensorValues(all_sensor_values[0])
        angle_detector.appendSensorValues(all_sensor_values[0])
        angle_detector.appendSensorValues(all_sensor_values[0])
        result0 = angle_detector.isBotOnLeftTurn()
        angle_detector.appendSensorValues(all_sensor_values[1])
        result1 = angle_detector.isBotOnLeftTurn()
        angle_detector.appendSensorValues(all_sensor_values[2])
        result2 = angle_detector.isBotOnLeftTurn()

        # THEN
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertTrue(result2)

    def test_bot_on_left_turn_false_multiple(self):
        # GIVEN
        angle_detector = RightAngleDetector(LineSensorSoft(MagicMock()))
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 100, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        angle_detector.appendSensorValues(all_sensor_values[0])
        result0 = angle_detector.isBotOnLeftTurn()
        angle_detector.appendSensorValues(all_sensor_values[1])
        result1 = angle_detector.isBotOnLeftTurn()
        angle_detector.appendSensorValues(all_sensor_values[2])
        result2 = angle_detector.isBotOnLeftTurn()

        # THEN
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertFalse(result2)

    def test_bot_on_left_turn_false(self):
        # GIVEN
        angle_detector = RightAngleDetector(LineSensorSoft(MagicMock()))
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 0, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        angle_detector.appendSensorValues(all_sensor_values[0])
        result2 = angle_detector.isBotOnLeftTurn()

        # THEN
        self.assertFalse(result2)

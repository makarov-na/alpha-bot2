import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.pose_detector import PoseDetector
from alphabot.follower.line_sensor_module import LineSensorSoft


class TestAngleDetector(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    def test_bot_on_left_turn_true(self):
        # GIVEN
        angle_detector = PoseDetector(LineSensorSoft(MagicMock()))
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
        angle_detector = PoseDetector(LineSensorSoft(MagicMock()))
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
        angle_detector = PoseDetector(LineSensorSoft(MagicMock()))
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 0, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        angle_detector.appendSensorValues(all_sensor_values[0])
        result2 = angle_detector.isBotOnLeftTurn()

        # THEN
        self.assertFalse(result2)

    def test_bot_is_not_out_of_line_when_not_all_on_white(self):
        # GIVEN
        pose_detector = PoseDetector(LineSensorSoft(MagicMock()))
        sensor_values = [0, 1, 1, 1, 89]
        pose_detector.appendSensorValues(sensor_values)

        # WHEN
        result = pose_detector.isBotOutOfLine()

        # THEN
        self.assertFalse(result)

    def test_bot_is_out_of_line_when_all_on_white(self):
        # GIVEN
        pose_detector = PoseDetector(LineSensorSoft(MagicMock()))
        sensor_values = [90, 90, 90, 100, 100]
        pose_detector.appendSensorValues(sensor_values)

        # WHEN
        result = pose_detector.isBotOutOfLine()

        # THEN
        self.assertTrue(result)

    def test_is_bot_exactly_on_line(self):
        # GIVEN
        pose_detector = PoseDetector(LineSensorSoft(MagicMock()))
        all_sensor_values = [100, 0, 0, 0, 100]
        pose_detector.appendSensorValues(all_sensor_values)

        # WHEN
        result = pose_detector.isBotExactlyOnLine()

        # THEN
        self.assertTrue(result)

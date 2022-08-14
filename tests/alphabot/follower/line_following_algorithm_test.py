import asyncio
import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.line_follower_module import LineFollower, LineFollowingAlgorithm


class TestLineFollowingAlgorithmTest(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    def test_following_algorythm_contain_step_correct_course(self):
        # GIVEN
        line_follower = LineFollowingAlgorithm(bot_truck=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower.doFollowingAlgorithm([100, 0, 0, 0, 100], 0)

        # THEN
        line_follower._correctCourse.assert_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()
        line_follower._handleBotIsOutOfLine.assert_not_called()

    def test_following_algorythm_contain_step_out_of_line(self):
        # GIVEN
        line_follower = LineFollowingAlgorithm(bot_truck=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower.doFollowingAlgorithm([100, 100, 100, 100, 100], 0)

        # THEN
        line_follower._correctCourse.assert_not_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()
        line_follower._handleBotIsOutOfLine.assert_called()

    def test_handle_bot_on_right_corner_left(self):
        # GIVEN
        line_follower = LineFollowingAlgorithm(bot_truck=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 0, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        line_follower.doFollowingAlgorithm(all_sensor_values[0], 0)
        line_follower.doFollowingAlgorithm(all_sensor_values[1], 0)
        line_follower.doFollowingAlgorithm(all_sensor_values[2], 0)

        # THEN
        line_follower._bot_truck.turnLeft90.assert_called_once()
        line_follower._bot_truck.turnRight90.assert_not_called()

    def test_handle_bot_on_right_corner_right(self):
        # GIVEN
        line_follower = LineFollowingAlgorithm(bot_truck=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [[100, 0, 0, 0, 50], [100, 0, 0, 0, 50], [100, 0, 0, 0, 0]]

        # WHEN
        line_follower.doFollowingAlgorithm(all_sensor_values[0], 0)
        line_follower.doFollowingAlgorithm(all_sensor_values[1], 0)
        line_follower.doFollowingAlgorithm(all_sensor_values[2], 0)

        # THEN
        line_follower._bot_truck.turnRight90.assert_called_once()
        line_follower._bot_truck.turnLeft90.assert_not_called()

import asyncio
import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.line_follower_module import LineFollower


class TestLineFollower(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    def test_calculate_delta_time_ms_one_second(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        dt_ns = (1 * (10 ** 9))

        # WHEN
        time_ms = line_follower._to_ms(dt_ns)

        # THEN
        self.assertEqual(1000, time_ms)

    def test_calculate_delta_time_ms_150_mks(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        dt_ns = (154 * (10 ** 3))

        # WHEN
        time_ms = line_follower._to_ms(dt_ns)

        # THEN
        self.assertEqual(0.154, time_ms)

    def test_start_following_loop_and_exit_from_loop(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.stop = MagicMock()
        line_follower._sleepAndMeasureTime = MagicMock()
        line_follower._sleepAndMeasureTime.return_value = 11
        line_follower._sensor.readSensors = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._sensor.readSensors.return_value = [1, 2, 3, 4, 5]
        loop = asyncio.get_event_loop()

        async def startFollowing():
            await loop.run_in_executor(None, line_follower.startFollowing)

        async def stopFollowing():
            while True:
                if line_follower._keep_following is True:
                    line_follower._keep_following = False
                    return
                await asyncio.sleep(0)

        # WHEN
        loop.run_until_complete(asyncio.gather(startFollowing(), stopFollowing()))

        # THEN
        line_follower._bot_truck.stop.assert_called()
        line_follower._sensor.readSensors.assert_called()
        line_follower._sleepAndMeasureTime.assert_called()
        line_follower._sendTelemetry.assert_called()

    def test_following_algorythm_contain_step_correct_course(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower._doFollowingAlgorithm([100, 0, 0, 0, 100], 0)

        # THEN
        line_follower._correctCourse.assert_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()
        line_follower._handleBotIsOutOfLine.assert_not_called()

    def test_following_algorythm_contain_step_correct_angle(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower._doFollowingAlgorithm([0, 0, 0, 0, 100], 0)

        # THEN
        line_follower._correctCourse.assert_not_called()
        line_follower._handleBotIsOnRightCorner.assert_called()
        line_follower._handleBotIsOutOfLine.assert_not_called()


    def test_following_algorythm_contain_step_out_of_line(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower._doFollowingAlgorithm([100, 100, 100, 100, 100], 0)

        # THEN
        line_follower._correctCourse.assert_not_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()
        line_follower._handleBotIsOutOfLine.assert_called()

    def test_handle_bot_on_right_corner_left(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [[50, 0, 0, 0, 100], [50, 0, 0, 0, 100], [0, 0, 0, 0, 100]]

        # WHEN
        line_follower._doFollowingAlgorithm(all_sensor_values[0], 0)
        line_follower._doFollowingAlgorithm(all_sensor_values[1], 0)
        line_follower._doFollowingAlgorithm(all_sensor_values[2], 0)

        # THEN
        line_follower._bot_truck.turnLeft90.assert_called_once()
        line_follower._bot_truck.turnRight90.assert_not_called()

    def test_handle_bot_on_right_corner_right(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [[100, 0, 0, 0, 50], [100, 0, 0, 0, 50], [100, 0, 0, 0, 0]]

        # WHEN
        line_follower._doFollowingAlgorithm(all_sensor_values[0], 0)
        line_follower._doFollowingAlgorithm(all_sensor_values[1], 0)
        line_follower._doFollowingAlgorithm(all_sensor_values[2], 0)

        # THEN
        line_follower._bot_truck.turnRight90.assert_called_once()
        line_follower._bot_truck.turnLeft90.assert_not_called()

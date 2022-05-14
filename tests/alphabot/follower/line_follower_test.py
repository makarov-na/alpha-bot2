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

    def test_bot_is_not_out_of_line_when_not_all_on_white(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        sensor_values = [0, 1, 1, 1, 89]

        # WHEN
        result = line_follower._isBotOutOfLine(sensor_values)

        # THEN
        self.assertFalse(result)

    def test_bot_is_out_of_line_when_all_on_white(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        sensor_values = [90, 90, 90, 100, 100]

        # WHEN
        result = line_follower._isBotOutOfLine(sensor_values)

        # THEN
        self.assertTrue(result)

    def test_start_following_loop_and_exit_from_loop(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.stop = MagicMock()
        line_follower._sleepAndMeasureTime = MagicMock()
        line_follower._sleepAndMeasureTime.return_value = 11
        line_follower._sensor.readSensors = MagicMock()
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

    def test_following_algorythm_contain_steps(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()

        # WHEN
        line_follower._doFollowingAlgorythm([0, 0, 0, 0, 0], 0)

        # THEN
        line_follower._correctCourse.assert_called()
        line_follower._handleBotIsOnRightCorner.assert_called()
        line_follower._handleBotIsOutOfLine.assert_called()
        line_follower._sendTelemetry.assert_called()

    def test_is_bot_on_right_corner_left(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        all_sensor_values = [100, 100, 0, 0, 0]

        # WHEN
        result = line_follower._isBotOnRightCorner(all_sensor_values)

        # THEN
        self.assertTrue(result)

    def test_is_bot_on_left_corner_right(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        all_sensor_values = [0, 0, 0, 100, 100]

        # WHEN
        result = line_follower._isBotOnRightCorner(all_sensor_values)

        # THEN
        self.assertTrue(result)

    def test_is_bot_on_left_corner_false(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        all_sensor_values = [100, 0, 0, 0, 100]

        # WHEN
        result = line_follower._isBotOnRightCorner(all_sensor_values)

        # THEN
        self.assertFalse(result)

    def test_handle_bot_on_right_corner_left(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._isBotOnRightCorner = MagicMock()
        line_follower._isBotOnRightCorner = MagicMock()
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [0, 0, 0, 100, 100]

        # WHEN
        line_follower._handleBotIsOnRightCorner(all_sensor_values)

        # THEN
        line_follower._bot_truck.turnLeft90.assert_called_once()
        line_follower._bot_truck.turnRight90.assert_not_called()

    def test_handle_bot_on_right_corner_right(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._isBotOnRightCorner = MagicMock()
        line_follower._isBotOnRightCorner = MagicMock()
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        all_sensor_values = [100, 100, 0, 0, 0]

        # WHEN
        line_follower._handleBotIsOnRightCorner(all_sensor_values)

        # THEN
        line_follower._bot_truck.turnRight90.assert_called_once()
        line_follower._bot_truck.turnLeft90.assert_not_called()

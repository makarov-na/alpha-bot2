import unittest
import time
from unittest.mock import MagicMock

from alphabot.follower.line_follower_module import LineFollower


class TestLineFollower(unittest.TestCase):

    def test_calculate_delta_time_ms_one_second(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        dt_ns = (1 * (10 ** 9))

        # WHEN
        time_ms = line_follower.to_ms(dt_ns)

        # THEN
        self.assertEqual(1000, time_ms)

    def test_calculate_delta_time_ms_150_mks(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        dt_ns = (154 * (10 ** 3))

        # WHEN
        time_ms = line_follower.to_ms(dt_ns)

        # THEN
        self.assertEqual(0.154, time_ms)

    def test_all_in_white_negative(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        sensor_values = [0, 1, 1, 1, 89]

        # WHEN
        result = line_follower._isBotOutOfline(sensor_values)

        # THEN
        self.assertFalse(result)

    def test_all_in_white_positive(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        sensor_values = [90, 90, 90, 100, 100]

        # WHEN
        result = line_follower._isBotOutOfline(sensor_values)

        # THEN
        self.assertTrue(result)

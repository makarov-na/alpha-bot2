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

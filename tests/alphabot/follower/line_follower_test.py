import unittest
import time
from unittest.mock import MagicMock

from alphabot.follower.line_follower_module import LineFollower


class TestLineFollower(unittest.TestCase):

    def test_calculate_delta_time_ms(self):
        # GIVEN
        line_follower = LineFollower(gpio=MagicMock())
        line_follower._calculateDeltaTimeInMs()

        # WHEN
        time.sleep(0.01)
        dt1 = line_follower._calculateDeltaTimeInMs()

        time.sleep(0.01)
        dt2 = line_follower._calculateDeltaTimeInMs()

        # THEN
        self.assertEqual(0.01, dt1 / 1000)
        self.assertEqual(0.01, dt2 / 1000)

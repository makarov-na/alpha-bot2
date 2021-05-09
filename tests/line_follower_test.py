import unittest
import time
from unittest.mock import MagicMock

from line_follower import LineFollower


class TestLineFollower(unittest.TestCase):

    def test_calculate_delta_time(self):
        # GIVEN
        line_follower = LineFollower(MagicMock())
        line_follower._calculateDeltaTimeInMs()

        # WHEN
        time.sleep(0.01)
        dt1 = line_follower._calculateDeltaTimeInMs()

        time.sleep(0.01)
        dt2 = line_follower._calculateDeltaTimeInMs()

        # THEN
        self.assertEqual(0.01, dt1 / 1000)
        self.assertEqual(0.01, dt2 / 1000)

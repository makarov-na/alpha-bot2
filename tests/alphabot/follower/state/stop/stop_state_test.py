import unittest
from unittest.mock import MagicMock

from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.stop.stop_state_module import Stop


class TestState(unittest.TestCase):

    def test_stop_state(self):
        # GIVEN
        track = MagicMock()
        track.stop = MagicMock()
        state = Stop(track)

        # WHEN
        state = state.doAction(Event(Pose.ON_LINE_WITH_CENTRAL_SENSOR, [100, 0, 0, 0, 100]))

        # THEN
        self.assertIsInstance(state, Stop)
        track.stop.assert_called_once()

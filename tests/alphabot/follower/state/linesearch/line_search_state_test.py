import time
import unittest
from unittest.mock import MagicMock, call

from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.linefollow.line_follow_state_module import LineFollow
from alphabot.follower.state.linesearch.line_search_state_module import LineSearch
from alphabot.follower.state.stop.stop_state_module import Stop


class TestState(unittest.TestCase):

    def test_search_line_before_timeout_out_of_line(self):
        # GIVEN
        state = LineSearch(MagicMock())
        state._truck = MagicMock()
        state._truck.powerStop = MagicMock()
        state._truck.setTurnPower = MagicMock()
        state._createLineFollowerState = MagicMock()

        # WHEN
        outState = state.doAction(Event(Pose.OUT_OF_LINE, []))
        outState = state.doAction(Event(Pose.OUT_OF_LINE, []))

        # THEN
        self.assertEqual(outState, state)
        state._truck.powerStop.assert_called_once()
        state._truck.setTurnPower.assert_has_calls([call(state.TURN_POWER), call(state.TURN_POWER)])

    def test_search_line_after_timeout_out_of_line(self):
        # GIVEN
        state = LineSearch(MagicMock())
        state._init_time = time.time() - LineSearch.ACTION_TIMEOUT_SEC
        state._createStopState = MagicMock()
        state._createStopState.return_value = Stop(Event(Pose.OUT_OF_LINE, []))

        # WHEN
        outState = state.doAction(Event(Pose.OUT_OF_LINE, []))

        # THEN
        self.assertEqual(outState, state._createStopState.return_value)

    def test_search_line_before_timeout_on_line(self):
        # GIVEN
        state = LineSearch(MagicMock())
        state._createLineFollowerState = MagicMock()
        state._createLineFollowerState.return_value = LineFollow(Event(Pose.OUT_OF_LINE, []))

        # WHEN
        outState = state.doAction(Event(Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR, []))

        # THEN
        self.assertEqual(str(LineFollow(MagicMock()).__class__), str(outState.__class__))

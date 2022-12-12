import unittest
from unittest.mock import MagicMock

from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.init.init_state_module import Init
from alphabot.follower.state.linefollow.line_follow_state_module import LineFollow


class TestState(unittest.TestCase):

    def test_init_state_out_of_line(self):
        # GIVEN
        state = Init(MagicMock())
        state._createLineSearch = MagicMock()
        state._createLineSearch.return_value = MagicMock()

        # WHEN
        outState = state.doAction(Event(Pose.OUT_OF_LINE, []))

        # THEN
        self.assertEqual(outState, state._createLineSearch.return_value)

    def test_init_state_on_line(self):
        # GIVEN
        state = Init(MagicMock())

        # WHEN
        state = state.doAction(Event(Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS, [100, 0, 0, 0, 100]))
        # THEN
        self.assertIsInstance(state, LineFollow)

        # WHEN
        state = state.doAction(Event(Pose.ON_LINE_WITH_CENTRAL_SENSOR, [100, 0, 0, 0, 100]))
        # THEN
        self.assertIsInstance(state, LineFollow)

        # WHEN
        state = state.doAction(Event(Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR, [100, 0, 0, 0, 100]))
        # THEN
        self.assertIsInstance(state, LineFollow)

import unittest
from unittest.mock import MagicMock

from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.turnrightangle.turn_right_angle_state import TurnRightAngle


class TestState(unittest.TestCase):

    def test_turn_right_angle_state_out_of_line(self):
        # GIVEN
        truck = MagicMock()
        truck.stop = MagicMock()
        state = TurnRightAngle(truck)
        state._createLineSearch = MagicMock()
        state._createLineSearch.return_value = MagicMock()

        # WHEN
        outState = state.doAction(Event(Pose.OUT_OF_LINE, [100, 0, 0, 0, 100]))

        # THEN
        self.assertEqual(outState, state._createLineSearch.return_value)
        truck.powerStopLeft.assert_called_once()

    def test_turn_right_angle_state_on_line(self):
        # GIVEN
        truck = MagicMock()
        truck.stop = MagicMock()
        state = TurnRightAngle(truck)
        state._createLineFollow = MagicMock()
        state._createLineFollow.return_value = MagicMock()
        state._init_time_ns = 0

        # WHEN
        outState = state.doAction(Event(Pose.ON_LINE_WITH_CENTRAL_SENSOR, [100, 0, 0, 0, 100]))

        # THEN
        self.assertEqual(outState, state._createLineFollow.return_value)
        truck.powerStopLeft.assert_called_once()

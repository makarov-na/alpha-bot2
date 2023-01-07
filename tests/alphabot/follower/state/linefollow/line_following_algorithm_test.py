import time
import unittest
from unittest.mock import MagicMock

from alphabot.follower.event.event_module import Event
from alphabot.follower.state.linefollow.line_follow_state_module import LineFollow
from alphabot.follower.state.linefollow.line_follower_algorithm_module import LineFollowingAlgorithm
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.turnrightangle.turn_right_angle_state import TurnRightAngle


class TestLineFollowingAlgorithmTest(unittest.TestCase):

    def setUp(self) -> None:
        time.sleep = MagicMock()
        return

    def test_following_algorythm_contain_step_correct_course(self):
        # GIVEN
        line_follower = LineFollowingAlgorithm(bot_truck=MagicMock())
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        line_follower._handleBotIsOutOfLine = MagicMock()
        event = Event(Pose.ON_LINE_WITH_CENTRAL_SENSOR, [100, 0, 0, 0, 100])

        # WHEN
        line_follower.doAction(event)

        # THEN
        line_follower._correctCourse.assert_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()
        line_follower._handleBotIsOutOfLine.assert_not_called()

    def test_following_algorythm_contain_step_out_of_line(self):
        # GIVEN
        state = LineFollow(truck=MagicMock())
        line_follower = state._algorithm
        line_follower._bot_truck = MagicMock()
        line_follower._correctCourse = MagicMock()
        line_follower._sendTelemetry = MagicMock()
        line_follower._handleBotIsOnRightCorner = MagicMock()
        state._createLineSearchState = MagicMock()

        event = Event(Pose.OUT_OF_LINE, [100, 100, 100, 100, 100])

        # WHEN
        state.doAction(event)

        # THEN
        line_follower._correctCourse.assert_not_called()
        line_follower._handleBotIsOnRightCorner.assert_not_called()

    def test_handle_bot_on_right_corner_left(self):
        # GIVEN
        state = LineFollow(truck=MagicMock())
        line_follower = state._algorithm
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        events = [
            Event(Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS, [50, 0, 0, 0, 100]),
            Event(Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS, [50, 0, 0, 0, 100]),
            Event(Pose.ON_LEFT_TURN, [0, 0, 0, 0, 100])
        ]

        # WHEN
        state.doAction(events[0])
        state.doAction(events[1])
        result = state.doAction(events[2])

        # THEN
        self.assertIsInstance(result, TurnRightAngle)

    def test_handle_bot_on_right_corner_right(self):
        # GIVEN
        state = LineFollow(truck=MagicMock())
        line_follower = state._algorithm
        line_follower._bot_truck = MagicMock()
        line_follower._bot_truck.turnLeft90 = MagicMock()
        line_follower._bot_truck.turnRight90 = MagicMock()
        events = [
            Event(Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS, [100, 0, 0, 0, 50]),
            Event(Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS, [100, 0, 0, 0, 50]),
            Event(Pose.ON_RIGHT_TURN, [100, 0, 0, 0, 0])
        ]

        # WHEN
        state.doAction(events[0])
        state.doAction(events[1])
        result = state.doAction(events[2])

        # THEN
        self.assertIsInstance(result, TurnRightAngle)

    def test_bot_is_right_to_the_line(self):
        # GIVEN
        algorithm = LineFollowingAlgorithm(MagicMock())
        all_sensor_values = [0, 0, 0, 0, 100]

        # WHEN
        result = algorithm._isBotRightToTheLine(all_sensor_values)

        # THEN
        self.assertTrue(result)

    def test_bot_is_right_to_the_line_false(self):
        # GIVEN
        algorithm = LineFollowingAlgorithm(MagicMock())
        all_sensor_values = [100, 0, 0, 0, 0]

        # WHEN
        result = algorithm._isBotRightToTheLine(all_sensor_values)

        # THEN
        self.assertFalse(result)
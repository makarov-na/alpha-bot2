from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.base_state_module import State
from alphabot.follower.state.linefollow.line_follower_algorithm_module import LineFollowingAlgorithm
import alphabot.follower.state.turnrightangle.turn_right_angle_state as trnm
import alphabot.follower.state.linesearch.line_search_state_module as lnsm


class LineFollow(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._algorithm = LineFollowingAlgorithm(truck)

    def doAction(self, event: Event) -> State:
        if event.pose == Pose.OUT_OF_LINE:
            return lnsm.LineSearch(self._truck).doAction(event)
        if event.pose in [Pose.ON_RIGHT_TURN, Pose.ON_LEFT_TURN]:
            return trnm.TurnRightAngle(self._truck).doAction(event)
        self._algorithm.doAction(event)
        return self

import time

from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.base_state_module import State
import alphabot.follower.state.linefollow.line_follow_state_module as lnfm
import alphabot.follower.state.linesearch.line_search_state_module as lnsm


class TurnRightAngle(State):
    TRANSITION_TIMEOUT_NS = 200 * 1_000_000

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._start_pose = None
        self._turn_power = 40
        self._init_time_ns = time.time_ns()

    def doAction(self, event: Event) -> State:
        if self._start_pose is None:
            self._start_pose = event.pose
            if self._start_pose == Pose.ON_RIGHT_TURN:
                self._truck.powerStopRight()
            else:
                self._truck.powerStopLeft()
        if self._start_pose == Pose.ON_RIGHT_TURN:
            self._truck.rotateAroundRightWheel(self._turn_power)
        else:
            self._truck.rotateAroundLeftWheel(self._turn_power)

        if event.pose == Pose.OUT_OF_LINE:
            return self._createLineSearch(event)
        if event.pose == Pose.ON_LINE_WITH_CENTRAL_SENSOR and self.isTransitionProcessFinished():
            return self._createLineFollow(event)

        return self

    def isTransitionProcessFinished(self):
        return time.time_ns() - self._init_time_ns > TurnRightAngle.TRANSITION_TIMEOUT_NS

    def _createLineFollow(self, event):
        return lnfm.LineFollow(self._truck).doAction(event)

    def _createLineSearch(self, event):
        return lnsm.LineSearch(self._truck).doAction(event)

from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.base_state_module import State
import alphabot.follower.state.linefollow.line_follow_state_module as lnfm
import alphabot.follower.state.linesearch.line_search_state_module as lnsm


class TurnRightAngle(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._start_pose = None
        self._turn_power = 40

    def doAction(self, event: Event) -> State:
        if self._start_pose is None:
            self._start_pose = event.pose
            self._truck.powerStop()
        if event.pose == Pose.OUT_OF_LINE:
            return self._createLineSearch(event)
        if event.pose == Pose.ON_LINE_WITH_CENTRAL_SENSOR:
            return self._createLineFollow(event)
        if self._start_pose == Pose.ON_RIGHT_TURN:
            self._truck.rotateAroundRightWheel(self._turn_power)
        else:
            self._truck.rotateAroundLeftWheel(self._turn_power)
        return self

    def _createLineFollow(self, event):
        return lnfm.LineFollow(self._truck).doAction(event)

    def _createLineSearch(self, event):
        return lnsm.LineSearch(self._truck).doAction(event)

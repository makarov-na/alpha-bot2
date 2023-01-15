from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.base_state_module import State
import alphabot.follower.state.linefollow.line_follow_state_module as lnfm
import alphabot.follower.state.linesearch.line_search_state_module as lnsm


class Init(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck

    def doAction(self, event: Event) -> State:
        self._truck.stop()
        if event.pose == Pose.OUT_OF_LINE:
            return self._createLineSearch(event)
        return self._createLineFollow(event)

    def _createLineFollow(self, event):
        return lnfm.LineFollow(self._truck).doAction(event)

    def _createLineSearch(self, event):
        return lnsm.LineSearch(self._truck).doAction(event)

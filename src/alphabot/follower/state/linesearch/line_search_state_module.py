import time

from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.base_state_module import State
import alphabot.follower.state.stop.stop_state_module as stm
import alphabot.follower.state.linefollow.line_follow_state_module as lfm


class LineSearch(State):
    ACTION_TIMEOUT_SEC = 5
    TURN_POWER = 40

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._init_time = None

    def doAction(self, event: Event) -> State:
        if self._init_time is None:
            self._truck.powerStop()
            self._init_time = time.time()
        action_time = time.time() - self._init_time
        if action_time >= LineSearch.ACTION_TIMEOUT_SEC:
            return self._createStopState(event)
        if event.pose in (Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR, Pose.ON_LINE_WITH_CENTRAL_SENSOR):
            return self._createLineFollowerState(event)
        self._truck.setTurnPower(LineSearch.TURN_POWER)
        return self

    def _createLineFollowerState(self, event):
        return lfm.LineFollow(self._truck).doAction(event)

    def _createStopState(self, event):
        return stm.Stop(self._truck).doAction(event)

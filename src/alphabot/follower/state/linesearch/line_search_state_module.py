from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.state.base_state_module import State
import alphabot.follower.state.stop.stop_state_module as stm


class LineSearch(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._limit = 0

    def doAction(self, event: Event) -> State:
        if self._limit <= 0:
            return stm.Stop(self._truck).doAction(event)
        # TODO Search line logic with limits must be placed here
        return self

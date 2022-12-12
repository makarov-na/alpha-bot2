from alphabot.bot.truck_module import Truck
from alphabot.follower.event.event_module import Event
from alphabot.follower.state.base_state_module import State


class Stop(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck

    def doAction(self, event: Event) -> State:
        self._truck.stop()
        return self

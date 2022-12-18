from alphabot.follower.event.event_module import Event


class State:

    def doAction(self, event: Event) -> 'State':
        pass

    def __str__(self) -> str:
        return str(self.__class__).split(".").pop()[:-2]

from alphabot.follower.event.event_module import Event


class State:

    def doAction(self, event: Event) -> 'State':
        pass

from alphabot.follower.event_module import Event
from alphabot.follower.line_follower_algorithm_module import LineFollowingAlgorithm
from alphabot.follower.pose_detector_module import Pose
from alphabot.truck_module import Truck


class State:

    def doAction(self, event: Event) -> 'State':
        pass


class TurnRightAngle(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._start_pose = None

    def doAction(self, event: Event) -> State:
        if self._start_pose is None:
            self._start_pose = event.pose
            self._truck.stop()
        if event.pose == Pose.OUT_OF_LINE:
            return self._createLineSearch(event)
        if event.pose == Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS:
            return self._createLineFollow(event)
        if self._start_pose == Pose.ON_RIGHT_TURN:
            self._truck.rotateAroundRightWheel(20)
        else:
            self._truck.rotateAroundLeftWheel(20)
        return self

    def _createLineFollow(self, event):
        LineFollow(self._truck).doAction(event)

    def _createLineSearch(self, event):
        return LineSearch(self._truck).doAction(event)


class LineFollow(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._algorithm = LineFollowingAlgorithm(truck)

    def doAction(self, event: Event) -> State:
        if event.pose == Pose.OUT_OF_LINE:
            return LineSearch(self._truck).doAction(event)
        if event.pose in [Pose.ON_RIGHT_TURN, Pose.ON_LEFT_TURN]:
            return TurnRightAngle(self._truck).doAction(event)
        self._algorithm.doAction(event)
        return self


class Init(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck

    def doAction(self, event: Event) -> State:
        self._truck.stop()
        if event.pose == Pose.OUT_OF_LINE:
            return self._createLineSearch(event)
        return self._createLineFollow(event)

    def _createLineFollow(self, event):
        return LineFollow(self._truck).doAction(event)

    def _createLineSearch(self, event):
        return LineSearch(self._truck).doAction(event)


class LineSearch(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck
        self._limit = 0

    def doAction(self, event: Event) -> State:
        if self._limit <= 0:
            return Stop(self._truck).doAction(event)
        # TODO Search line logic with limits must be placed here
        return self


class Stop(State):

    def __init__(self, truck: Truck) -> None:
        self._truck = truck

    def doAction(self, event: Event) -> State:
        self._truck.stop()
        return self

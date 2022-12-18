import time
from typing import List

from alphabot.follower.pose.pose_detector_module import Pose


class Event:
    def __init__(self, pose: Pose, sensor_values: List):
        self.pose = pose
        self.time_ns = time.time_ns()
        self.sensor_values = sensor_values

    def __str__(self) -> str:
        return "Pose {} values {}".format(self.pose, self.sensor_values)

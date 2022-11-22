import logging
import time

from alphabot.follower.config_module import LineFollowerConfig
from alphabot.follower.event_module import Event
from alphabot.follower.line_sensor_module import LineSensorSoft
from alphabot.follower.pose_detector_module import PoseDetector
from alphabot.follower.state_module import Init
from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.line_sensor_module import LineSensorsAdc
from alphabot.hardware.motor_module import LeftMotor, RightMotor
from alphabot.telemetry.telemetry_module import Telemetry
from alphabot.truck_module import Truck


class LineFollower:

    def __init__(self, config: LineFollowerConfig = LineFollowerConfig(), gpio: GpioWrapper = None):
        self._cfg = config
        self._bot_truck = Truck(LeftMotor(gpio), RightMotor(gpio))
        self._sensor = LineSensorSoft(LineSensorsAdc(gpio))
        self._logger = logging.getLogger(__name__)
        self._telemetry = Telemetry()
        self._speed_power = config.SPEED_POWER
        self._sleep_time = config.SLEEP_TIME
        self._prevent_time_ns = None
        self._keep_following = True
        self._pose_detector = PoseDetector()
        self._current_state = Init(self._bot_truck)

    def startFollowing(self):
        while self._keep_following:
            dt = self._sleepAndMeasureTime()
            all_sensors_values = self._sensor.readSensors()
            pose = self._pose_detector.getCurrentPose(all_sensors_values)
            event = Event(pose, all_sensors_values)
            self._current_state = self._current_state.doAction(event)
            self._sendTelemetry(all_sensors_values, dt)

    def _sleepAndMeasureTime(self) -> int:
        time.sleep(self._sleep_time)
        current_time_ns = time.time_ns()
        if self._prevent_time_ns is None:
            self._prevent_time_ns = current_time_ns
            return None
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        delta_time_ms = delta_time_ns / 1_000_000
        return delta_time_ms

    def _sendTelemetry(self, all_sensors_values, delta_time):
        self._telemetry.send(
            {
                'flv':
                    {
                        'tm': time.time_ns(),
                        'dt': delta_time,
                        'sns': all_sensors_values,
                        'sp': self._bot_truck.getSpeedPower(),
                        'tn': self._bot_truck.getTurnPower()
                    },
                'pid': self.get_pid_data()
            }
        )

    def get_pid_data(self):
        # TODO real pid data  
        # return self._line_following_algorithm.getTelemetryData()
        return ''

    @property
    def logger(self):
        return self._logger

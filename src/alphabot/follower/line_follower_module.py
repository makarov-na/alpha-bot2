import logging
import time

from alphabot.bot.bot_module import Bot
from alphabot.bot.hardware.gpio_module import GpioWrapper
from alphabot.follower.config_module import LineFollowerConfig
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import PoseDetector, Pose
from alphabot.follower.state.init.init_state_module import Init
from alphabot.telemetry.telemetry_module import Telemetry


class LineFollower:

    def __init__(self, config: LineFollowerConfig = LineFollowerConfig(), gpio: GpioWrapper = None):
        self._bot = Bot(gpio)
        self._logger = logging.getLogger(__name__)
        self._telemetry = Telemetry()
        self._main_loop_sleep_time = config.SLEEP_TIME
        self._keep_following = True
        self._pose_detector = PoseDetector()
        self._current_state = Init(self._bot.truck)

    def startFollowing(self):
        while self._keep_following:
            all_sensors_values = self._bot.line_sensor.readSensors()
            event = Event(self._pose_detector.getCurrentPose(all_sensors_values), all_sensors_values)
            if event.pose == Pose.ON_T_INTERSECTION:
                event.pose = self._chooseTurn()
            self._current_state = self._current_state.doAction(event)
            self._sendTelemetry(event.sensor_values)
            time.sleep(self._main_loop_sleep_time)
            self._logger.info("current state = {} event = {}".format(self._current_state, event))

    def _chooseTurn(self):
        return Pose.ON_RIGHT_TURN

    def _sendTelemetry(self, all_sensors_values):
        self._telemetry.send(
            {
                'flv':
                    {
                        'tm': time.time_ns(),
                        'sns': all_sensors_values,
                        'sp': self._bot.truck.getSpeedPower(),
                        'tn': self._bot.truck.getTurnPower()
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

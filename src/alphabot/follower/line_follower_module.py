import logging
import time

import cv2

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
        self._USE_CAMERA_COURSE_CORRECTION = config.USE_CAMERA_COURSE_CORRECTION
        self._capture = cv2.VideoCapture(0)
        self._capture.set(3, 640)  # Set horizontal resolution
        self._capture.set(4, 480)  # Set vertical resolution
        success, frame = self._capture.read()

    def startFollowing(self):

        if self._USE_CAMERA_COURSE_CORRECTION:
            self._bot.camera_servo.setHorizontalPosition(0)
            self._bot.camera_servo.setVerticalPosition(-30)
            time.sleep(2)
            self._bot.camera_servo.stop_servos()

        while self._keep_following:
            all_sensors_values = self._bot.line_sensor.readSensors()
            pose = self._pose_detector.getCurrentPose(all_sensors_values)
            if pose == Pose.ON_T_INTERSECTION:
                event = Event(self._chooseTurn(), all_sensors_values)
            elif pose == Pose.OUT_OF_LINE:
                event = Event(pose, all_sensors_values, self._pose_detector.get_last_on_line_state())
            else:
                event = Event(pose, all_sensors_values)

            if self._USE_CAMERA_COURSE_CORRECTION:
                success, frame = self._capture.read()
                event.video_frame = frame

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
        return self._current_state.getTelemetryData()


    @property
    def logger(self):
        return self._logger

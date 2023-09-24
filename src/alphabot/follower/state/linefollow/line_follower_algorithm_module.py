import cv2

from alphabot.bot.truck_module import Truck
from alphabot.follower.config_module import LineFollowerConfig
from alphabot.follower.event.event_module import Event
from alphabot.follower.pose.pose_detector_module import Pose
from alphabot.follower.state.linefollow.pid_turn_power_calculator_module import PidTurnPowerCalculator
import logging


class LineFollowingAlgorithm:

    def __init__(self, bot_truck: Truck, config=LineFollowerConfig()) -> None:
        self._logger = logging.getLogger(__name__)
        self._pid_turn_power_calculator = PidTurnPowerCalculator(config.KP, config.KI, config.KD, config.TARGET_VALUE_LEFT, config.TARGET_VALUE_RIGHT, config.MAX_OUT)
        self._bot_truck = bot_truck
        self._speed_power = config.SPEED_POWER
        self._prevent_time_ns = None
        self._USE_CAMERA_COURSE_CORRECTION = config.USE_CAMERA_COURSE_CORRECTION
        self._stream = None

    def doAction(self, event: Event):
        if event.pose == Pose.ON_LINE_WITH_TREE_CENTRAL_SENSORS:
            self._bot_truck.setSpeedPower(self._speed_power * 1.2)
        elif event.pose == Pose.ON_LINE_WITH_CENTRAL_SENSOR:
            self._bot_truck.setSpeedPower(self._speed_power)
        elif event.pose == Pose.ON_LINE_WITHOUT_CENTRAL_SENSOR:
            self._bot_truck.setSpeedPower(0)
        self._correctCourse(event, self._calculate_delta_time_ms(event.time_ns))

    def _correctCourse(self, event: Event, delta_time):
        left_value, right_value, left_value_cam, right_value_cam = None, None, None, None
        left_value_sns, right_value_sns = self._calculateValuesBySensors(event.sensor_values)

        if self._USE_CAMERA_COURSE_CORRECTION:
            left_value_cam, right_value_cam = self._calculateValuesByFrame(event.video_frame)

        if self._USE_CAMERA_COURSE_CORRECTION and left_value_cam is not None:
            left_value, right_value = left_value_cam, right_value_cam
        else:
            left_value, right_value = left_value_sns, right_value_sns

        self._pid_turn_power_calculator.calculateTurnPower(delta_time, left_value, right_value)
        if self._isBotRightToTheLine(event.sensor_values):
            self._bot_truck.setTurnPower(self._pid_turn_power_calculator.getRightPidOut())
        else:
            self._bot_truck.setTurnPower(self._pid_turn_power_calculator.getLeftPidOut())

        self._logger.info("lsns={};lcam={};rsns={};rcam={};trnpwr={}".format(left_value_sns, left_value_cam, right_value_sns, right_value_cam, self._bot_truck.getTurnPower()))

    def _isBotRightToTheLine(self, all_sensors_values):
        left_side_sensors_sum = all_sensors_values[0] + all_sensors_values[1]
        right_side_sensors_sum = all_sensors_values[3] + all_sensors_values[4]
        return right_side_sensors_sum > left_side_sensors_sum

    def getTelemetryData(self):
        return self._pid_turn_power_calculator.getTelemetryData()

    def _calculate_delta_time_ms(self, current_time_ns: int) -> int:
        if self._prevent_time_ns is None:
            self._prevent_time_ns = current_time_ns
            return 1
        delta_time_ns = (current_time_ns - self._prevent_time_ns)
        self._prevent_time_ns = current_time_ns
        delta_time_ms = delta_time_ns / 1_000_000
        return delta_time_ms

    def _calculateValuesBySensors(self, all_sensors_values):
        left_value_three_sensors = all_sensors_values[1] + all_sensors_values[2] + 100 - all_sensors_values[0]
        right_value_three_sensors = all_sensors_values[3] + all_sensors_values[2] + 100 - all_sensors_values[4]
        return left_value_three_sensors, right_value_three_sensors

    def _calculateValuesByFrame(self, original_frame):

        scale_percent = 50
        frame_width = int(original_frame.shape[1] * scale_percent / 100)
        frame_height = int(original_frame.shape[0] * scale_percent / 100)
        resized_frame = cv2.resize(original_frame, (frame_width, frame_height))

        if (self._stream is None):
            dir = '/home/pi/tmp/'
            self._stream = cv2.VideoWriter(dir + 'resized_frame.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))

        # Переводим кадр в HSV, чтобы отфильтровать черный цвет. Цветовая фильтрация в RGB работает плохо.
        hsv_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)

        # Выбираем диапазон для фильтрации
        black_color_low = (0, 0, 0)
        black_color_high = (255, 255, 110)
        mask_for_black_colour = cv2.inRange(hsv_frame, black_color_low, black_color_high)

        # Вытравливаем мелкие элементы для устранения шума.
        erode_kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (50, 50))
        eroded_mask = mask_for_black_colour.copy()
        cv2.erode(mask_for_black_colour, erode_kernel, eroded_mask)

        # Выполняем заливку оставшихся элементов для устранения избыточного вытравливания
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (60, 60))
        dilated_mask = eroded_mask.copy()
        cv2.dilate(eroded_mask, dilate_kernel, dilated_mask)

        # Находим на маске контуры
        # Не возвращать вложенные контуры cv2.RETR_EXTERNAL
        contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) <= 0:
            return None, None
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)

        cv2.rectangle(resized_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        self._stream.write(resized_frame)

        left_value = int((x - (frame_width - (x + w))) / 2)
        right_value = - left_value

        if left_value < 0:
            left_value = 0
        if right_value < 0:
            right_value = 0

        return left_value, right_value

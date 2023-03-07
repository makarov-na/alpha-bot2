import math
import time

try:
    import smbus
except ImportError:
    import smbus2 as smbus


class CameraServo:
    SERVO_MOTOR_PWM_PERIOD_HZ = 50  # Servo motor datasheet
    VERTICAL_ZERO_PWM = 420  # Experimental found
    HORIZONTAL_ZERO_PWM = 317  # Experimental found
    HORIZONTAL_SERVO_CHANNEL = 0  # Alphabot 2PI schematic
    VERTICAL_SERVO_CHANNEL = 1  # Alphabot 2PI schematic
    __FIFTY_FIVE_DELTA_PWM = 107  # Experimental found
    __DEGREE_TO_PWM_COEFFICIENT = __FIFTY_FIVE_DELTA_PWM / 45

    def __init__(self, controller=None) -> None:
        if controller is None:
            self.controller = PCA9685()
        else:
            self.controller = controller
        self.controller.setPWMFreqHz(CameraServo.SERVO_MOTOR_PWM_PERIOD_HZ)

    def horizontal_position(self, degree):
        assert -45 <= degree <= 45, "Horizontal position must be between -45 and 45"
        self.controller.setPWM(CameraServo.HORIZONTAL_SERVO_CHANNEL, 0, CameraServo.HORIZONTAL_ZERO_PWM - round(degree * CameraServo.__DEGREE_TO_PWM_COEFFICIENT))

    def vertical_position(self, degree):
        assert -45 <= degree <= 45, "Vertical position must be between -45 and 45"
        self.controller.setPWM(CameraServo.VERTICAL_SERVO_CHANNEL, 0, CameraServo.VERTICAL_ZERO_PWM - round(degree * CameraServo.__DEGREE_TO_PWM_COEFFICIENT))

    def stop_servos(self):

        self.controller.setPWM(0, PCA9685.MAX_PWM_VALUE, 0)
        self.controller.setPWM(1, PCA9685.MAX_PWM_VALUE, 0)


class PCA9685:
    __CONTROLLER_ADDRESS = 0x40  # i2cdetect -y 1
    __INTERNAL_OSCILLATOR_CLOCK = 25000000  # 25MHz PCA9685 datasheet
    __MODE1 = 0x00  # PCA9685 datasheet
    __PRESCALE = 0xFE  # PCA9685 datasheet
    __LED0_ON_L = 0x06  # PCA9685 datasheet
    __LED0_ON_H = 0x07  # PCA9685 datasheet
    __LED0_OFF_L = 0x08  # PCA9685 datasheet
    __LED0_OFF_H = 0x09  # PCA9685 datasheet
    MAX_PWM_VALUE = 4096  # PCA9685 datasheet (12 bit)

    def __init__(self) -> None:
        self.bus = smbus.SMBus(1)
        self._set_controller_to_normal_mode()

    def setPWMFreqHz(self, freq):
        pre_scale = self._calc_pre_scale(freq)
        old_mode = self._read_from_register(PCA9685.__MODE1)
        new_mode = self._set_bit_4_sleep(self._reset_bit_7_restart_disabled(old_mode))
        self._write_to_register(PCA9685.__MODE1, new_mode)  # go to sleep
        self._write_to_register(PCA9685.__PRESCALE, int(math.floor(pre_scale)))
        self._write_to_register(PCA9685.__MODE1, old_mode)
        time.sleep(0.005)
        self._write_to_register(PCA9685.__MODE1, self._set_bit_7_restart_enabled(old_mode))

    def setPWM(self, channel_number, on_count, off_count):
        self._write_to_register(self.__LED0_ON_L + 4 * channel_number, self._value_low(on_count))
        self._write_to_register(self.__LED0_ON_H + 4 * channel_number, self._value_high(on_count))
        self._write_to_register(self.__LED0_OFF_L + 4 * channel_number, self._value_low(off_count))
        self._write_to_register(self.__LED0_OFF_H + 4 * channel_number, self._value_high(off_count))

    def _set_bit_7_restart_enabled(self, value):
        return value | 0x80

    def _set_bit_4_sleep(self, value):
        return value | 0x10  # 00010000

    def _reset_bit_7_restart_disabled(self, value):
        return value & 0x7F  # 01111111

    def _set_controller_to_normal_mode(self):
        self._write_to_register(self.__MODE1, 0x00)

    def _calc_pre_scale(self, frequency):
        return int(round(PCA9685.__INTERNAL_OSCILLATOR_CLOCK / (4096.0 * frequency)) - 1)

    def _write_to_register(self, register_address, value):
        self.bus.write_byte_data(PCA9685.__CONTROLLER_ADDRESS, register_address, value)

    def _read_from_register(self, register_address):
        return self.bus.read_byte_data(PCA9685.__CONTROLLER_ADDRESS, register_address)

    def _value_low(self, value):
        return value & 0xFF

    def _value_high(self, value):
        return (value >> 8) & 0xFF

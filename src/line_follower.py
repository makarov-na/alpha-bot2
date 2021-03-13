from alphabot.hardware.gpio_module import GpioWrapper
from alphabot.hardware.motor_module import LeftMotor, RightMotor


class Joystick:
    def __init__(self) -> None:
        super().__init__()

    def waitForCentralKeyPressed(self):
        pass


class LineSensor(object):
    def calibrate(self):
        pass

    def getTargetValue(self):
        return 0

    def getCurrentValue(self):
        return 0


class PidController:

    def __init__(self, target_value) -> None:
        self._target_value = target_value

    def getOutput(self, current_value):
        return 0




joystick = Joystick()
joystick.waitForCentralKeyPressed()

line_sensor = LineSensor()
line_sensor.calibrate()
target_value = line_sensor.getTargetValue()
current_value = line_sensor.getCurrentValue()
pid_controller = PidController(target_value)
output = pid_controller.getOutput(current_value)

gpio = GpioWrapper()

leftMotor = LeftMotor(gpio)
rightMotor = RightMotor(gpio)

bot_truck = BotTruck(leftMotor, rightMotor)

speed_power = 10
bot_truck.setSpeedPower(speed_power)  # -100 0 100
bot_truck.setTurnPower(output)  # -200 0 200
bot_truck.stop()  # power = 0

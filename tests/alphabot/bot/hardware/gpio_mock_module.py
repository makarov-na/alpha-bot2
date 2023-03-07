from alphabot.bot.hardware.gpio_module import GpioWrapper


class GpioWrapperMock(GpioWrapper):

    def __init__(self):
        self.LOW = 0
        self.HIGH = 1
        self.OUT = 2
        self.IN = 3
        self.PUD_UP = 4

    def setup(self, pin, mode, pull_up_down=None):
        pass

    def output(self, pin, value):
        pass

    def createPwm(self, pin, frequency):
        pass

    def input(self, pin):
        pass

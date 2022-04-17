import logging
from alphabot.follower.line_follower_module import LineFollower
from alphabot.hardware.gpio_module import GpioWrapper

logging.basicConfig(level=logging.INFO)
follower = LineFollower(gpio=GpioWrapper())
follower.logger.setLevel(level=logging.INFO)
follower.run()

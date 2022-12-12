import logging
from alphabot.follower.line_follower_module import LineFollower
from alphabot.bot.hardware.gpio_module import GpioWrapper

logging.basicConfig(level=logging.INFO)
follower = LineFollower(gpio=GpioWrapper())
follower.logger.setLevel(level=logging.INFO)
# logging.getLogger('alphabot.truck_module').setLevel(level=logging.ERROR)
follower.startFollowing()

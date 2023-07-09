import logging
from alphabot.follower.line_follower_module import LineFollower
from alphabot.bot.hardware.gpio_module import GpioWrapper

logging.basicConfig(level=logging.INFO)
follower = LineFollower(gpio=GpioWrapper())
logging.getLogger('alphabot.bot.truck_module').setLevel(level=logging.ERROR)
logging.getLogger('alphabot.follower.line_follower_module').setLevel(level=logging.ERROR)
logging.getLogger('alphabot.follower.state.linefollow.line_follower_algorithm_module').setLevel(level=logging.INFO)
follower.startFollowing()

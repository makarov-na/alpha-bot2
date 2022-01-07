import logging
from alphabot.follower.line_follower_module import LineFollower

logging.basicConfig(level=logging.INFO)
follower = LineFollower()
follower.logger.setLevel(level=logging.INFO)
follower.run()

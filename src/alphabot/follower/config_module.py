class LineFollowerConfig:
    def __init__(self) -> None:
        microsecond = 1 / 1_000_000
        millisecond = 1 / 1_000
        self.KP = 0.3
        self.KD = 20
        self.KI = 0
        self.MAX_OUT = 60
        self.SPEED_POWER = 25
        self.SLEEP_TIME = microsecond * 10
        self.TARGET_VALUE_LEFT = 0
        self.TARGET_VALUE_RIGHT = 0
        self.USE_CAMERA_COURSE_CORRECTION = False

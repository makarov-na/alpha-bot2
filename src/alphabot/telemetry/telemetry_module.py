from datetime import datetime
import os


class Telemetry:

    def __init__(self):
        self._telemetry_path = os.path.expanduser('~/.alpha-bot2')
        if not os.path.exists(self._telemetry_path):
            os.mkdir(self._telemetry_path)
        self._file_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".log"
        self._full_file_name = self._telemetry_path + '/' + self._file_name

    def send(self, telemetry_item: dict):
        with open(self._full_file_name, mode='a+t') as file_stream:
            file_stream.write(str(telemetry_item) + '\n')

from datetime import datetime
import os


class Telemetry:

    def __init__(self, buffer_size=100):
        self._buffer_size = buffer_size
        self._telemetry_path = os.path.expanduser('~/.alpha-bot2')
        if not os.path.exists(self._telemetry_path):
            os.mkdir(self._telemetry_path)
        self._file_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".log"
        self._full_file_name = self._telemetry_path + '/' + self._file_name
        self._buffer = []

    def send(self, telemetry_item: dict):
        self._buffer.append(telemetry_item)
        if len(self._buffer) == self._buffer_size:
            with open(self._full_file_name, mode='a+t') as file_stream:
                for item in self._buffer:
                    file_stream.write(str(item) + '\n')
                self._buffer = []

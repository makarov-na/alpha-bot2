import os
import shutil
import unittest
from datetime import datetime

from alphabot.telemetry.telemetry_module import Telemetry


class TestTelemetry(unittest.TestCase):

    def test_initialization(self):
        # GIVEN
        telemetry_path = os.path.expanduser('~/.alpha-bot2')
        shutil.rmtree(telemetry_path)

        # WHEN
        telemetry = Telemetry(1)

        # THEN
        self.assertEqual(datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".log", telemetry._file_name)
        self.assertTrue(os.path.exists(telemetry._telemetry_path))

    def test_write_file(self):
        # GIVEN
        telemetry = Telemetry(1)
        # WHEN
        telemetry.send({'test': 'test'})
        telemetry.send({'test1': 'test1'})
        telemetry.send({'test2': 'test2'})

        # THEN
        self.assertTrue(os.path.exists(telemetry._full_file_name))
        self.assertTrue(3, len(open(telemetry._full_file_name).readlines()))


if __name__ == '__main__':
    unittest.main()

import unittest
from beeper_module import Beeper

class TestBeeper(unittest.TestCase):

    def test_upper(self):


        self.assertEqual('foo'.upper(), 'FOO')




if __name__ == '__main__':
    unittest.main()

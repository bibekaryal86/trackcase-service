import unittest

from src.trackcase_service.main import ping


class MainTest(unittest.TestCase):
    def test_ping(self):
        self.assertEqual(ping(), {"test": "successful"})

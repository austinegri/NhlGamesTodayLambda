from datetime import datetime
from unittest import TestCase

from src.eventbridge.eventbridge import schedule


class Test(TestCase):
    def test_schedule(self):
        schedule('1111', datetime.now())

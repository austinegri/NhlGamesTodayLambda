import unittest

from src.scheduleHandler import lambda_handler


class TestLambdaScheduleHandler(unittest.TestCase):
    def test_lambda_handler(self):
        lambda_handler(None, None)
        self.assertN(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

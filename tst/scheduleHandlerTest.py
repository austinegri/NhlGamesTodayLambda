import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock, ANY, call
import responses

from src.eventbridge.eventbridge import Eventbridge
from src.scheduleHandler import lambda_handler
from tst.responseData.scheduleResponseWithGames import nhlScheduleResponseString

schedule_data_todays_games = json.loads(nhlScheduleResponseString)


class TestLambdaScheduleHandler(unittest.TestCase):
    @responses.activate
    @patch.object(Eventbridge, 'schedule')
    def test_lambda_handler(self, mockEventbridge):
        responses.add(responses.GET,
                      'https://api-web.nhle.com/v1/schedule/now',
                      json= schedule_data_todays_games,
                      status= 200)

        lambda_handler(None, None)
        print(mockEventbridge.call_args_list)
        expectedCallArgsList = [
            call(gameId=2023020474, scheduleTime=datetime(2023, 12, 17, 19, 55)),
            call(gameId=2023020475, scheduleTime=datetime(2023, 12, 17, 22, 55)),
            call(gameId=2023020476, scheduleTime=datetime(2023, 12, 17, 23, 55)),
            call(gameId=2023020477, scheduleTime=datetime(2023, 12, 18, 0, 55)),
            call(gameId=2023020478, scheduleTime=datetime(2023, 12, 18, 0, 55))]
        assert mockEventbridge.call_count == 5
        assert mockEventbridge.call_args_list == expectedCallArgsList

if __name__ == '__main__':
    unittest.main()

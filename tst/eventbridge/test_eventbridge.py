import os
from dataclasses import dataclass
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, ANY

import boto3
from dateutil.tz import tzlocal
from moto.scheduler import mock_scheduler

from src.eventbridge.eventbridge import Eventbridge


class TestEventbridge(TestCase):

    @patch.dict(os.environ, {"EVENT_BRIDGE_RULE": "GameDayGameStartRule",
                             "STATE_MACHINE": 'stepFunctionARN',
                             "STATE_MACHINE_EXECUTION_ROLE": "stepFunctionRole"}, clear=True)
    @mock_scheduler
    def test_schedule(self):
        mockScheduler = boto3.client("scheduler")

        underTest = Eventbridge()

        underTest.schedule('1111', datetime(year=2023, month=12, day= 12, hour=19, minute= 55))

        scheduleResponse = mockScheduler.list_schedules()
        actualScheduleList = scheduleResponse['Schedules']
        actualSchedule = Schedule(**actualScheduleList[0])

        expectedSchedule = Schedule(Arn= 'arn:aws:scheduler:us-east-1:123456789012:schedule/default/GameDayGameStartRule',
                                     CreationDate= ANY,
                                     GroupName= 'default',
                                     LastModificationDate= ANY,
                                     Name= 'GameDayGameStartRule',
                                     State= 'ENABLED',
                                     Target= {'Arn': 'stepFunctionARN'})

        self.assertEqual(len(actualScheduleList), 1)
        self.assertEqual(expectedSchedule, actualSchedule)


@dataclass
class Schedule:
    Arn: str
    CreationDate: datetime
    GroupName: str
    LastModificationDate: datetime
    Name: str
    State: str
    Target: dict

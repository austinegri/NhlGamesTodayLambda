import json
import os
from datetime import datetime

import boto3


class Eventbridge:
    scheduler = boto3.client('scheduler')

    def schedule(self, gameId, scheduleTime: datetime):
        response = self.scheduler.create_schedule(Name= os.environ.get('EVENT_BRIDGE_RULE', "GameDayGameStartRule"),
                                             ScheduleExpression= 'at({})'.format(scheduleTime.strftime('%Y-%m-%dT%H:%M:%S')),
                                             FlexibleTimeWindow={
                                                 'MaximumWindowInMinutes': 2,
                                                 'Mode': 'FLEXIBLE'
                                             },
                                             Target={
                                                 'Arn': os.environ.get('STATE_MACHINE'),
                                                 'RoleArn': os.environ.get('STATE_MACHINE_EXECUTION_ROLE'),
                                                 'Input': json.dumps({
                                                    'gameId': gameId}
                                                ),
                                             })
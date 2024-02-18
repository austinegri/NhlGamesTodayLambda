import json
import logging
import os
from datetime import datetime

import boto3

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

class Eventbridge:
    scheduler = boto3.client('scheduler')

    def schedule(self, gameId, scheduleTime: datetime):
        logger.info("Calling eventbridge to create schedule for game {} at time {}".format(gameId, scheduleTime))
        try:
            response = self.scheduler.create_schedule(Name='GameDayStart_{}'.format(gameId),
                                                  ScheduleExpression='at({})'.format(
                                                      scheduleTime.strftime('%Y-%m-%dT%H:%M:%S')),
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
                                                  },
                                                  ActionAfterCompletion= 'DELETE'
                                              )

            logger.info("Added eventbridge schedule for game {} at time {}, Eventbridge response: {}".format(gameId,
                                                                                                             scheduleTime,
                                                                                                             response))
            return
        except self.scheduler.exceptions.ConflictException:
            logger.info("Schedule for gameId={} at time {} already exists".format(gameId, scheduleTime))
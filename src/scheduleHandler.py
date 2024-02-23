import json
import logging
import os
from datetime import datetime, timedelta
import pytz

import requests

from src.data.game import Game
from src.eventbridge.eventbridge import Eventbridge


logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

DATE = 'date'
def lambda_handler(event, context):
    NHL_SCHEDULE_ENDPOINT = "https://api-web.nhle.com/v1/schedule/{}"

    eventbridge = Eventbridge()

    if DATE in event:
        currentDate = datetime.strptime(event[DATE], '%Y-%m-%d')
    else:
        currentDate = datetime.now(pytz.timezone('America/New_York'))

    r = requests.get(NHL_SCHEDULE_ENDPOINT.format(currentDate.strftime('%Y-%m-%d')))
    r_json = r.json()

    scheduled_games = set()

    if len(r_json.get('gameWeek')) > 0:
        gamesToday = r_json.get('gameWeek')[0]['games']
        for gameJson in gamesToday:
            try:
                game = Game.fromDict(gameJson) # classFromArgs(Game, gameJson)
                gameTime = datetime.strptime(game.startTimeUTC, '%Y-%m-%dT%H:%M:%SZ')
                scheduleTime = gameTime - timedelta(minutes=5)
                response = eventbridge.schedule(gameId= game.id, scheduleTime= scheduleTime)
                logger.info("Added eventbridge schedule for game {} at time {}, Eventbridge response: {}".format(game.id, scheduleTime, response))
                scheduled_games.add(game.id)
            except:
                logger.exception("Cannot schedule game for {}".format(gameJson))
                continue
    return {
        "statusCode": 200,
        "body": json.dumps("EventBridgeScheduled for games {}".format(scheduled_games))
    }
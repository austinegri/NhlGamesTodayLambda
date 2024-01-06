import json
import logging
from datetime import datetime, timedelta
import pytz

import requests

from data.game import Game
from eventbridge.eventbridge import Eventbridge


logger = logging.getLogger()

def lambda_handler(event, context):
    NHL_SCHEDULE_ENDPOINT = "https://api-web.nhle.com/v1/schedule/{}"

    eventbridge = Eventbridge()

    currentDate = datetime.now(pytz.timezone('America/New_York'))

    r = requests.get(NHL_SCHEDULE_ENDPOINT.format(currentDate.strftime('%Y-%m-%d')))
    r_json = r.json()
    logger.info(r.json())

    scheduled_games = set()

    if len(r_json.get('gameWeek')) > 0:
        gamesToday = r_json.get('gameWeek')[0]['games']
        for gameJson in gamesToday:
            try:
                game = Game(**gameJson) # classFromArgs(Game, gameJson)
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
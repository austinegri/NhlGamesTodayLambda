import json
import logging
from datetime import datetime, timedelta

import requests

from src.data.game import Game
from src.eventbridge import eventbridge

logger = logging.getLogger()

NHL_SCHEDULE_ENDPOINT = "https://api-web.nhle.com/v1/schedule/now"
def lambda_handler(event, context):
    r = requests.get(NHL_SCHEDULE_ENDPOINT)
    r_json = r.json()
    logger.info(r.json())

    if len(r_json.get('gameWeek')) > 0:
        gamesToday = r_json.get('gameWeek')[0]['games']
        for gameJson in gamesToday:
            game = Game(**gameJson) # classFromArgs(Game, gameJson)
            gameTime = datetime.strptime(game.startTimeUTC, '%Y-%m-%dT%H:%M:%SZ')
            eventbridge.schedule(game.id, gameTime - timedelta(minutes=5))

    return {
        "statusCode": 200,
        "body": json.dumps("EventBridgeScheduled for games {}")
    }
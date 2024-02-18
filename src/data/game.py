import inspect
from dataclasses import dataclass, field
from typing import List


@dataclass
class Game:
    id: int
    season: int
    gameType: int
    venue: dict
    neutralSite: bool
    startTimeUTC: str
    awayTeam: dict
    homeTeam: dict
    periodDescriptor: dict

    easternUTCOffset: str = ""
    venueUTCOffset: str = ""
    venueTimezone: str = ""
    gameState: str = ""
    gameScheduleState: str = ""
    tvBroadcasts : List[dict] = field(default_factory= [])
    ticketsLink: str = ""
    gameCenterLink: str = ""

    @classmethod
    def fromDict(cls, gameJson):
        return cls(**{
            k: v for k, v in gameJson.items()
            if k in inspect.signature(cls).parameters
        })
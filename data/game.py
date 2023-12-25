from dataclasses import dataclass, fields, field
from typing import Optional, List


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
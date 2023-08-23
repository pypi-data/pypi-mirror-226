"""NBA teams module"""

from typing import Optional

from basketix.tables import NbaTeamsTable


class NbaTeamsHandler:
    """Handle NBA teams."""

    _MAPPING_ID_TRICODE = {
        "1610612757": "POR",
        "1610612742": "DAL",
        "1610612741": "CHI",
        "1610612737": "ATL",
        "1610612752": "NYK",
        "1610612753": "ORL",
        "1610612754": "IND",
        "1610612759": "SAS",
        "1610612764": "WAS",
        "1610612745": "HOU",
        "1610612739": "CLE",
        "1610612751": "BKN",
        "1610612750": "MIN",
        "1610612738": "BOS",
        "1610612763": "MEM",
        "1610612758": "SAC",
        "1610612746": "LAC",
        "1610612744": "GSW",
        "1610612756": "PHX",
        "1610612747": "LAL",
        "1610612749": "MIL",
        "1610612762": "UTA",
        "1610612761": "TOR",
        "1610612766": "CHA",
        "1610612765": "DET",
        "1610612748": "MIA",
        "1610612740": "NOP",
        "1610612760": "OKC",
        "1610612755": "PHI",
        "1610612743": "DEN",
    }

    _MAPPING_TRICODE_ID = {tricode: _id for _id, tricode in _MAPPING_ID_TRICODE.items()}

    @classmethod
    def tricode(cls, id: str):
        return cls._MAPPING_ID_TRICODE[id]

    @classmethod
    def id(cls, tricode: str):
        return cls._MAPPING_TRICODE_ID[tricode.upper()]

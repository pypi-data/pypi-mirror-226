"""NBA teams module"""

from typing import Optional

from basketix.tables import NbaTeamsTable


class NbaTeamsHandler:
    """Handle NBA teams."""

    _MAPPING_ID_TRICODE = {
        "1610612738": "BOS",
    }

    _MAPPING_TRICODE_ID = {tricode: _id for _id, tricode in _MAPPING_ID_TRICODE}

    @classmethod
    def tricode(cls, id: str):
        return cls._MAPPING_ID_TRICODE[id]

    @classmethod
    def id(cls, tricode: str):
        return cls._MAPPING_TRICODE_ID[tricode]

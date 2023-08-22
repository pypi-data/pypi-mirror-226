"""Game related objects."""
import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from asyncpixel.constants import GameType
from asyncpixel.utils import validate_game_type

from .utils import to_camel


class Game(BaseModel):
    """Game class.

    Args:
        date (datetime.datetime): Time game started.
        game_type (GameType): Game Type.
        mode (Optional[str]): Game mode.
        map (Optional[str]): Map the game is on.
        ended (Optional[datetime.datetime]): Time game ended. Defaults to None.
    """

    date: datetime.datetime
    game_type: GameType
    mode: Optional[str] = None
    map: Optional[str] = None
    ended: Optional[datetime.datetime] = None

    @field_validator("game_type", mode="before")
    @classmethod
    def _validate_game_type(cls, v: str) -> GameType:
        """Turn game type to correct format."""
        return validate_game_type(v)

    model_config = ConfigDict(alias_generator=to_camel)

"""Constants."""
import json
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

script_dir = os.path.dirname(os.path.realpath(__file__))


class GameType(BaseModel):
    """Main game class.

    Args:
        id (str): ID
        purchaser_uuid (uuid.UUID): UUID of booster.
        amount (int): Amount of boosters.
        original_length (int): Original length of booster.
        length (int): Length of booster.
        game_type (int): Game type.
        date_activated (datetime.datetime): Date boost activated.
        stacked (Union[List[uuid.UUID], bool]): Whether boosters stacked.
    """

    id: int
    type_name: str
    database_name: str
    lobby_name: Optional[str] = None
    clean_name: str
    standard_name: str
    legacy: bool = False


# with open("asyncpixel/hypixelconstants/build/achievements.json") as file:
#     achievements: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/achievements_extended.json") as file:
#     achivements_extended: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/challenges.json") as file:
#     challenges: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/guild_achivements.json") as file:
#     guild_achivements: Dict[str, Any] = json.load(file)


# with open("asyncpixel/hypixelconstants/build/languages.json") as file:
#     languages: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/maps.json") as file:
#     maps: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/modes.json") as file:
#     modes: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/pet_xp.json") as file:
#     pet_xp: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/quests.json") as file:
#     quests: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/skyblock_bazaar.json") as file:
#     skyblock_bazaar: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/skyblock_collections.json") as file:
#     skyblock_collections: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/skyblock_items.json") as file:
#     skyblock_items: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/achievements.json") as file:
#     achievements: Dict[str, Any] = json.load(file)

# with open("asyncpixel/hypixelconstants/build/skyblock_skills.json") as file:
#     skyblock_skills: Dict[str, Any] = json.load(file)


@lru_cache()
def get_game_types() -> List[GameType]:
    """Get current game types.

    Returns:
        List[GameType]: game types.
    """
    abs_file_path = os.path.join(script_dir, "hypixelconstants/build/game_types.json")
    with open(abs_file_path) as file:
        game_types_data: Dict[str, Any] = json.load(file)
    return [GameType.model_validate(data) for data in game_types_data]

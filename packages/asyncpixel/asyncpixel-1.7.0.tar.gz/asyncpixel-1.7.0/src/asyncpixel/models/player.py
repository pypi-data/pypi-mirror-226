"""Player objects."""
import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.types import UUID4

from asyncpixel import utils
from asyncpixel.constants import GameType
from asyncpixel.models.pet import Pet

from .players import (
    MCGO,
    UHC,
    Arcade,
    Arena,
    Battleground,
    Bedwars,
    BuildBattle,
    Duels,
    GingerBread,
    Housing,
    HungerGames,
    Legacy,
    Paintball,
    Pit,
    Quake,
    SkyClash,
    Skywars,
    TNTGames,
    VampireZ,
    Walls,
    Walls3,
)
from .utils import to_camel


class Stats(BaseModel):
    """Game Stats.

    Args:
        bedwars (Optional[Bedwars]): bedwars stats.
        arcade (Optional[Arcade]): Arcade stats.
        build_battle (Optional[BuildBattle]): Build Battle stats.
        duels (Optional[Duels]): Duels stats.
        battleground (Optional[Battleground]): Battleground stats.
        hunger_games (Optional[HungerGames]): Hunger Games stats.
        ginger_bread (Optional[GingerBread]): Ginger Bread stats.
        paintball (Optional[Paintball]): Paintball stats.
        quake (Optional[Quake]): Quake stats.
        vampirez (Optional[VampireZ]): VampireZ stats.
        tnt_games (Optional[TNTGames]): TNT Games stats.
        uhc (Optional[UHC]): UHC stats.
        mcgo (Optional[MCGO]): MCGO stats.
        walls3 (Optional[Walls3]): Walls3 stats.
        walls (Optional[Walls]): Walls stats.
        arena (Optional[Arena]): Arena stats.
        sky_clash (Optional[SkyClash]): SkyClash stats.
        pit (Optional[Pit]): Pit stats.
        housing (Optional[Housing]): Housing stats.
        legacy (Optional[Legacy]): Legacy stats.
    """

    bedwars: Optional[Bedwars] = Field(alias="Bedwars", default=None)
    arcade: Optional[Arcade] = Field(alias="Arcade", default=None)
    build_battle: Optional[BuildBattle] = Field(alias="BuildBattle", default=None)
    duels: Optional[Duels] = Field(alias="Duels", default=None)
    battleground: Optional[Battleground] = Field(alias="Battleground", default=None)
    hunger_games: Optional[HungerGames] = Field(alias="HungerGames", default=None)
    ginger_bread: Optional[GingerBread] = Field(alias="GingerBread", default=None)
    paintball: Optional[Paintball] = Field(alias="Paintball", default=None)
    quake: Optional[Quake] = Field(alias="Quake", default=None)
    vampirez: Optional[VampireZ] = Field(alias="VampireZ", default=None)
    tnt_games: Optional[TNTGames] = Field(alias="TNTGames", default=None)
    uhc: Optional[UHC] = Field(alias="UHC", default=None)
    mcgo: Optional[MCGO] = Field(alias="MCGO", default=None)
    walls3: Optional[Walls3] = Field(alias="Walls3", default=None)
    walls: Optional[Walls] = Field(alias="Walls", default=None)
    arena: Optional[Arena] = Field(alias="Arena", default=None)
    sky_clash: Optional[SkyClash] = Field(alias="SkyClash", default=None)
    pit: Optional[Pit] = Field(alias="Pit", default=None)
    housing: Optional[Housing] = Field(alias="Housing", default=None)
    legacy: Optional[Legacy] = Field(alias="Legacy", default=None)
    skywars: Optional[Skywars] = Field(alias="SkyWars", default=None)

    # true_combat: Optional[TrueCombat] = Field(alias="TrueCombat", default=None)
    # speed_uhc: Optional[SpeedUHC]= Field(alias="SpeedUHC", default=None)
    # sky_block: Optional[SkyBlock]= Field(alias="SkyBlock", default=None)
    # super_smash: Optional[SuperSmash] = Field(alias="SuperSmash", default=None)


class Social(BaseModel):
    """Social accounts.

    Args:
        twitter (Optional[str]): Twitter.
        youtube (Optional[str]): YouTube.
        instagram (Optional[str]): Instagram.
        twitch (Optional[str]): Twitch.
        discord (Optional[str]): Discord.
        hypixel_forums (Optional[str]): Hypixel Forums.
    """

    twitter: Optional[str] = None
    youtube: Optional[str] = None
    instagram: Optional[str] = None
    twitch: Optional[str] = None
    discord: Optional[str] = None
    hypixel_forums: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def get_social_media(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Get social media in correct format."""
        out = values.copy()
        for k, v in out["links"].items():
            out[k.lower()] = v
        return out


class Player(BaseModel):
    """Player.

    Args:
        uuid (UUID4): uuid of user.
        displayname (Optional[str]): Display name of user.
        rank (Optional[str]): Rank of user
        first_login (datetime.datetime): First login date.
        last_login (Optional[datetime.datetime]): Most recent login date.
        last_logout (Optional[datetime.datetime]): Last logout.
        stats (Stats): Stats for various game types.
        social_media (Optional[Social]): Social media accounts.
        id (Optional[str]): id of user.
        playername (Optional[str]): Playername.
        known_aliases (Optional[List[str]]): known aliases.
        known_aliases_lower (Optional[List[str]]): known aliases in lowercase.
        achievements_one_time (Optional[List[str]]): Achievements.
        mc_version_rp (Optional[str]): Minecraft version.
        network_exp (Optional[float]): Network experience.
        karma (Optional[int]): Player karma.
        last_adsense_generate_time (Optional[datetime.datetime]): Last generate
            time for adsense.
        last_claimed_reward (Optional[int]): Last claimed reward.
        total_rewards (Optional[int]): Total rewards.
        total_daily_rewards (Optional[int]): Total daily awards.
        reward_streak (Optional[int]): Current reward streak.
        reward_score (Optional[int]): Reward score.
        reward_high_score (Optional[int]): High score for rewards.
        friend_requests_uuid (Optional[List[UUID4]]): UUID of friend requests.
        achievement_tracking (Optional[List[str]]): Achievement tracking.
        achievement_points (Optional[int]): achievement points.
        current_gadget (Optional[str]): Current equipped gadget.
        channel (Optional[str]): Channel.
        most_recent_game_type (Optional[GameType]): Most recent Game Type that
            has been played.
        level (Optional[float]): Level of user.
        pet_stats (Optional[Pet]): Pet stats.
        raw (Dict[str, Any]): raw data
    """

    uuid: UUID4
    displayname: Optional[str] = None
    rank: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def create_rank(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Get the rank."""
        out = values.copy()
        rank = utils.get_rank(
            values.get("rank"),
            values.get("prefix"),
            values.get("monthlyPackageRank"),
            values.get("newPackageRank"),
            values.get("packageRank"),
        )
        out["rank"] = rank
        return out

    first_login: datetime.datetime
    last_login: Optional[datetime.datetime] = None
    last_logout: Optional[datetime.datetime] = None
    stats: Stats
    social_media: Optional[Social] = None

    id: Optional[str] = Field(alias="_id", default=None)
    playername: Optional[str] = None
    known_aliases: Optional[List[str]] = None
    known_aliases_lower: Optional[List[str]] = None
    achievements_one_time: Optional[List[str]] = None
    mc_version_rp: Optional[str] = None
    network_exp: Optional[float] = None
    karma: Optional[int] = None
    last_adsense_generate_time: Optional[datetime.datetime] = None
    last_claimed_reward: Optional[int] = None
    total_rewards: Optional[int] = None
    total_daily_rewards: Optional[int] = None
    reward_streak: Optional[int] = None
    reward_score: Optional[int] = None
    reward_high_score: Optional[int] = None
    friend_requests_uuid: Optional[List[UUID4]] = None
    achievement_tracking: Optional[List[str]] = None
    achievement_points: Optional[int] = None
    current_gadget: Optional[str] = None
    channel: Optional[str] = None
    most_recent_game_type: Optional[GameType] = None
    pet_stats: Optional[Dict[str, Pet]] = None

    @field_validator("most_recent_game_type", mode="before")
    @classmethod
    def _validate_game_type(cls, v: Union[str, int]) -> GameType:
        """Validate game type."""
        return utils.validate_game_type(v)

    level: float

    @model_validator(mode="before")
    @classmethod
    def create_level(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Create level."""
        out = values.copy()
        exp = float(out.get("networkExp", 0.0))
        out["level"] = utils.calc_player_level(exp)
        return out

    raw: Dict[str, Any]

    @model_validator(mode="before")
    @classmethod
    def create_raw(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Create a copy of the values to directly access."""
        out = values.copy()
        out["raw"] = values
        return out

    model_config = ConfigDict(alias_generator=to_camel)

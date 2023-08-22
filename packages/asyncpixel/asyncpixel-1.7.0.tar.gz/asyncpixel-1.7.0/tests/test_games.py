"""Test games."""
import datetime
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel
from asyncpixel.constants import GameType


@pytest.mark.asyncio
async def test_games(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the games method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/recentGames?key={key!s}" + "&uuid=7486aa03aca5470e888dde8a43eb8c10",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "games": [
                    {
                        "date": 1590935247444,
                        "gameType": "SKYWARS",
                        "mode": "solo_normal",
                        "map": "Shire",
                    },
                    {
                        "date": 1590850836485,
                        "gameType": "BEDWARS",
                        "mode": "FOUR_FOUR",
                        "map": "Dreamgrove",
                        "ended": 1590850919917,
                    },
                    {
                        "date": 1590850404473,
                        "gameType": "SKYWARS",
                        "mode": "ranked_normal",
                        "map": "Meteor",
                        "ended": 1590850783962,
                    },
                    {
                        "date": 1590850359562,
                        "gameType": "DUELS",
                        "mode": "SW_DUEL",
                        "map": "Agni Temple",
                        "ended": 1590850500815,
                    },
                    {
                        "date": 1590850287155,
                        "gameType": "SKYWARS",
                        "mode": "solo_insane",
                        "map": "Mythic",
                        "ended": 1590850352734,
                    },
                ],
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.recent_games("7486aa03aca5470e888dde8a43eb8c10")

        assert data is not None
        assert len(data) == 5

        assert data[0].date == datetime.datetime.fromtimestamp(1590935247.444, tz=datetime.timezone.utc)
        assert data[0].game_type == GameType(
            id=51,
            type_name="SKYWARS",
            database_name="SkyWars",
            lobby_name="sw",
            clean_name="SkyWars",
            standard_name="SkyWars",
        )
        assert data[0].mode == "solo_normal"
        assert data[0].map == "Shire"

        assert data[1].date == datetime.datetime.fromtimestamp(1590850836.485, tz=datetime.timezone.utc)
        # assert data[1].game_type == gametype("BEDWARS", "Bedwars", "Bed Wars", 58)
        GameType(
            id=51,
            type_name="SKYWARS",
            database_name="SkyWars",
            lobby_name="sw",
            clean_name="SkyWars",
            standard_name="SkyWars",
        )
        assert data[1].mode == "FOUR_FOUR"
        assert data[1].map == "Dreamgrove"
        assert data[1].ended == datetime.datetime.fromtimestamp(1590850919.917, tz=datetime.timezone.utc)

        assert data[2].date == datetime.datetime.fromtimestamp(1590850404.473, tz=datetime.timezone.utc)
        assert data[2].game_type == GameType(
            id=51,
            type_name="SKYWARS",
            database_name="SkyWars",
            lobby_name="sw",
            clean_name="SkyWars",
            standard_name="SkyWars",
        )
        assert data[2].mode == "ranked_normal"
        assert data[2].map == "Meteor"
        assert data[2].ended == datetime.datetime.fromtimestamp(1590850783.962, tz=datetime.timezone.utc)

        assert data[3].date == datetime.datetime.fromtimestamp(1590850359.562, tz=datetime.timezone.utc)
        assert data[3].game_type == GameType(
            id=61,
            type_name="DUELS",
            database_name="Duels",
            lobby_name="duels",
            clean_name="Duels",
            standard_name="Duels",
        )
        assert data[3].mode == "SW_DUEL"
        assert data[3].map == "Agni Temple"
        assert data[3].ended == datetime.datetime.fromtimestamp(1590850500.815, tz=datetime.timezone.utc)

        assert data[4].date == datetime.datetime.fromtimestamp(1590850287.155, tz=datetime.timezone.utc)
        assert data[4].game_type == GameType(
            id=51,
            type_name="SKYWARS",
            database_name="SkyWars",
            lobby_name="sw",
            clean_name="SkyWars",
            standard_name="SkyWars",
        )
        assert data[4].mode == "solo_insane"
        assert data[4].map == "Mythic"
        assert data[4].ended == datetime.datetime.fromtimestamp(1590850352.734, tz=datetime.timezone.utc)


@pytest.mark.asyncio
async def test_games_none(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the games method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/recentGames?key={key!s}" + "&uuid=7486aa03aca5470e888dde8a43eb8c10",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "games": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.recent_games("7486aa03aca5470e888dde8a43eb8c10")

        assert data is None

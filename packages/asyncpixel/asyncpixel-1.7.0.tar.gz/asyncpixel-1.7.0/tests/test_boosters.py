"""Test boosters."""
import datetime
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel
from asyncpixel.constants import GameType
from tests.utils import generate_key


@pytest.mark.asyncio
async def test_boosters(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the boosters method returns correct data."""
    purchaseruuid1 = generate_key()
    purchaseruuid2 = generate_key()
    purchaseruuid3 = generate_key()
    stacked1 = generate_key()
    stacked2 = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/boosters?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "boosters": [
                    {
                        "_id": "5c197fadc8f245280926413d",
                        "purchaserUuid": str(purchaseruuid1),
                        "amount": 2,
                        "originalLength": 3600,
                        "length": 3595,
                        "gameType": 24,
                        "dateActivated": 1545244519133,
                        "stacked": True,
                    },
                    {
                        "_id": "5de1bf590cf2544cd01a7e04",
                        "purchaserUuid": str(purchaseruuid2),
                        "amount": 2.2,
                        "originalLength": 3600,
                        "length": 2074,
                        "gameType": 13,
                        "dateActivated": 1590842991659,
                        "stacked": [
                            str(stacked1),
                            str(stacked2),
                        ],
                    },
                    {
                        "_id": "6de1bf590cf2544cd01a7e04",
                        "purchaserUuid": str(purchaseruuid3),
                        "amount": 2.2,
                        "originalLength": 3600,
                        "length": 2074,
                        "gameType": 13,
                        "dateActivated": 1590842991659,
                    },
                ],
                "boosterState": {"decrementing": True},
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.boosters()

        assert data is not None

        assert len(data.boosters) == 3
        assert data.booster_state_decrementing is True

        assert data.boosters[0].id == "5c197fadc8f245280926413d"
        assert data.boosters[0].purchaser_uuid == purchaseruuid1
        assert data.boosters[0].amount == 2.0
        assert data.boosters[0].original_length == 3600
        assert data.boosters[0].length == 3595
        assert data.boosters[0].game_type == GameType(
            id=24,
            type_name="SUPER_SMASH",
            database_name="SuperSmash",
            lobby_name="smash",
            clean_name="Smash Heroes",
            standard_name="Smash",
        )
        assert data.boosters[0].date_activated == datetime.datetime.fromtimestamp(
            1545244519.133, tz=datetime.timezone.utc
        )
        assert data.boosters[0].stacked is True

        assert data.boosters[1].id == "5de1bf590cf2544cd01a7e04"
        assert data.boosters[1].purchaser_uuid == purchaseruuid2
        assert data.boosters[1].amount == 2.2
        assert data.boosters[1].original_length == 3600
        assert data.boosters[1].length == 2074
        assert data.boosters[1].game_type == GameType(
            id=13,
            type_name="WALLS3",
            database_name="Walls3",
            lobby_name="megawalls",
            clean_name="Mega Walls",
            standard_name="MegaWalls",
        )

        assert data.boosters[1].date_activated == datetime.datetime.fromtimestamp(
            1590842991.659, tz=datetime.timezone.utc
        )
        assert data.boosters[1].stacked == [
            stacked1,
            stacked2,
        ]

        assert data.boosters[2].id == "6de1bf590cf2544cd01a7e04"
        assert data.boosters[2].purchaser_uuid == purchaseruuid3
        assert data.boosters[2].amount == 2.2
        assert data.boosters[2].original_length == 3600
        assert data.boosters[2].length == 2074
        assert data.boosters[2].game_type == GameType(
            id=13,
            type_name="WALLS3",
            database_name="Walls3",
            lobby_name="megawalls",
            clean_name="Mega Walls",
            standard_name="MegaWalls",
        )
        assert data.boosters[2].date_activated == datetime.datetime.fromtimestamp(
            1590842991.659, tz=datetime.timezone.utc
        )
        assert data.boosters[2].stacked is False

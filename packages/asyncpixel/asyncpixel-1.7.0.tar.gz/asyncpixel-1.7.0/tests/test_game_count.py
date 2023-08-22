"""Test game count."""
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_game_count(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the game_count method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/gameCounts?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "games": {
                    "SKYBLOCK": {
                        "players": 30522,
                        "modes": {
                            "combat_1": 690,
                            "foraging_1": 1456,
                            "hub": 8049,
                            "mining_2": 1062,
                            "combat_2": 277,
                            "farming_2": 247,
                            "mining_1": 300,
                            "farming_1": 204,
                            "combat_3": 2350,
                            "dynamic": 15888,
                        },
                    },
                    "BEDWARS": {"players": 30323},
                },
                "playerCount": 77238,
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.game_count()

        assert data is not None

        assert data.player_count == 77238
        assert data.games["SKYBLOCK"].players == 30522
        assert data.games["SKYBLOCK"].modes is not None
        assert data.games["SKYBLOCK"].modes["combat_1"] == 690
        assert data.games["SKYBLOCK"].modes["foraging_1"] == 1456
        assert data.games["SKYBLOCK"].modes["hub"] == 8049
        assert data.games["SKYBLOCK"].modes["mining_2"] == 1062
        assert data.games["SKYBLOCK"].modes["combat_2"] == 277
        assert data.games["SKYBLOCK"].modes["farming_2"] == 247
        assert data.games["SKYBLOCK"].modes["mining_1"] == 300
        assert data.games["SKYBLOCK"].modes["farming_1"] == 204
        assert data.games["SKYBLOCK"].modes["combat_3"] == 2350
        assert data.games["SKYBLOCK"].modes["dynamic"] == 15888
        assert data.games["BEDWARS"].players == 30323

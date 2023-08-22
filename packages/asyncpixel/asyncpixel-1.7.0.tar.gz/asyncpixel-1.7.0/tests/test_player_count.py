"""Test player count."""
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_player_count(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the player_count method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/playerCount?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "playerCount": 75612},
        )
        data = None
        async for client in hypixel_client:
            data = await client.player_count()

        assert data is not None

        assert data == 75612

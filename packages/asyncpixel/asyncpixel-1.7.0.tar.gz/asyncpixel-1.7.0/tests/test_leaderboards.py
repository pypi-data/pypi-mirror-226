"""Test leaderboards."""
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_leaderboards(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the leaderboards method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/leaderboards?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "leaderboards": {
                    "SKYWARS": [
                        {
                            "path": "wins",
                            "prefix": "Overall",
                            "title": "Wins",
                            "location": "-2556,55,712",
                            "count": 14,
                            "leaders": [
                                "2afdb69c-c007-40cd-98b9-76a7554612d9",
                                "6951ccdb-9ca7-4c8a-883b-a8d3bb81c3d2",
                                "e61044cc-c42f-439b-9ad7-817c51ae7174",
                            ],
                        }
                    ]
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.leaderboards()

        assert data is not None

        assert len(data.keys()) == 1
        assert next(iter(data.keys())) == "SKYWARS"
        assert len(data["SKYWARS"]) == 1
        assert data["SKYWARS"][0].path == "wins"
        assert data["SKYWARS"][0].prefix == "Overall"
        assert data["SKYWARS"][0].title == "Wins"
        assert data["SKYWARS"][0].location == (-2556, 55, 712)
        assert data["SKYWARS"][0].count == 14
        assert len(data["SKYWARS"][0].leaders) == 3
        assert data["SKYWARS"][0].leaders[0] == uuid.UUID("2afdb69c-c007-40cd-98b9-76a7554612d9")
        assert data["SKYWARS"][0].leaders[1] == uuid.UUID("6951ccdb-9ca7-4c8a-883b-a8d3bb81c3d2")
        assert data["SKYWARS"][0].leaders[2] == uuid.UUID("e61044cc-c42f-439b-9ad7-817c51ae7174")

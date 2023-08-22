"""Test news."""
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_skyblock_news(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the skyblock_news method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/news?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "items": [
                    {
                        "item": {"material": "MONSTER_EGG", "data": 90},
                        "link": "https://hypixel.net/threads/2852738/",
                        "text": "6th May 2020",
                        "title": "SkyBlock v0.7.8",
                    },
                    {
                        "item": {"material": "GOLD_NUGGET"},
                        "link": "https://hypixel.net/threads/2655146/",
                        "text": "9th March 2020",
                        "title": "SkyBlock v0.7.7",
                    },
                ],
            },
        )
        data = None
        async for client in hypixel_client:
            data = await client.news()

        assert data is not None

        assert len(data) == 2

        assert data[0].item.material == "MONSTER_EGG"
        assert data[0].item.data == 90
        assert data[0].link == "https://hypixel.net/threads/2852738/"
        assert data[0].text == "6th May 2020"
        assert data[0].title == "SkyBlock v0.7.8"

        assert data[1].item.material == "GOLD_NUGGET"
        assert data[1].link == "https://hypixel.net/threads/2655146/"
        assert data[1].text == "9th March 2020"
        assert data[1].title == "SkyBlock v0.7.7"

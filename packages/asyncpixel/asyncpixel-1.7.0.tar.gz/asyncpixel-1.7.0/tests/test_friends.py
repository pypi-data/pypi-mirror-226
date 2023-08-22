"""Test friends."""
import datetime
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_friends(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the friends method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/friends?key={key!s}&uuid=74" + "86aa03aca5470e888dde8a43eb8c10",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "records": [
                    {
                        "_id": "5eb97d170cf22f431e8d6170",
                        "uuidSender": "20934ef9488c465180a78f861586b4cf",
                        "uuidReceiver": "7486aa03aca5470e888dde8a43eb8c10",
                        "started": 1589214487454,
                    }
                ],
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.player_friends("7486aa03aca5470e888dde8a43eb8c10")

        assert data is not None
        assert len(data) == 1
        assert data[0].id == "5eb97d170cf22f431e8d6170"
        assert data[0].uuid_sender == uuid.UUID("20934ef9488c465180a78f861586b4cf")
        assert data[0].uuid_receiver == uuid.UUID("7486aa03aca5470e888dde8a43eb8c10")
        assert data[0].started == datetime.datetime.fromtimestamp(1589214487.454, tz=datetime.timezone.utc)


@pytest.mark.asyncio
async def test_friends_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the friends method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/friends?key={key!s}&uuid=74" + "86aa03aca5470e888dde8a43eb8c10",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "records": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.player_friends("7486aa03aca5470e888dde8a43eb8c10")

        assert data is None

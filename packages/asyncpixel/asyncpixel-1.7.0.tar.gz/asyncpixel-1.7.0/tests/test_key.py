"""Testkey."""
import uuid

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel
from asyncpixel.exceptions.exceptions import InvalidApiKeyError
from tests.utils import generate_key


@pytest.mark.asyncio
async def test_default_key() -> None:
    """Test default key."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/key?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "record": {
                    "key": str(key),
                    "owner": "8ffb79fa-620e-45fe-8d62-381abd5bc60f",
                    "limit": 120,
                    "queriesInPastMin": 0,
                    "totalQueries": 849,
                },
            },
        )
        client = Hypixel(api_key=str(key))
        data = await client.key_data()

        assert data.key == key
        assert data.owner == uuid.UUID("8ffb79fa-620e-45fe-8d62-381abd5bc60f")
        assert data.limit == 120
        assert data.queries_in_past_min == 0
        assert data.total_queries == 849
        await client.close()


@pytest.mark.asyncio
async def test_added_key() -> None:
    """Test added key."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/key?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "record": {
                    "key": str(key),
                    "owner": "8ffb79fa-620e-45fe-8d62-381abd5bc60f",
                    "limit": 120,
                    "queriesInPastMin": 0,
                    "totalQueries": 849,
                },
            },
        )
        client = Hypixel(api_key=str(key))
        data = await client.key_data(str(key))

        assert data.key == key
        assert data.owner == uuid.UUID("8ffb79fa-620e-45fe-8d62-381abd5bc60f")
        assert data.limit == 120
        assert data.queries_in_past_min == 0
        assert data.total_queries == 849
        await client.close()


@pytest.mark.asyncio
async def test_no_key() -> None:
    """Test no key."""
    client = Hypixel()
    with pytest.raises(InvalidApiKeyError):
        await client.key_data()
    await client.close()

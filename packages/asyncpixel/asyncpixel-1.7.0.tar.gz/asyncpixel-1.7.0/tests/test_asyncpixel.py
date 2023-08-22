"""Main tests."""
from uuid import UUID

import pytest
from aioresponses import aioresponses

import asyncpixel

from .utils import generate_key


@pytest.mark.asyncio
async def test_get() -> None:
    """Test get method."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "Test_value": "Random string"},
        )
        client = asyncpixel.Hypixel(api_key=str(key))
        data = await client._get("test")
        assert data == {"success": True, "Test_value": "Random string"}
        await client.close()


@pytest.mark.asyncio
async def test_safe_ratelimit() -> None:
    """Test get method."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "0",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "Test_value": "Random string"},
        )
        client = asyncpixel.Hypixel(api_key=str(key))
        await client._get("test")
        with pytest.raises(asyncpixel.exceptions.RateLimitError):
            await client._get("test")
        await client.close()


@pytest.mark.asyncio
async def test_safe_no_key() -> None:
    """Test no key method."""
    client = asyncpixel.Hypixel()
    with pytest.raises(asyncpixel.exceptions.InvalidApiKeyError):
        await client._get("test")
    await client.close()


@pytest.mark.asyncio
async def test_no_hader() -> None:
    """Test get method."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=200,
            payload={"success": True, "Test_value": "Random string"},
        )
        client = asyncpixel.Hypixel(api_key=str(key))
        await client._get("test")
        await client.close()


@pytest.mark.asyncio
async def test_saved_rate_max() -> None:
    """Test get method."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "5",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "Test_value": "Random string"},
        )
        client = asyncpixel.Hypixel(api_key=str(key))
        await client._get("test")
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "200",
                "RateLimit-Remaining": "4",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "Test_value": "Random string"},
        )
        await client._get("test")
        assert client.total_requests == 120
        await client.close()


@pytest.mark.asyncio
async def test_get_uuid() -> None:
    """Test get uuid."""
    with aioresponses() as m:
        m.get(
            "https://api.mojang.com/users/profiles/minecraft/Technoblade",
            status=200,
            payload={"name": "Technoblade", "id": "b876ec32e396476ba1158438d83c67d4"},
        )
        client = asyncpixel.Hypixel()
        uuid = await client.uuid_from_name("Technoblade")
        assert uuid == UUID("b876ec32e396476ba1158438d83c67d4")
        await client.close()


@pytest.mark.asyncio
async def test_get_uuid_fail() -> None:
    """Test get uuid."""
    with aioresponses() as m:
        m.get(
            "https://api.mojang.com/users/profiles/minecraft/Technoblade",
            status=404,
        )
        client = asyncpixel.Hypixel()
        uuid = await client.uuid_from_name("Technoblade")
        assert uuid is None


@pytest.mark.asyncio
async def test_context_manager() -> None:
    """Test context manager."""
    with aioresponses() as m:
        m.get(
            "https://api.mojang.com/users/profiles/minecraft/Technoblade",
            status=200,
            payload={"name": "Technoblade", "id": "b876ec32e396476ba1158438d83c67d4"},
        )
        async with asyncpixel.Hypixel() as client:
            uuid = await client.uuid_from_name("Technoblade")
            assert uuid == UUID("b876ec32e396476ba1158438d83c67d4")

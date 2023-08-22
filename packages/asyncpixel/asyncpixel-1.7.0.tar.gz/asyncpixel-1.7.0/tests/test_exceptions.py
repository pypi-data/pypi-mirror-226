"""Test bazaar."""
import datetime

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel
from asyncpixel.exceptions import RateLimitError
from asyncpixel.exceptions.exceptions import ApiNoSuccessError, InvalidApiKeyError
from tests.utils import generate_key


@pytest.mark.asyncio
async def test_rate_limit() -> None:
    """Test bazaar."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=429,
            headers={"Retry-After": "5"},
            payload={"success": False, "cause": "Key throttle!", "throttle": True},
        )
        client = Hypixel(api_key=str(key))
        with pytest.raises(RateLimitError) as e:
            await client._get("test")
        assert str(e.value).startswith("The hypixel API ratelimit was reached, try again at ")
        await client.close()


@pytest.mark.asyncio
async def test_invalid_key() -> None:
    """Test bazaar."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=403,
            payload={"success": False, "cause": "Invalid API key"},
        )
        client = Hypixel(api_key=str(key))
        with pytest.raises(InvalidApiKeyError) as e:
            await client._get("test")
        assert str(e.value) == "Entered API key is not valid"
        await client.close()


@pytest.mark.asyncio
async def test_api_error() -> None:
    """Test bazaar."""
    key = generate_key()
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/test?key={key!s}",
            status=502,
            payload={"success": False, "cause": "Error"},
        )
        client = Hypixel(api_key=str(key))
        with pytest.raises(ApiNoSuccessError) as e:
            await client._get("test")
        assert str(e.value) == "The test endpoint encountered an error on the hypixel side."
        await client.close()


def test_str_api_error() -> None:
    """Check api error."""
    e = ApiNoSuccessError("test")
    assert str(e) == e.__str__()


def test_str_invalid_key() -> None:
    """Check api error."""
    e = InvalidApiKeyError()
    assert str(e) == e.__str__()


def test_str_rate_limit() -> None:
    """Check api error."""
    e = RateLimitError(datetime.datetime.now())
    assert str(e) == e.__str__()

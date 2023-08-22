"""pytest fixtures."""
import uuid
from typing import AsyncIterator

import pytest

from asyncpixel import Hypixel


@pytest.fixture
def key() -> uuid.UUID:
    """Generate key."""
    return uuid.uuid4()


@pytest.fixture
async def hypixel_client(key: uuid.UUID) -> AsyncIterator[Hypixel]:
    """Hypixel client fixture."""
    hypixel = Hypixel(api_key=str(key))
    yield hypixel
    await hypixel.close()


@pytest.fixture
async def hypixel_client_no_key() -> AsyncIterator[Hypixel]:
    """hypixel_client with no key."""
    hypixel = Hypixel()
    yield hypixel
    await hypixel.close()

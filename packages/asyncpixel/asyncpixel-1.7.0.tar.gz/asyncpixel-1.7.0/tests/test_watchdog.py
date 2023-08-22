"""Test watchdog."""
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_watchdog(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the watchdog method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/watchdogstats?key={key!s}",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "watchdog_lastMinute": 5,
                "staff_rollingDaily": 1356,
                "watchdog_total": 4924740,
                "watchdog_rollingDaily": 7679,
                "staff_total": 1608360,
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.watchdog_stats()

        assert data is not None

        assert data.watchdog_last_minute == 5
        assert data.staff_rolling_daily == 1356
        assert data.watchdog_total == 4924740
        assert data.watchdog_rolling_daily == 7679
        assert data.staff_total == 1608360

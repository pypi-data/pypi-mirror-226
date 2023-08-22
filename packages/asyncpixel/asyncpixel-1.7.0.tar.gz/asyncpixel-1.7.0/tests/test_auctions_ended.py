"""Test Auctions."""
import datetime
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
@pytest.mark.parametrize("hypixel_client", ["hypixel_client", "hypixel_client_no_key"], indirect=True)
async def test_auctions_ended(hypixel_client: AsyncGenerator[Hypixel, None]) -> None:
    """Test to check the auctions ended method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.hypixel.net/skyblock/auctions_ended",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "lastUpdated": 1679435322685,
                "auctions": [
                    {
                        "auction_id": "50e70ff17ac2409b8d5e94e51b0e9531",
                        "seller": "3c0f6da52855408c96a87c391734f2db",
                        "seller_profile": "d7ab595483ac4e74aa137d5d4ce82cf6",
                        "buyer": "af510607b5734653aa61e1e51aa5fa39",
                        "timestamp": 1679435259014,
                        "price": 17000000,
                        "bin": True,
                        "item_bytes": "...",
                    }
                ],
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.auctions_ended()

        assert data is not None

        assert data.last_updated == datetime.datetime.fromtimestamp(1679435322.685, tz=datetime.timezone.utc)
        assert len(data.auctions) == 1

        assert data.auctions[0].bin
        assert data.auctions[0].auction_id == uuid.UUID("50e70ff17ac2409b8d5e94e51b0e9531")
        assert data.auctions[0].seller == uuid.UUID("3c0f6da52855408c96a87c391734f2db")
        assert data.auctions[0].seller_profile == uuid.UUID("d7ab595483ac4e74aa137d5d4ce82cf6")
        assert data.auctions[0].buyer == uuid.UUID("af510607b5734653aa61e1e51aa5fa39")

        assert data.auctions[0].timestamp == datetime.datetime.fromtimestamp(1679435259.014, tz=datetime.timezone.utc)
        assert data.auctions[0].price == 17000000
        assert data.auctions[0].item_bytes == "..."

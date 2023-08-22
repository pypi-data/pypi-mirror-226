"""Test Auctions."""
import datetime
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
@pytest.mark.parametrize("hypixel_client", ["hypixel_client", "hypixel_client_no_key"], indirect=True)
async def test_auctions(hypixel_client: AsyncGenerator[Hypixel, None]) -> None:
    """Test to check the auction method returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.hypixel.net/skyblock/auctions?page=0",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "page": 0,
                "totalPages": 32,
                "totalAuctions": 31267,
                "lastUpdated": 1571065561345,
                "auctions": [
                    {
                        "uuid": "bc581ce675e94a0c88ac9deae06090f0",
                        "auctioneer": "96a7c06732f54c1382ab6a2515dbb960",
                        "profile_id": "96a7c06732f54c1382ab6a2515dbb960",
                        "coop": ["96a7c06732f54c1382ab6a2515dbb960"],
                        "start": 1571049581232,
                        "end": 1571071181232,
                        "item_name": "Magical Mushroom Soup",
                        "item_lore": "§7Consuming this Magical Mushroom\n§7"
                        + "Soup on your private island\n§7allows the player "
                        + "to fly for §a2\n§aminutes§7. Leaving the private\n"
                        + "§7island will remove the effect!\n\n§a§lUNCOMMON",
                        "extra": "Magical Mushroom Soup Mushroom Soup",
                        "category": "consumables",
                        "tier": "UNCOMMON",
                        "starting_bid": 256,
                        "item_bytes": "...",
                        "claimed": False,
                        "claimed_bidders": [],
                        "highest_bid_amount": 256,
                        "bin": True,
                        "bids": [
                            {
                                "auction_id": "bc581ce675e94a0c88ac9deae06090f0",
                                "bidder": "70aafcc6764b45ff80e60226193a0784",
                                "profile_id": "70aafcc6764b45ff80e60226193a0784",
                                "amount": 256,
                                "timestamp": 1571065921089,
                            }
                        ],
                    }
                ],
            },
        )
        data = None
        async for client in hypixel_client:
            data = await client.auctions()

        assert data is not None

        assert data.page == 0
        assert data.total_pages == 32
        assert data.total_auctions == 31267
        assert data.last_updated == datetime.datetime.fromtimestamp(1571065561.345, tz=datetime.timezone.utc)
        assert len(data.auctions) == 1

        assert not data.auctions[0].active()
        assert data.auctions[0].lowest_possible_bid() == 294

        assert data.auctions[0].bin
        assert data.auctions[0].uuid == uuid.UUID("bc581ce675e94a0c88ac9deae06090f0")
        assert data.auctions[0].auctioneer == uuid.UUID("96a7c06732f54c1382ab6a2515dbb960")
        assert data.auctions[0].profile_id == uuid.UUID("96a7c06732f54c1382ab6a2515dbb960")
        assert len(data.auctions[0].coop) == 1
        assert data.auctions[0].coop[0] == uuid.UUID("96a7c06732f54c1382ab6a2515dbb960")
        assert data.auctions[0].start == datetime.datetime.fromtimestamp(1571049581.232, tz=datetime.timezone.utc)
        assert data.auctions[0].end == datetime.datetime.fromtimestamp(1571071181.232, tz=datetime.timezone.utc)
        assert data.auctions[0].item_name == "Magical Mushroom Soup"
        assert data.auctions[0].item_lore == (
            "§7Consuming this Magical Mushroom\n§7"
            + "Soup on your private island\n§7allows the player "
            + "to fly for §a2\n§aminutes§7. Leaving the private\n"
            + "§7island will remove the effect!\n\n§a§lUNCOMMON"
        )
        assert data.auctions[0].extra == "Magical Mushroom Soup Mushroom Soup"
        assert data.auctions[0].category == "consumables"
        assert data.auctions[0].tier == "UNCOMMON"
        assert data.auctions[0].starting_bid == 256
        assert data.auctions[0].item_bytes == "..."
        assert data.auctions[0].claimed is False
        assert data.auctions[0].claimed_bidders is not None
        assert len(data.auctions[0].claimed_bidders) == 0
        assert data.auctions[0].highest_bid_amount == 256
        assert data.auctions[0].bids is not None
        assert len(data.auctions[0].bids) == 1
        assert data.auctions[0].bids[0].auction_id == uuid.UUID("bc581ce675e94a0c88ac9deae06090f0")
        assert data.auctions[0].bids[0].bidder == uuid.UUID("70aafcc6764b45ff80e60226193a0784")
        assert data.auctions[0].bids[0].profile_id == uuid.UUID("70aafcc6764b45ff80e60226193a0784")
        assert data.auctions[0].bids[0].amount == 256
        assert data.auctions[0].bids[0].timestamp == datetime.datetime.fromtimestamp(
            1571065921.089, tz=datetime.timezone.utc
        )

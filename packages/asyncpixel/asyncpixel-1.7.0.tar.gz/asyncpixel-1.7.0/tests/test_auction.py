"""Test Auctions."""
import datetime
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_auction_from_uuid(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_uuid method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&uuid=409a1e0f261a49849493278d6cd9305a",
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            status=200,
            payload={
                "success": True,
                "auctions": [
                    {
                        "_id": "5dcdaf2244f4f4f350c02bf3",
                        "uuid": "409a1e0f261a49849493278d6cd9305a",
                        "auctioneer": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "profile_id": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "coop": ["347ef6c1daac45ed9d1fa02818cf0fb6"],
                        "start": 1573760802637,
                        "end": 1573761102637,
                        "item_name": "Azure Bluet",
                        "item_lore": "§f§lCOMMON",
                        "extra": "Azure Bluet Red Rose",
                        "category": "blocks",
                        "tier": "COMMON",
                        "starting_bid": 1,
                        "item_bytes": {
                            "type": 0,
                            "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaK"
                            + "u0KoLtGtnarRIhTpA/OGfDIwZ4wxUF/IeHiyyto/"
                            + "3eBKIIJQEIDx4qsJaYJK07m6FhG+p9hEdVMV7TXU"
                            + "3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR5XhYhgoIaxmK"
                            + "E8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O5Tnbb"
                            + "gAP05Qaqhk+8AVIrd2eoAAAAA==",
                        },
                        "claimed": True,
                        "claimed_bidders": [],
                        "highest_bid_amount": 7607533,
                        "bids": [
                            {
                                "auction_id": "409a1e0f261a49849493278d6cd9305a",
                                "bidder": "99748e629dee463892f68abf3a780094",
                                "profile_id": "99748e629dee463892f68abf3a780094",
                                "amount": 7607533,
                                "timestamp": 1573760824844,
                            }
                        ],
                    }
                ],
            },
        )
        async for client in hypixel_client:
            data = await client.auction_from_uuid("409a1e0f261a49849493278d6cd9305a")

            assert data is not None
            assert len(data) == 1

            assert not data[0].bin
            assert data[0].id == "5dcdaf2244f4f4f350c02bf3"
            assert data[0].uuid == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
            assert data[0].auctioneer == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
            assert data[0].profile_id == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
            assert len(data[0].coop) == 1
            assert data[0].coop[0] == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
            assert data[0].start == datetime.datetime.fromtimestamp(1573760802.637, tz=datetime.timezone.utc)
            assert data[0].end == datetime.datetime.fromtimestamp(1573761102.637, tz=datetime.timezone.utc)
            assert data[0].item_name == "Azure Bluet"
            assert data[0].item_lore == "§f§lCOMMON"
            assert data[0].extra == "Azure Bluet Red Rose"
            assert data[0].category == "blocks"
            assert data[0].tier == "COMMON"
            assert data[0].starting_bid == 1
            assert data[0].item_bytes == {
                "type": 0,
                "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaK"
                + "u0KoLtGtnarRIhTpA/OGfDIwZ4wxUF/IeHiyyto/"
                + "3eBKIIJQEIDx4qsJaYJK07m6FhG+p9hEdVMV7TXU"
                + "3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR5XhYhgoIaxmK"
                + "E8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O5Tnbb"
                + "gAP05Qaqhk+8AVIrd2eoAAAAA==",
            }
            assert data[0].claimed is True
            assert data[0].claimed_bidders is not None
            assert len(data[0].claimed_bidders) == 0
            assert data[0].highest_bid_amount == 7607533
            assert len(data[0].bids) == 1
            assert data[0].bids[0].auction_id == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
            assert data[0].bids[0].bidder == uuid.UUID("99748e629dee463892f68abf3a780094")
            assert data[0].bids[0].profile_id == uuid.UUID("99748e629dee463892f68abf3a780094")
            assert data[0].bids[0].amount == 7607533
            assert data[0].bids[0].timestamp == datetime.datetime.fromtimestamp(
                1573760824.844, tz=datetime.timezone.utc
            )


@pytest.mark.asyncio
async def test_auction_from_uuid_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_uuid method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&uuid=409a1e0f261a49849493278d6cd9305a",
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            status=200,
            payload={"success": True, "auctions": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.auction_from_uuid("409a1e0f261a49849493278d6cd9305a")

        assert data is None


@pytest.mark.asyncio
async def test_auction_from_profiile(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_profile method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&profile=347ef6c1daac45ed9d1fa02818cf0fb6",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "auctions": [
                    {
                        "_id": "5dcdaf2244f4f4f350c02bf3",
                        "uuid": "409a1e0f261a49849493278d6cd9305a",
                        "auctioneer": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "profile_id": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "coop": ["347ef6c1daac45ed9d1fa02818cf0fb6"],
                        "start": 1573760802637,
                        "end": 1573761102637,
                        "item_name": "Azure Bluet",
                        "item_lore": "§f§lCOMMON",
                        "extra": "Azure Bluet Red Rose",
                        "category": "blocks",
                        "tier": "COMMON",
                        "starting_bid": 1,
                        "item_bytes": {
                            "type": 0,
                            "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaK"
                            + "u0KoLtGtnarRIhTpA/OGfDIwZ4wxUF/IeHiyyto/"
                            + "3eBKIIJQEIDx4qsJaYJK07m6FhG+p9hEdVMV7TXU"
                            + "3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR5XhYhgoIaxmK"
                            + "E8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O5Tnbb"
                            + "gAP05Qaqhk+8AVIrd2eoAAAAA==",
                        },
                        "claimed": True,
                        "bin": True,
                        "claimed_bidders": [],
                        "highest_bid_amount": 7607533,
                        "bids": [
                            {
                                "auction_id": "409a1e0f261a49849493278d6cd9305a",
                                "bidder": "99748e629dee463892f68abf3a780094",
                                "profile_id": "99748e629dee463892f68abf3a780094",
                                "amount": 7607533,
                                "timestamp": 1573760824844,
                            }
                        ],
                    }
                ],
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.auction_from_profile("347ef6c1daac45ed9d1fa02818cf0fb6")

        assert data is not None
        assert len(data) == 1

        assert not data[0].active()
        assert data[0].lowest_possible_bid() == 8748662

        assert data[0].bin
        assert data[0].id == "5dcdaf2244f4f4f350c02bf3"
        assert data[0].uuid == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
        assert data[0].auctioneer == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert data[0].profile_id == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert len(data[0].coop) == 1
        assert data[0].coop[0] == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert data[0].start == datetime.datetime.fromtimestamp(1573760802.637, tz=datetime.timezone.utc)
        assert data[0].end == datetime.datetime.fromtimestamp(1573761102.637, tz=datetime.timezone.utc)
        assert data[0].item_name == "Azure Bluet"
        assert data[0].item_lore == "§f§lCOMMON"
        assert data[0].extra == "Azure Bluet Red Rose"
        assert data[0].category == "blocks"
        assert data[0].tier == "COMMON"
        assert data[0].starting_bid == 1
        assert data[0].item_bytes == {
            "type": 0,
            "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaKu0KoLtGtnar"
            + "RIhTpA/OGfDIwZ4wxUF/IeHiyyto/3eBKIIJQEIDx4qsJaYJK07"
            + "m6FhG+p9hEdVMV7TXU3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR"
            + "5XhYhgoIaxmKE8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O"
            + "5TnbbgAP05Qaqhk+8AVIrd2eoAAAAA==",
        }
        assert data[0].claimed is True
        assert data[0].claimed_bidders is not None
        assert len(data[0].claimed_bidders) == 0
        assert data[0].highest_bid_amount == 7607533
        assert len(data[0].bids) == 1
        assert data[0].bids[0].auction_id == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
        assert data[0].bids[0].bidder == uuid.UUID("99748e629dee463892f68abf3a780094")
        assert data[0].bids[0].profile_id == uuid.UUID("99748e629dee463892f68abf3a780094")
        assert data[0].bids[0].amount == 7607533
        assert data[0].bids[0].timestamp == datetime.datetime.fromtimestamp(1573760824.844, tz=datetime.timezone.utc)


@pytest.mark.asyncio
async def test_auction_from_profile_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_profile method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&profile=347ef6c1daac45ed9d1fa02818cf0fb6",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "auctions": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.auction_from_profile("347ef6c1daac45ed9d1fa02818cf0fb6")

        assert data is None


@pytest.mark.asyncio
async def test_auction_from_player(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_player method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&player=bc581ce675e94a0c88ac9deae06090f0",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "auctions": [
                    {
                        "_id": "5dcdaf2244f4f4f350c02bf3",
                        "uuid": "409a1e0f261a49849493278d6cd9305a",
                        "auctioneer": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "profile_id": "347ef6c1daac45ed9d1fa02818cf0fb6",
                        "coop": ["347ef6c1daac45ed9d1fa02818cf0fb6"],
                        "start": 1573760802637,
                        "end": 2530081735,
                        "item_name": "Azure Bluet",
                        "item_lore": "§f§lCOMMON",
                        "extra": "Azure Bluet Red Rose",
                        "category": "blocks",
                        "tier": "COMMON",
                        "starting_bid": 1,
                        "item_bytes": {
                            "type": 0,
                            "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaK"
                            + "u0KoLtGtnarRIhTpA/OGfDIwZ4wxUF/IeHiyyto/"
                            + "3eBKIIJQEIDx4qsJaYJK07m6FhG+p9hEdVMV7TXU"
                            + "3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR5XhYhgoIaxmK"
                            + "E8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O5Tnbb"
                            + "gAP05Qaqhk+8AVIrd2eoAAAAA==",
                        },
                        "claimed": False,
                        "claimed_bidders": [],
                        "highest_bid_amount": 1,
                        "bids": [
                            {
                                "auction_id": "409a1e0f261a49849493278d6cd9305a",
                                "bidder": "99748e629dee463892f68abf3a780094",
                                "profile_id": "99748e629dee463892f68abf3a780094",
                                "amount": 7607533,
                                "timestamp": 1573760824844,
                            }
                        ],
                    }
                ],
            },
        )
        data = None
        async for client in hypixel_client:
            data = await client.auction_from_player("bc581ce675e94a0c88ac9deae06090f0")

        assert data is not None
        assert len(data) == 1

        assert data[0].active()
        assert data[0].lowest_possible_bid() == 2

        assert not data[0].bin
        assert data[0].id == "5dcdaf2244f4f4f350c02bf3"
        assert data[0].uuid == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
        assert data[0].auctioneer == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert data[0].profile_id == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert len(data[0].coop) == 1
        assert data[0].coop[0] == uuid.UUID("347ef6c1daac45ed9d1fa02818cf0fb6")
        assert data[0].start == datetime.datetime.fromtimestamp(1573760802.637, tz=datetime.timezone.utc)
        assert data[0].end == datetime.datetime.fromtimestamp(2530081735, tz=datetime.timezone.utc)
        assert data[0].item_name == "Azure Bluet"
        assert data[0].item_lore == "§f§lCOMMON"
        assert data[0].extra == "Azure Bluet Red Rose"
        assert data[0].category == "blocks"
        assert data[0].tier == "COMMON"
        assert data[0].starting_bid == 1
        assert data[0].item_bytes == {
            "type": 0,
            "data": "H4sIAAAAAAAAAB2NQQqCQBhGv1ErHaKu0KoLtGtnar"
            + "RIhTpA/OGfDIwZ4wxUF/IeHiyyto/3eBKIIJQEIDx4qsJaYJK07"
            + "m6FhG+p9hEdVMV7TXU3Wh+JWaW6h6ZXhODYGg5/LeZDfxt6nZR"
            + "5XhYhgoIaxmKE8dsZXu20YwuJZfa0hmJrjbo6y134f8pTll5O"
            + "5TnbbgAP05Qaqhk+8AVIrd2eoAAAAA==",
        }
        assert data[0].claimed is False
        assert data[0].claimed_bidders is not None
        assert len(data[0].claimed_bidders) == 0
        assert data[0].highest_bid_amount == 1
        assert len(data[0].bids) == 1
        assert data[0].bids[0].auction_id == uuid.UUID("409a1e0f261a49849493278d6cd9305a")
        assert data[0].bids[0].bidder == uuid.UUID("99748e629dee463892f68abf3a780094")
        assert data[0].bids[0].profile_id == uuid.UUID("99748e629dee463892f68abf3a780094")
        assert data[0].bids[0].amount == 7607533
        assert data[0].bids[0].timestamp == datetime.datetime.fromtimestamp(1573760824.844, tz=datetime.timezone.utc)


@pytest.mark.asyncio
async def test_auction_from_player_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the auction_from_player method."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/skyblock/auction?key={key!s}" + "&player=bc581ce675e94a0c88ac9deae06090f0",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "auctions": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.auction_from_player("bc581ce675e94a0c88ac9deae06090f0")

        assert data is None

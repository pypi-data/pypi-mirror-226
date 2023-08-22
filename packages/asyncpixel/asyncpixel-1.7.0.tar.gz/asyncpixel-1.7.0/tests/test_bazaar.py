"""Test bazaar."""
import datetime
from typing import AsyncGenerator
from uuid import UUID

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
@pytest.mark.parametrize("hypixel_client", ["hypixel_client", "hypixel_client_no_key"], indirect=True)
async def test_bazaar(hypixel_client: AsyncGenerator[Hypixel, None], key: UUID) -> None:
    """Test to check the bazaar returns correct data."""
    with aioresponses() as m:
        m.get(
            "https://api.hypixel.net/skyblock/bazaar",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "lastUpdated": 1590854517479,
                "products": {
                    "INK_SACK:3": {
                        "product_id": "INK_SACK:3",
                        "sell_summary": [
                            {"amount": 20569, "pricePerUnit": 4.2, "orders": 1},
                            {"amount": 140326, "pricePerUnit": 3.8, "orders": 2},
                        ],
                        "buy_summary": [
                            {"amount": 640, "pricePerUnit": 4.8, "orders": 1},
                            {"amount": 640, "pricePerUnit": 4.9, "orders": 1},
                            {"amount": 25957, "pricePerUnit": 5, "orders": 3},
                        ],
                        "quick_status": {
                            "productId": "INK_SACK:3",
                            "sellPrice": 4.2,
                            "sellVolume": 409855,
                            "sellMovingWeek": 8301075,
                            "sellOrders": 11,
                            "buyPrice": 4.99260315136572,
                            "buyVolume": 1254854,
                            "buyMovingWeek": 5830656,
                            "buyOrders": 85,
                        },
                    }
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.bazaar()

        assert data is not None

        assert data.last_updated == datetime.datetime.fromtimestamp(1590854517.479, tz=datetime.timezone.utc)
        assert len(data.bazaar_items) == 1

        assert data.bazaar_items[0].product_id == "INK_SACK:3"

        assert len(data.bazaar_items[0].sell_summary) == 2
        assert data.bazaar_items[0].sell_summary[0].amount == 20569
        assert data.bazaar_items[0].sell_summary[0].price_per_unit == 4.2
        assert data.bazaar_items[0].sell_summary[0].orders == 1

        assert data.bazaar_items[0].sell_summary[1].amount == 140326
        assert data.bazaar_items[0].sell_summary[1].price_per_unit == 3.8
        assert data.bazaar_items[0].sell_summary[1].orders == 2

        assert len(data.bazaar_items[0].buy_summary) == 3
        assert data.bazaar_items[0].buy_summary[0].amount == 640
        assert data.bazaar_items[0].buy_summary[0].price_per_unit == 4.8
        assert data.bazaar_items[0].buy_summary[0].orders == 1

        assert data.bazaar_items[0].buy_summary[1].amount == 640
        assert data.bazaar_items[0].buy_summary[1].price_per_unit == 4.9
        assert data.bazaar_items[0].buy_summary[1].orders == 1

        assert data.bazaar_items[0].buy_summary[2].amount == 25957
        assert data.bazaar_items[0].buy_summary[2].price_per_unit == 5
        assert data.bazaar_items[0].buy_summary[2].orders == 3

        assert data.bazaar_items[0].quick_status.product_id == "INK_SACK:3"
        assert data.bazaar_items[0].quick_status.sell_price == 4.2
        assert data.bazaar_items[0].quick_status.sell_volume == 409855
        assert data.bazaar_items[0].quick_status.sell_moving_week == 8301075
        assert data.bazaar_items[0].quick_status.sell_orders == 11
        assert data.bazaar_items[0].quick_status.buy_price == 4.99260315136572
        assert data.bazaar_items[0].quick_status.buy_volume == 1254854
        assert data.bazaar_items[0].quick_status.buy_moving_week == 5830656
        assert data.bazaar_items[0].quick_status.buy_orders == 85

        assert len(data.bazaar_items[0].buy_summary) == 3

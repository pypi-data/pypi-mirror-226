"""Test utilss."""
import pytest

from asyncpixel.models.utils import safe_divide, to_camel
from asyncpixel.utils import get_rank, validate_game_type


@pytest.mark.asyncio
async def test_get_rank() -> None:
    """Test get rank."""
    assert (
        get_rank(
            prefix_raw="§a§l[§bVIP§a§l]",
        )
        == "VIP"
    )
    assert get_rank(rank="OWNER") == "OWNER"
    assert get_rank(monthly_package_rank="MVP++") == "MVP++"
    assert get_rank(new_package_rank="MVP++") == "MVP++"
    assert get_rank(package_rank="MVP++") == "MVP++"


@pytest.mark.asyncio
async def test_safe_divide() -> None:
    """Test safe divide."""
    assert safe_divide(dividend=1, divisor=1) == 1
    assert safe_divide(dividend=1, divisor=0) == float("inf")


@pytest.mark.asyncio
async def test_to_camel() -> None:
    """Test to camel."""
    assert to_camel("test_string") == "testString"
    assert to_camel("test_string_2") == "testString2"


@pytest.mark.asyncio
async def test_validate_game_type() -> None:
    """Test validate game type."""
    assert validate_game_type(2).id == 2
    assert validate_game_type("QUAKECRAFT").id == 2

    with pytest.raises(StopIteration):
        validate_game_type(1)

    with pytest.raises(StopIteration):
        validate_game_type("NULL")

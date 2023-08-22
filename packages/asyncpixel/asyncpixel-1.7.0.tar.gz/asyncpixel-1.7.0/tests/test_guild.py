"""Test guild."""
import datetime
import uuid
from typing import AsyncGenerator

import pytest
from aioresponses import aioresponses

from asyncpixel import Hypixel


@pytest.mark.asyncio
async def test_guild_by_id(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_id method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&id=52e57a1c0cf2e250d1cd00f8",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                            "questParticipation": 4,
                            "mutedTill": 1399507406038,
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_id("52e57a1c0cf2e250d1cd00f8")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation == 4
        assert data.members[0].muted_till == datetime.datetime.fromtimestamp(1399507406.038, tz=datetime.timezone.utc)
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is False
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }


@pytest.mark.asyncio
async def test_guild_by_id_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_id method returns correct data when not found."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&id=52e57a1c0cf2e250d1cd00f8",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "guild": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_id("52e57a1c0cf2e250d1cd00f8")

        assert data is None


@pytest.mark.asyncio
async def test_guild_by_name(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_name method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&name=The%20Sloths",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                            "questParticipation": 4,
                            "mutedTill": 1399507406038,
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_name("The Sloths")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation == 4
        assert data.members[0].muted_till == datetime.datetime.fromtimestamp(1399507406.038, tz=datetime.timezone.utc)
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is False
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }


@pytest.mark.asyncio
async def test_guild_by_name_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_name method returns correct data when not found."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&name=The%20Sloths",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "guild": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_name("The Sloths")

        assert data is None


@pytest.mark.asyncio
async def test_guild_by_player(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_player method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}" + "&player=f7c77d999f154a66a87dc4a51ef30d19",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                            "questParticipation": 4,
                            "mutedTill": 1399507406038,
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_player("f7c77d999f154a66a87dc4a51ef30d19")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation == 4
        assert data.members[0].muted_till == datetime.datetime.fromtimestamp(1399507406.038, tz=datetime.timezone.utc)
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is False
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }


@pytest.mark.asyncio
async def test_guild_by_player_none(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_player method returns correct data when not found."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}" + "&player=f7c77d999f154a66a87dc4a51ef30d19",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={"success": True, "guild": None},
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_player("f7c77d999f154a66a87dc4a51ef30d19")

        assert data is None


@pytest.mark.asyncio
async def test_guild_by_id_no_mute_quest(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_id method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&id=52e57a1c0cf2e250d1cd00f8",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_id("52e57a1c0cf2e250d1cd00f8")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation is None
        assert data.members[0].muted_till is None
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is False
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }


@pytest.mark.asyncio
async def test_guild_by_name_no_mute_quest(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_name method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}&name=The%20Sloths",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_name("The Sloths")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation is None
        assert data.members[0].muted_till is None
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is False
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }


@pytest.mark.asyncio
async def test_guild_by_player_no_mute_quest(hypixel_client: AsyncGenerator[Hypixel, None], key: uuid.UUID) -> None:
    """Test to check the guild_by_player method returns correct data."""
    with aioresponses() as m:
        m.get(
            f"https://api.hypixel.net/guild?key={key!s}" + "&player=f7c77d999f154a66a87dc4a51ef30d19",
            status=200,
            headers={
                "RateLimit-Limit": "120",
                "RateLimit-Remaining": "119",
                "RateLimit-Reset": "8",
            },
            payload={
                "success": True,
                "guild": {
                    "_id": "52e57a1c0cf2e250d1cd00f8",
                    "created": 1390770716373,
                    "name": "The Sloths",
                    "name_lower": "the sloths",
                    "description": "The sloths",
                    "tag": "SLOTH",
                    "tagColor": "DARK_AQUA",
                    "exp": 2238673,
                    "members": [
                        {
                            "uuid": "f7c77d999f154a66a87dc4a51ef30d19",
                            "rank": "GUILDMASTER",
                            "joined": 1390770716373,
                            "expHistory": {"2020-05-25": 108, "2020-05-24": 404},
                        }
                    ],
                    "achievements": {
                        "ONLINE_PLAYERS": 4,
                        "EXPERIENCE_KINGS": 40062,
                        "WINNERS": 2,
                    },
                    "ranks": [
                        {
                            "name": "Member",
                            "default": True,
                            "created": 1,
                            "priority": 1,
                            "tag": "Member",
                        }
                    ],
                    "joinable": True,
                    "legacyRanking": 10446,
                    "publiclyListed": False,
                    "preferredGames": ["ARCADE", "SPEED_UHC", "UHC"],
                    "chatMute": 1590703490783,
                    "guildExpByGameType": {
                        "TNTGAMES": 1312,
                        "VAMPIREZ": 4495,
                        "ARCADE": 10285,
                    },
                },
            },
        )

        data = None
        async for client in hypixel_client:
            data = await client.guild_by_player("f7c77d999f154a66a87dc4a51ef30d19")

        assert data is not None
        assert data.id == "52e57a1c0cf2e250d1cd00f8"
        assert data.created == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.name == "The Sloths"
        assert data.name_lower == "the sloths"
        assert data.description == "The sloths"
        assert data.tag == "SLOTH"
        assert data.tag_color == "DARK_AQUA"
        assert data.exp == 2238673
        assert len(data.members) == 1

        assert data.members[0].uuid == uuid.UUID("f7c77d999f154a66a87dc4a51ef30d19")
        assert data.members[0].rank == "GUILDMASTER"
        assert data.members[0].joined == datetime.datetime.fromtimestamp(1390770716.373, tz=datetime.timezone.utc)
        assert data.members[0].exp_history == {"2020-05-25": 108, "2020-05-24": 404}
        assert data.members[0].quest_participation is None
        assert data.members[0].muted_till is None
        assert data.achievements == {
            "ONLINE_PLAYERS": 4,
            "EXPERIENCE_KINGS": 40062,
            "WINNERS": 2,
        }
        assert data.ranks is not None
        assert len(data.ranks) == 1
        assert data.ranks[0].name == "Member"
        assert data.ranks[0].default is True
        assert data.ranks[0].created == 1
        assert data.ranks[0].priority == 1
        assert data.ranks[0].tag == "Member"
        assert data.joinable is True
        assert data.legacy_ranking is not None
        assert data.legacy_ranking == 10446
        assert data.publicly_listed is not None
        assert data.publicly_listed is False
        assert data.preferred_games is not None
        assert data.preferred_games == ["ARCADE", "SPEED_UHC", "UHC"]
        assert data.chat_mute is not None
        assert data.chat_mute == datetime.datetime.fromtimestamp(1590703490.783, tz=datetime.timezone.utc)
        assert data.guild_exp_by_game_type is not None
        assert data.guild_exp_by_game_type == {
            "TNTGAMES": 1312,
            "VAMPIREZ": 4495,
            "ARCADE": 10285,
        }

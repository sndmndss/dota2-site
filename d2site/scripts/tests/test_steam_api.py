import pytest
from d2site.scripts.steam_api_requests import SteamWebApi


@pytest.mark.asyncio
async def test_get_common_matches():
    matches = await SteamWebApi.get_common_matches(875292579, 311360822)
    assert len(matches) > 0

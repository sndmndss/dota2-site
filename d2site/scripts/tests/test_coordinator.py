import pytest
from d2site.scripts import game_coordinator_interface


@pytest.mark.asyncio
async def test_match_history():
    match_id = 7496660306
    result = await game_coordinator_interface.get_match_history(match_id)
    assert result is not None


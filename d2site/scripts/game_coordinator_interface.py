from .coordinator import Coordinator


async def get_player_statistic(player_steamid3: int) -> (dict, str):
    """
    Returns the data for the given account.

    :param: player_steamid3: ID of the account
    :return: A list of dictionaries containing statistics for last 20 matches
    """
    dota = await Coordinator.connection()
    dota.request_player_stats(player_steamid3)
    _, data = dota.wait_event("player_stats", timeout=5, raises=True)
    return data


async def get_match_history(match_id: int):
    """
    Returns match details for a given match.

    :param match_id: ID of the match.
    :return: A list of dictionaries containing match data.
    """
    dota = await Coordinator.connection()
    dota.request_match_details(match_id)
    data = dota.wait_event("match_details", timeout=10, raises=True)
    return data

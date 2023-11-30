from dota2.proto_enums import EGCItemMsg
from .coordinator import Coordinator


async def request_data(account_id: int) -> (dict, str):
    """
    Returns the data for the given account.

    :param: account_id: ID of the account
    :type account_id: :class:`int`
    :return: data`
    :rtype: :class:`tuple`: (:class:`dict`, :class:`str`)
    """
    dota = await Coordinator.connect()
    dota.request_player_stats(account_id)
    _, data = dota.wait_event("player_stats", timeout=5, raises=True)
    player_name = await request_players_name(dota, account_id)
    return data, player_name


async def request_players_name(dota, account_id: int) -> str:
    """
    Returns the player name for the given account id.

    :param dota: Dota 2 API object
    :type dota: :class:`Dota2Client`
    :param account_id: Account ID to get data for
    :type account_id: :class:`int`
    :return: Player name
    :rtype: str
    """
    dota.send_job(EGCItemMsg.EMsgClientToGCLookupAccountName, {'account_id': account_id})
    name = dota.wait_msg(EGCItemMsg.EMsgClientToGCLookupAccountNameResponse, timeout=5, raises=True)
    return name.account_name

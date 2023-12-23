import requests
from decouple import config
from d2site.scripts.helpers import steamid3_to_steamid


class BadRequest(Exception):
    """Exception raised when a bad request is made to an external API."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class HistoryIsHidden(Exception):
    """Exception raised when match history is hidden or damaged"""

    def __init__(self, message):
        super().__init__(message)


class DataIsDamaged(Exception):
    """Exception raised when data is corrupted"""

    def __init__(self, message="Data is corrupted, please, try again"):
        super().__init__(message)


class SteamWebApi:
    default_url = 'https://api.steampowered.com/'
    GetMatchHistory_url = 'IDOTA2Match_570/GetMatchHistory/v1'
    GetMatchDetails_url = 'IDOTA2Match_570/GetMatchDetails/v1'
    GetPlayerSummaries_url = 'ISteamUser/GetPlayerSummaries/v0002/'
    MATCHES_REQUESTED = 10

    @classmethod
    async def _make_request(cls, url, params):
        full_url = cls.default_url + url
        try:
            response = requests.get(full_url, params=params)
            response.raise_for_status()  # Will raise HTTPError for bad status codes
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise BadRequest(f"Bad request to SteamWebApi: {e}", e.response.status_code)
        except requests.exceptions.RequestException as e:
            raise BadRequest(f"Error making request to SteamWebApi: {e}")

    @classmethod
    async def get_match_history(cls, player_steamid3: int, last_match_id=0):
        """Returns 10 matches from last_match_id"""
        params = {"key": config("STEAM_API_KEY"),
                  "account_id": str(player_steamid3),
                  "start_at_match_id": last_match_id,
                  "matches_requested": cls.MATCHES_REQUESTED}
        match_history = await cls._make_request(url=cls.GetMatchHistory_url, params=params)
        if match_history["result"]["status"] == 1:
            match_history = match_history["result"]["matches"]
        elif match_history["result"]["status"] == 15:
            raise HistoryIsHidden("History is hidden")
        else:
            raise DataIsDamaged()
        return match_history

    @classmethod
    async def get_match_details(cls, match_id):
        params = {"key": config("STEAM_API_KEY"),
                  "match_id": match_id,
                  "include_persona_names": True}
        match_details = await cls._make_request(url=cls.GetMatchDetails_url, params=params)
        match_details = match_details["result"]  # TODO: Watch result codes
        return match_details

    @classmethod
    async def get_common_matches(cls, owner_steamid3: int, requester_steamid3: int):
        r = await cls.get_match_history(requester_steamid3)
        common_matches_ids = []
        for match in r:
            for player in match["players"]:
                if player["account_id"] == owner_steamid3:
                    common_matches_ids.append((match["match_id"], str(match["match_id"])))
        return common_matches_ids

    @classmethod
    async def get_player_name(cls, steamid3: int):
        steamid = steamid3_to_steamid(steamid3)
        params = {"key": config("STEAM_API_KEY"),
                  "steamids": steamid}
        player_summaries = await cls._make_request(url=cls.GetPlayerSummaries_url, params=params)
        if bool(player_summaries["response"]["players"]):
            player_name = player_summaries["response"]["players"][0]["personaname"]
            return player_name
        else:
            raise DataIsDamaged()

    @classmethod
    async def player_exists(cls, steamid3: int):
        steamid = steamid3_to_steamid(steamid3)
        params = {"key": config("STEAM_API_KEY"),
                  "steamids": steamid}
        player_summaries = await cls._make_request(url=cls.GetPlayerSummaries_url, params=params)
        return bool(player_summaries["response"]["players"])

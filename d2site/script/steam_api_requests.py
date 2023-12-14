import requests
from decouple import config


class SteamWebApi:
    default_url = 'https://api.steampowered.com/'
    GetMatchHistory_url = 'IDOTA2Match_570/GetMatchHistory/v1'
    GetMatchDetails_url = 'IDOTA2Match_570/GetMatchDetails/v1'
    MATCHES_REQUESTED = 10

    @classmethod
    async def get_match_history(cls, account_id: int, last_match_id=0):
        match_history_request = requests.get(cls.default_url + cls.GetMatchHistory_url,
                                             params={"key": config("STEAM_API_KEY"),
                                                     "account_id": str(account_id),
                                                     "start_at_match_id": last_match_id,
                                                     "matches_requested": cls.MATCHES_REQUESTED})
        if match_history_request.json()["result"]["status"] != 15:
            match_history = match_history_request.json()["result"]["matches"]
        else:
            return 0
        return match_history

    @classmethod
    async def get_match_details(cls, match_id):
        match_details_request = requests.get(cls.default_url + cls.GetMatchDetails_url,
                                             params={"key": config("STEAM_API_KEY"),
                                                     "match_id": match_id,
                                                     "include_persona_names": True})
        match_details = match_details_request.json()["result"]
        return match_details




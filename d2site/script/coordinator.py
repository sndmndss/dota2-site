from steam.client import SteamClient
from dota2.client import Dota2Client
from d2site.settings import STEAM_LOGIN, STEAM_PASSWORD


class Coordinator:
    _is_connected = None
    client = SteamClient()
    dota = None

    @classmethod
    async def connect(cls):
        if cls._is_connected:
            return cls.dota
        if not cls.client.logged_on:
            cls.client.login(username=STEAM_LOGIN, password=STEAM_PASSWORD)
            cls.dota = Dota2Client(cls.client)
            cls.dota.launch()
        cls._is_connected = True
        return cls.dota

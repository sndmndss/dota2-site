from steam.client import SteamClient
from dota2.client import Dota2Client
from decouple import config


STEAM_LOGIN = config("STEAM_LOGIN")
STEAM_PASSWORD = config("STEAM_PASSWORD")


class LoginError(Exception):
    """Exception raised when trying to log in is failed"""
    pass


class Coordinator:
    _is_connected = None
    client = SteamClient()
    dota = None

    @classmethod
    async def connection(cls):
        """Makes the connection with steam and dota 2 coordinator"""
        if cls._is_connected:
            return cls.dota
        if not cls.client.logged_on:
            cls.client.login(username=STEAM_LOGIN, password=STEAM_PASSWORD)
            cls.dota = Dota2Client(cls.client)
            cls.dota.launch()
            if not cls.dota.steam.logged_on:
                raise LoginError("We have unexpected temporary problem with Steam")
            else:
                cls._is_connected = True
        return cls.dota

    @classmethod
    async def disconnect(cls):
        cls.client.disconnect()
        cls.dota.exit()

import math


def steamid_to_steamid3(steamid64: int) -> int:
    """Converts a steamid64 to a steamID3"""
    lowest_bit_position = math.log2(steamid64 & -steamid64)
    mask = 0x7FFFFFFF
    shifted_mask = mask << int(lowest_bit_position)
    steam_id3 = (steamid64 & shifted_mask) >> int(lowest_bit_position)
    return steam_id3


def steamid3_to_steamid(steamid3: int) -> int:
    """Converts a steamID3 to a steamid"""
    y = steamid3 % 2
    z = steamid3 // 2
    steamid_constant = 76561197960265728
    steamid64 = (z * 2) + y + steamid_constant
    return steamid64

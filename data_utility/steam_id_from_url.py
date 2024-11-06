from steam.steamid import SteamID, steam64_from_url


def get_steam_id_from_url(url: str):
    try:
        steam_id = SteamID(url).as_64
        if steam_id:
            return steam_id
    except:
        pass
    try:
        steam_id = steam64_from_url(url)
        if steam_id:
            return steam_id
    except:
        pass
    return None

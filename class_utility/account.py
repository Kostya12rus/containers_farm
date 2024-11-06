from data_utility import get_steam_profile_info

class Account:
    def __init__(self, steam_id64: str | int, steam_avatar_url: str = '', steam_nickname: str = '', is_ready_register: bool = False, last_launch: int = 0):
        self.steam_id64 = str(steam_id64)
        self.profile_url = f'https://steamcommunity.com/profiles/{self.steam_id64}'
        self.steam_avatar_url = steam_avatar_url
        self.steam_nickname = steam_nickname
        self.last_launch = last_launch
        self.is_ready_register = bool(is_ready_register)

    def load_account_info(self):
        steam_profile_data = get_steam_profile_info(url_profile=self.profile_url)
        self.steam_avatar_url = steam_profile_data.get('avatarFull', None)
        self.steam_nickname = steam_profile_data.get('steamID', None)
        if not self.steam_nickname:
            self.steam_nickname = 'Unknown Nickname'
        self.save_account_info()

    def save_account_info(self):
        from sql_utility import sql_manager
        sql_manager.account_save(account=self)

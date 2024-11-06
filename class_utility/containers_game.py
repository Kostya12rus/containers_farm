import time
import threading
import requests
from collections import deque


class Containers:
    def __init__(self, steam_id64: str):
        self.steam_id64 = steam_id64

        self.base_url = 'http://45.128.205.193:8000'
        self.headers = {"Content-Type": "application/json"}

        self.is_in_work = False
        self.is_ready_register = False
        self.is_auto_spin_roulette = False
        self.is_abuss_spin_roulette = False
        self.delay_add_money = 0.01

        self.account_money = 0
        self.roulette_price = 1000

        self.add_money_success = 0
        self.add_money_total = 0
        self.add_money_rps = 0
        self.add_money_rps_list = deque(maxlen=30)
        self.__add_money_lock = threading.Lock()

        self.roulette_spin_result = []
        self.__roulette_spin_result_lock = threading.Lock()
        self.__roulette_spin_lock = threading.Lock()


    def add_money(self):
        try:
            url = f"{self.base_url}/addMoney?steamID={self.steam_id64}"
            req = requests.post(url, headers=self.headers, timeout=10)
            self.add_money_total += 1
            if not req.ok: return
            self.add_money_success += 1
            with self.__add_money_lock:
                self.add_money_rps += 1
        except:
            pass
    def add_money_pool(self):
        while self.is_in_work:
            with self.__roulette_spin_lock:
                threading.Thread(target=self.add_money, daemon=True).start()
                time.sleep(self.delay_add_money)

    def __spin_roulette(self, url: str):
        try:
            response = requests.post(url, headers=self.headers, timeout=10)
            response_json = response.json()

            with self.__roulette_spin_result_lock:
                self.roulette_spin_result.append(response_json)
            return response_json
        except:
            pass
        return {}
    def spin_roulette(self):
        url = f"{self.base_url}/spinRoulette?steamID={self.steam_id64}"
        return self.__spin_roulette(url)
    def abuss_spin_roulette(self, count: int = 20) -> list[dict]:
        url = f"{self.base_url}/spinRoulette?steamID={self.steam_id64}"

        self.roulette_spin_result = []
        threads = []
        with self.__roulette_spin_lock:
            time.sleep(1)
            for _ in range(count):
                thread = threading.Thread(target=self.__spin_roulette, args=(url,), daemon=True)
                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

        return self.roulette_spin_result

    def __open_container(self, url):
        try:
            response = requests.post(url, headers=self.headers, timeout=10)
            return response.json()
        except:
            pass
    def open_container(self, case_id: int | str, case_number: int):
        url = f"{self.base_url}/openContainer?steamID={self.steam_id64}&caseID={case_id}&caseNUMBER={case_number}"
        return self.__open_container(url)
    def abuss_open_container(self, case_id: int | str, case_number: int, count: int = 20):
        url = f"{self.base_url}/openContainer?steamID={self.steam_id64}&caseID={case_id}&caseNUMBER={case_number}"

        threads = []
        for _ in range(count):
            thread = threading.Thread(target=self.__open_container, args=(url,), daemon=True)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def get_data(self) -> dict:
        try:
            url = f"{self.base_url}/getData?steamID={self.steam_id64}"
            response = requests.get(url, headers=self.headers)
            return response.json()
        except:
            pass
        return {}

    def check(self) -> bool:
        try:
            url = f"{self.base_url}/check?steamID={self.steam_id64}"
            response = requests.get(url, headers=self.headers)
            response_json = response.json()
            return response_json.get('success', 'false') == 'true'
        except:
            pass
        return False

    def add_player(self) -> bool:
        try:
            url = f"{self.base_url}/addPlayer?steamID={self.steam_id64}"
            response = requests.post(url, headers=self.headers)
            response_json = response.json()
            return 'message' in response_json
        except:
            pass
        return False

    def apply_promo(self, promo_code: str = None) -> bool:
        if not promo_code: return {}
        try:
            url = f"{self.base_url}/applyPromo?steamID={self.steam_id64}&promoCode={promo_code}"
            response = requests.post(url, headers=self.headers)
            response_json = response.json()
            return response_json.get('success', False)
        except:
            pass
        return {}

    def update_stats_pool(self):
        last_update = time.time() + 1
        while self.is_in_work:
            time.sleep(0.1)
            time_time = time.time()
            if last_update <= time_time:
                with self.__add_money_lock:
                    self.add_money_rps_list.append(self.add_money_rps)
                    self.add_money_rps = 0
                    last_update = time_time + 1

                self.update_data_account()


    def register_account(self):
        if self.is_ready_register: return
        self.is_ready_register = True if self.check() else self.add_player()

    def update_data_account(self):
        data = self.get_data()
        self.account_money = data.get('PlayerMoney', 0)
        self.roulette_price = data.get('PlayerSpinCost', 1000)

    def start(self):
        if self.is_in_work: return
        self.is_in_work = True
        self.update_data_account()
        threading.Thread(target=self.add_money_pool, daemon=True).start()
        threading.Thread(target=self.update_stats_pool, daemon=True).start()

    def stop(self):
        if not self.is_in_work: return
        self.is_in_work = False

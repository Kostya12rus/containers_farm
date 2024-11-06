import threading
import time

import flet as ft
from sql_utility import sql_manager, config
from flet_utility.pages.base import BasePage, Title
from data_utility import get_steam_id_from_url
from class_utility import Account, Containers
from logger_utility import logger


class AccountContent(ft.Row):
    def __init__(self, account: Account):
        super().__init__()
        self.expand = True
        self.spacing = 3
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.START

        config.register_callback('hide_nickname', self.on_change_hide_nickname)
        config.register_callback('hide_avatar', self.on_change_hide_avatar)
        config.register_callback('delay_add_money', self.on_change_delay_add_money)
        config.register_callback('auto_use_roulette', self.on_change_auto_use_roulette)
        config.register_callback('abuss_use_roulette', self.on_change_abuss_use_roulette)

        self.is_widget_work = False
        self.account = account
        self.container_game = Containers(self.account.steam_id64)
        self.container_game.is_ready_register = self.account.is_ready_register


        self.avatar_image = ft.Image(width=20, height=20)
        self.avatar_image.src = self.account.steam_avatar_url
        self.avatar_image.fit = ft.ImageFit.CONTAIN

        self.steam_nickname = ft.Text(size=15, max_lines=1, selectable=True, width=100)
        self.steam_nickname.tooltip = 'Nickname Steam'
        self.steam_nickname.value = self.account.steam_nickname
        self.steam_nickname.color = ft.colors.BLUE
        self.steam_nickname.weight = ft.FontWeight.BOLD

        self.is_already_registered = ft.Icon(size=20)
        self.is_already_registered.tooltip = 'Account is already registered?'
        self.is_already_registered.name = ft.icons.CLOSE if not self.account.is_ready_register else ft.icons.CHECK
        self.is_already_registered.color = ft.colors.RED if not self.account.is_ready_register else ft.colors.GREEN

        self.income_balance = ft.Text(size=15, max_lines=1, expand=True)
        self.income_balance.tooltip = 'Income balance: Requests per second | Balance'
        self.income_balance.value = "Income: ?rps | ?$"
        self.income_balance.color = ft.colors.GREEN
        self.income_balance.text_align = ft.TextAlign.RIGHT

        self.income_tatal = ft.Text(size=15, max_lines=1, expand=True)
        self.income_tatal.tooltip = 'Total Requests: Requests per second | Balance'
        self.income_tatal.value = "Total: ?rps | ?$"
        self.income_tatal.color = ft.colors.BLUE
        self.income_tatal.text_align = ft.TextAlign.RIGHT

        self.balance = ft.Text(size=15, max_lines=1, expand=True)
        self.balance.tooltip = 'Account balance'
        self.balance.value = "Balance: ?$"
        self.balance.color = ft.colors.GREEN
        self.balance.text_align = ft.TextAlign.RIGHT

        self.roulette_price = ft.Text(size=15, max_lines=1, expand=True)
        self.roulette_price.tooltip = 'Price roulette spin'
        self.roulette_price.value = "Price: ?$"
        self.roulette_price.color = ft.colors.RED
        self.roulette_price.text_align = ft.TextAlign.RIGHT

        self.button_spin_roulette = ft.FilledTonalButton(height=20)
        self.button_spin_roulette.tooltip = 'Spin roulette'
        self.button_spin_roulette.text = 'Spin roulette'
        self.button_spin_roulette.disabled = True
        self.button_spin_roulette.on_click = self.__on_click_button_buy_roulette

        self.button_icon_start = ft.IconButton(height=20)
        self.button_icon_start.tooltip = 'Start | stop farming'
        self.button_icon_start.icon = ft.icons.PLAY_CIRCLE
        self.button_icon_start.icon_color = ft.colors.GREEN
        self.button_icon_start.visual_density = ft.VisualDensity.COMPACT
        self.button_icon_start.style = ft.ButtonStyle(padding=ft.padding.all(0), icon_size=20, alignment=ft.alignment.center)
        self.button_icon_start.on_click = self.start_or_stop

        self.button_icon_delete = ft.IconButton(height=20)
        self.button_icon_delete.tooltip = 'Delete account'
        self.button_icon_delete.icon = ft.icons.DELETE
        self.button_icon_delete.icon_color = ft.colors.RED
        self.button_icon_delete.visual_density = ft.VisualDensity.COMPACT
        self.button_icon_delete.style = ft.ButtonStyle(padding=ft.padding.all(0), icon_size=20, alignment=ft.alignment.center)

        self.controls = [
            self.avatar_image,
            self.steam_nickname,
            self.is_already_registered,
            self.income_balance,
            self.income_tatal,
            self.balance,
            self.roulette_price,
            self.button_spin_roulette,
            self.button_icon_start,
            ft.VerticalDivider(width=20),
            self.button_icon_delete,
            ft.VerticalDivider(width=10),
        ]

    def start_or_stop(self, *args):
        self.container_game.register_account()
        if not self.container_game.is_ready_register: return

        self.is_already_registered.name = ft.icons.CLOSE if not self.container_game.is_ready_register else ft.icons.CHECK
        self.is_already_registered.color = ft.colors.RED if not self.container_game.is_ready_register else ft.colors.GREEN

        if not self.container_game.is_in_work:
            self.container_game.start()
            self.button_icon_start.icon = ft.icons.PAUSE_CIRCLE
            self.button_icon_start.icon_color = ft.colors.RED
            self.account.last_launch = int(time.time())
            self.account.is_ready_register = self.container_game.is_ready_register
            self.account.save_account_info()
        else:
            self.container_game.stop()
            self.button_icon_start.icon = ft.icons.PLAY_CIRCLE
            self.button_icon_start.icon_color = ft.colors.GREEN

        if self.page: self.update()

    def __on_click_button_buy_roulette(self, *args):
        if self.container_game.is_abuss_spin_roulette:
            count_request = 40
            results: list[dict] = self.container_game.abuss_spin_roulette(count_request)
            for result in results:
                if 'success' not in result or not result.get('success', False): continue
                if result.get('item', '') != 'case': continue
                logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette {result}')
            success_count = len([result for result in results if 'success' in result and result.get('success', False)])
            case_count = len([result for result in results if 'item' in result and result.get('item', '') == 'case'])
            logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette: request {count_request}, success {success_count}, get case {case_count}')
        else:
            result = self.container_game.spin_roulette()
            if 'success' in result and result.get('success', False):
                logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette {result}')

        self.container_game.update_data_account()
        self.__update_game_info()
        if self.page: self.update()

    def __update_game_info(self, *args):
        self.is_already_registered.name = ft.icons.CLOSE if not self.container_game.is_ready_register else ft.icons.CHECK
        self.is_already_registered.color = ft.colors.RED if not self.container_game.is_ready_register else ft.colors.GREEN

        avg_success_rps = int(
            sum(self.container_game.add_money_rps_list) / len(self.container_game.add_money_rps_list)
        ) if self.container_game.add_money_rps_list else 0
        self.income_balance.value = f"Income: {avg_success_rps}rps | {avg_success_rps*50}$"
        self.income_tatal.value = f"Total: {self.container_game.add_money_total}rps | {self.container_game.add_money_total*50}$"
        self.balance.value = f"Balance: {self.container_game.account_money}$"
        self.roulette_price.value = f"Price: {self.container_game.roulette_price}$"

        self.button_spin_roulette.disabled = self.container_game.roulette_price > self.container_game.account_money

    def __update_pool(self):
        while self.is_widget_work:
            time.sleep(0.2)
            if not self.container_game.is_in_work: continue
            self.__update_game_info()

            if self.container_game.is_auto_spin_roulette:
                if self.container_game.roulette_price <= self.container_game.account_money:
                    if self.container_game.is_abuss_spin_roulette:
                        count_request = 40
                        results: list[dict] = self.container_game.abuss_spin_roulette(count_request)
                        for result in results:
                            if 'success' not in result or not result.get('success', False): continue
                            if result.get('item', '') != 'case': continue
                            logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette {result}')
                        success_count = len([result for result in results if 'success' in result and result.get('success', False)])
                        case_count = len([result for result in results if 'item' in result and result.get('item', '') == 'case'])
                        logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette: request {count_request}, success {success_count}, get case {case_count}')
                    else:
                        result = self.container_game.spin_roulette()
                        if 'success' in result and result.get('success', False):
                            logger.info(f'{self.account.steam_nickname}[{self.account.steam_id64}]: spin roulette {result}')
            if self.page: self.update()

    def will_unmount(self):
        self.is_widget_work = False
    def did_mount(self):
        if self.is_widget_work: return
        self.is_widget_work = True
        threading.Thread(target=self.__update_pool, daemon=True).start()

    def on_change_hide_nickname(self, is_hide_nickname):
        self.steam_nickname.value = self.account.steam_nickname[:4] + '***' if is_hide_nickname else self.account.steam_nickname
        if self.page: self.steam_nickname.update()
    def on_change_hide_avatar(self, is_hide_avatar):
        self.avatar_image.visible = not is_hide_avatar
        if self.page: self.avatar_image.update()
    def on_change_delay_add_money(self, value):
        self.container_game.delay_add_money = value
    def on_change_auto_use_roulette(self, value):
        self.container_game.is_auto_spin_roulette = value
    def on_change_abuss_use_roulette(self, value):
        self.container_game.is_abuss_spin_roulette = value

class AccountsList(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 0

        config.register_callback('hide_nickname', self.__on_change_hide_nickname)
        config.register_callback('hide_avatar', self.__on_change_hide_avatar)
        config.register_callback('delay_add_money', self.__on_change_delay_add_money)
        config.register_callback('auto_use_roulette', self.__on_change_auto_use_roulette)
        config.register_callback('abuss_use_roulette', self.__on_change_abuss_use_roulette)
        self.__setting_hide_nickname = bool(config.hide_nickname)
        self.__setting_hide_avatar = bool(config.hide_avatar)
        self.__setting_delay_add_money = config.delay_add_money
        self.__setting_auto_use_roulette = bool(config.auto_use_roulette)
        self.__setting_abuss_use_roulette = bool(config.abuss_use_roulette)

        self.profile_url_add_field = ft.TextField(dense=True, content_padding=5, max_lines=1, multiline=False, expand=True)
        self.profile_url_add_field.label = 'Steam URL profile | SteamID'
        self.profile_url_add_field.border_color = ft.colors.GREY

        self.profile_add_button = ft.FilledTonalButton(height=25)
        self.profile_add_button.text = 'Add Account'
        self.profile_add_button.icon = ft.icons.PERSON_ADD
        self.profile_add_button.on_click = self.__on_click_profile_add_button

        self.profile_add_row = ft.Row()
        self.profile_add_row.controls = [
            self.profile_url_add_field,
            self.profile_add_button
        ]

        self.accounts_column = ft.Column(expand=True, spacing=3)
        self.accounts_column.scroll = ft.ScrollMode.AUTO

        self.controls = [
            self.profile_add_row,
            ft.Divider(),
            self.accounts_column
        ]

        self.__load_accounts()

    def __add_account(self, account: Account):
        is_has_account = any(account.steam_id64 == acc.account.steam_id64 for acc in self.accounts_column.controls)
        if is_has_account: return
        account_widget = AccountContent(account=account)
        account_widget.on_change_hide_nickname(self.__setting_hide_nickname)
        account_widget.on_change_hide_avatar(self.__setting_hide_avatar)
        account_widget.on_change_delay_add_money(self.__setting_delay_add_money)
        account_widget.on_change_auto_use_roulette(self.__setting_auto_use_roulette)
        account_widget.on_change_abuss_use_roulette(self.__setting_abuss_use_roulette)

        self.accounts_column.controls.append(account_widget)
        self.accounts_column.controls.sort(key=lambda acc: acc.account.steam_id64)
        if self.page: self.accounts_column.update()

    def __on_click_profile_add_button(self, e):
        steam_id64 = get_steam_id_from_url(self.profile_url_add_field.value)
        self.profile_url_add_field.value = ''
        self.profile_url_add_field.update()
        if self.page: self.profile_url_add_field.update()
        account = Account(steam_id64=steam_id64)
        account.load_account_info()
        self.__add_account(account=account)

    def __load_accounts(self):
        accounts = sql_manager.account_all_get()
        for account in accounts:
            self.__add_account(account=account)

    def __on_change_hide_nickname(self, value):
        self.__setting_hide_nickname = value
    def __on_change_hide_avatar(self, value):
        self.__setting_hide_avatar = value
    def __on_change_delay_add_money(self, value):
        self.__setting_delay_add_money = value
    def __on_change_auto_use_roulette(self, value):
        self.__setting_auto_use_roulette = value
    def __on_change_abuss_use_roulette(self, value):
        self.__setting_abuss_use_roulette = value


class MassStartPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 0
        self.accounts_list_widget = None
        self.is_widget_work = False
        self.is_period_farm = False
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.START

        self.title_start_stop_all = ft.Text('Start/Stop ALL', size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

        self.button_start_all = ft.FilledTonalButton(height=20, expand=True)
        self.button_start_all.icon = ft.icons.PLAY_CIRCLE
        self.button_start_all.icon_color = ft.colors.GREEN
        self.button_start_all.tooltip = 'Start ALL'
        self.button_start_all.text = 'Start ALL'
        self.button_start_all.style = ft.ButtonStyle(padding=ft.padding.all(0), icon_size=20, alignment=ft.alignment.center)
        self.button_start_all.on_click = self.__on_click_button_start_all

        self.button_stop_all = ft.FilledTonalButton(height=20, expand=True)
        self.button_stop_all.icon = ft.icons.STOP_CIRCLE
        self.button_stop_all.icon_color = ft.colors.RED
        self.button_stop_all.tooltip = 'Stop ALL'
        self.button_stop_all.text = 'Stop ALL'
        self.button_stop_all.style = ft.ButtonStyle(padding=ft.padding.all(0), icon_size=20, alignment=ft.alignment.center)
        self.button_stop_all.on_click = self.__on_click_button_stop_all

        self.row_start_stop = ft.Row()
        self.row_start_stop.alignment = ft.MainAxisAlignment.START
        self.row_start_stop.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.row_start_stop.controls = [
            self.button_start_all,
            self.button_stop_all
        ]


        self.title_period_start_stop_all = ft.Text('Start/Stop поочередный запуск', size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

        self.timer_slider = ft.Slider(min=10, max=610, divisions=60, label="{value} sec", height=20, expand=True)
        self.timer_slider.value = config.time_period_farm
        self.timer_slider.tooltip = 'Время на фарм одного аккаунта до перехода к следующему'
        self.timer_slider.on_change = self.__on_change_timer_slider

        self.button_period_start = ft.IconButton(height=20)
        self.button_period_start.tooltip = 'Start | stop farming'
        self.button_period_start.icon = ft.icons.PLAY_CIRCLE
        self.button_period_start.icon_color = ft.colors.GREEN
        self.button_period_start.visual_density = ft.VisualDensity.COMPACT
        self.button_period_start.style = ft.ButtonStyle(padding=ft.padding.all(0), icon_size=20, alignment=ft.alignment.center)
        self.button_period_start.on_click = self.__on_click_button_period_start

        self.row_period_start_stop = ft.Row()
        self.row_period_start_stop.alignment = ft.MainAxisAlignment.START
        self.row_period_start_stop.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.row_period_start_stop.controls = [
            self.timer_slider,
            self.button_period_start,
        ]

        self.controls = [
            self.title_start_stop_all,
            self.row_start_stop,
            ft.Divider(),
            self.title_period_start_stop_all,
            self.row_period_start_stop
        ]

    def __on_click_button_start_all(self, *args):
        accounts: list[AccountContent] = self.accounts_list_widget.accounts_column.controls
        for account in accounts:
            if account.container_game.is_in_work: continue
            account.start_or_stop()
    def __on_click_button_stop_all(self, *args):
        accounts: list[AccountContent] = self.accounts_list_widget.accounts_column.controls
        for account in accounts:
            if not account.container_game.is_in_work: continue
            account.start_or_stop()
    def __on_change_timer_slider(self, *args):
        config.time_period_farm = self.timer_slider.value
    def __on_click_button_period_start(self, *args):
        self.is_period_farm = not self.is_period_farm
        self.button_period_start.icon = ft.icons.PLAY_CIRCLE if not self.is_period_farm else ft.icons.STOP_CIRCLE
        self.button_period_start.icon_color = ft.colors.GREEN if not self.is_period_farm else ft.colors.RED
        self.__on_click_button_stop_all()
        if self.page: self.update()

    def __update_pool(self):
        while self.is_widget_work:
            time.sleep(1)
            if not self.is_period_farm: continue
            self.__on_click_button_stop_all()

            accounts: list[AccountContent] = self.accounts_list_widget.accounts_column.controls

            min_time_start = min((account.account.last_launch for account in accounts), default=None)
            if min_time_start is None: continue

            try:
                account = next(account for account in accounts if account.account.last_launch == min_time_start)
            except StopIteration:
                continue

            account.start_or_stop()
            time_start_account = time.time()
            while self.is_widget_work and self.is_period_farm and account.container_game.is_in_work:
                time.sleep(1)
                time_start_next = time_start_account + self.timer_slider.value
                if time.time() > time_start_next: break


    def will_unmount(self):
        self.is_widget_work = False
    def did_mount(self):
        if self.is_widget_work: return
        self.is_widget_work = True
        threading.Thread(target=self.__update_pool, daemon=True).start()

class AccountsPage(BasePage):
    def __init__(self):
        super().__init__()
        self.name = 'accounts'
        self.label = 'Accounts'
        self.icon = ft.icons.PERSON
        self.selected_icon = ft.icons.PERSON_OUTLINED

        self.accounts_list_page = AccountsList()
        self.mass_start_page = MassStartPage()
        self.mass_start_page.accounts_list_widget = self.accounts_list_page

        self.page_content = ft.Column(expand=True, spacing=0)
        self.page_content.controls = [
            ft.Container(
                content=self.accounts_list_page,
                border=ft.border.all(width=1, color=ft.colors.GREY),
                padding=ft.padding.all(5),
                border_radius=ft.border_radius.all(5),
                expand=True
            ),
            ft.Divider(),
            ft.Container(
                content=self.mass_start_page,
                border=ft.border.all(width=1, color=ft.colors.GREY),
                padding=ft.padding.all(5),
                border_radius=ft.border_radius.all(5),
            ),
        ]

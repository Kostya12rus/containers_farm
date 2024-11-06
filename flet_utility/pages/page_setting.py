import flet as ft
from flet_utility.pages.base import BasePage, Title
from sql_utility import config


class RouletteSettingContent(ft.Container):
    def __init__(self):
        super().__init__()
        self.border = ft.border.all(width=1, color=ft.colors.GREY)
        self.padding = ft.padding.all(5)
        self.border_radius = ft.border_radius.all(5)
        self.alignment = ft.alignment.top_center

        self.title = Title('Buy Roulette Setting', size=15)

        self.auto_use_roulette = ft.Checkbox(label='Auto Buy Roulette')
        self.auto_use_roulette.value = bool(config.auto_use_roulette)
        self.auto_use_roulette.on_change = self.__on_change_auto_use_roulette

        self.abuss_use_roulette = ft.Checkbox(label='Use Abuss Buy Roulette')
        self.abuss_use_roulette.value = bool(config.abuss_use_roulette)
        self.abuss_use_roulette.on_change = self.__on_change_abuss_use_roulette

        self.setting_row = ft.Row(expand=True)
        self.setting_row.alignment = ft.MainAxisAlignment.CENTER
        self.setting_row.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.setting_row.controls = [
            self.auto_use_roulette,
            self.abuss_use_roulette,
        ]

        self.content = ft.Column(spacing=0)
        self.content.controls = [
            self.title,
            self.setting_row
        ]

    def __on_change_auto_use_roulette(self, *args):
        config.auto_use_roulette = self.auto_use_roulette.value
    def __on_change_abuss_use_roulette(self, *args):
        config.abuss_use_roulette = self.abuss_use_roulette.value

class FarmMoneySettingContent(ft.Container):
    def __init__(self):
        super().__init__()
        self.border = ft.border.all(width=1, color=ft.colors.GREY)
        self.padding = ft.padding.all(5)
        self.border_radius = ft.border_radius.all(5)
        self.alignment = ft.alignment.top_center

        self.title = Title('Farm Money Setting', size=15)

        self.delay_setting = ft.Slider(min=10, max=1010, divisions=100, label="{value}ms", height=20, expand=True)
        self.delay_setting.on_change_end = self.__on_change_delay_setting
        self.delay_setting.value = config.delay_add_money * 1000
        self.delay_title = ft.Text('Задержка между получением денег', size=15, width=300)

        self.setting_row = ft.Row(expand=True)
        self.setting_row.alignment = ft.MainAxisAlignment.CENTER
        self.setting_row.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.setting_row.controls = [
            self.delay_setting,
            self.delay_title,
        ]

        self.content = ft.Column(spacing=0)
        self.content.controls = [
            self.title,
            self.setting_row
        ]

    def __on_change_delay_setting(self, *args):
        config.delay_add_money = self.delay_setting.value / 1000

class AnonymousSettingContent(ft.Container):
    def __init__(self):
        super().__init__()
        self.border = ft.border.all(width=1, color=ft.colors.GREY)
        self.padding = ft.padding.all(5)
        self.border_radius = ft.border_radius.all(5)
        self.alignment = ft.alignment.top_center

        self.title = Title('Anonymous Setting', size=15)

        self.hide_nickname = ft.Checkbox(label='Hide nickname')
        self.hide_nickname.value = bool(config.hide_nickname)
        self.hide_nickname.on_change = self.__on_change_hide_nickname

        self.hide_avatar = ft.Checkbox(label='Hide avatar')
        self.hide_avatar.value = bool(config.hide_avatar)
        self.hide_avatar.on_change = self.__on_change_hide_avatar

        self.setting_row = ft.Row(expand=True)
        self.setting_row.alignment = ft.MainAxisAlignment.CENTER
        self.setting_row.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.setting_row.controls = [
            self.hide_nickname,
            self.hide_avatar,
        ]

        self.content = ft.Column(spacing=0)
        self.content.controls = [
            self.title,
            self.setting_row
        ]

    def __on_change_hide_nickname(self, *args):
        config.hide_nickname = self.hide_nickname.value
    def __on_change_hide_avatar(self, *args):
        config.hide_avatar = self.hide_avatar.value

class SettingPageContent(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 0

        self.title = Title('Setting Page')

        self.setting_widgets = ft.Column(expand=True)
        self.setting_widgets.controls = [
            AnonymousSettingContent(),
            FarmMoneySettingContent(),
            RouletteSettingContent(),
        ]

        self.controls = [
            self.title,
            ft.Divider(),
            self.setting_widgets,
        ]


class SettingPage(BasePage):
    def __init__(self):
        super().__init__()
        self.name = 'setting'
        self.label = 'Setting'
        self.icon = ft.icons.SETTINGS
        self.selected_icon = ft.icons.SETTINGS_ROUNDED

        self.page_content = SettingPageContent()


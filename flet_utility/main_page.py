import flet as ft
from flet_utility.other import ThemeToggleButton, ColorMenuButton
from flet_utility.pages import *


class MainPageContent(ft.Row):
    def __init__(self):
        super().__init__()

        self._accounts_page = AccountsPage()
        self._setting_page = SettingPage()
        self._pages = [
            self._accounts_page,
            self._setting_page,
        ]

        self.expand = True
        self.spacing = 0

        self.logout_button = ft.IconButton(visible=False)
        self.logout_button.icon = ft.icons.LOGOUT
        self.logout_button.icon_color = ft.colors.RED
        self.logout_button.tooltip = "Logout"
        # self.logout_button.on_click = self.on_press_logout

        self.navigation_rail = ft.NavigationRail(expand=True, selected_index=0)
        self.navigation_rail.label_type = ft.NavigationRailLabelType.ALL
        self.navigation_rail.destinations = self._pages
        self.navigation_rail.on_change = self.on_rail_change
        # self.navigation_rail.trailing = self.logout_button

        self.design_editor_theme_toggle = ThemeToggleButton()
        self.design_editor_color_menu = ColorMenuButton()

        self.design_editor = ft.Row(spacing=0)
        self.design_editor.alignment = ft.MainAxisAlignment.CENTER
        self.design_editor.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.design_editor.controls = [
            self.design_editor_theme_toggle,
            self.design_editor_color_menu
        ]

        self.navigation_column = ft.Column()
        self.navigation_column.alignment = ft.MainAxisAlignment.CENTER
        self.navigation_column.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.navigation_column.controls = [
            self.navigation_rail,
            self.design_editor
        ]

        self.vertical_divider = ft.VerticalDivider()

        self.content_page = ft.Column(controls=[], expand=True, spacing=1)

        self.controls = [
            self.navigation_column,
            self.vertical_divider,
            self.content_page
        ]

    def set_snack_bar(self, text: str):
        if self.page:
            text_snack_bar = ft.Text(text, expand=True, text_align=ft.TextAlign.CENTER)
            self.page.snack_bar = ft.SnackBar(text_snack_bar)
            self.page.snack_bar.open = True
            self.page.update()

    def on_rail_change(self, event: ft.ControlEvent = None, set_page: ft.NavigationRailDestination = None):
        if set_page:
            selected_index = self._pages.index(set_page)
            if selected_index != self.navigation_rail.selected_index:
                self.navigation_rail.selected_index = selected_index
                self.navigation_rail.update()
        now_page = self._pages[self.navigation_rail.selected_index]
        if not now_page: return
        if now_page.page_content in self.content_page.controls: return
        self.content_page.controls = [now_page.page_content]
        if self.page: self.content_page.update()


class MainPage:
    def __init__(self, title: str = None):
        self.title = title or "No Name title"
        self.page = None
        self.page_content = MainPageContent()

    def build(self, page: ft.Page):
        self.page = page
        self.page.window.min_width = 1130
        self.page.window.min_height = 600
        self.page.padding = 0
        self.page.spacing = 1
        self.page.title = self.title
        self.page.controls = [
            self.page_content
        ]

        self.page_content.on_rail_change(None)
        self.page.update()

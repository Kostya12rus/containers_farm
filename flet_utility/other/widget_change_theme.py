import flet as ft

class ThemeToggleButton(ft.IconButton):
    def __init__(self):
        super().__init__()
        self.icon = ft.icons.LIGHT_MODE
        self.tooltip = "Change theme"
        self.on_click = self.toggle_theme

    def toggle_theme(self, *args):
        new_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.page.theme_mode = new_mode
        self.icon = ft.icons.DARK_MODE if new_mode == ft.ThemeMode.DARK else ft.icons.LIGHT_MODE
        self.page.update()

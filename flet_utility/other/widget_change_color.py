import flet as ft

COLORS = [
    {"color": "indigo", "name": "Indigo"},
    {"color": "blue", "name": "Blue (default)"},
    {"color": "teal", "name": "Teal"},
    {"color": "green", "name": "Green"},
    {"color": "yellow", "name": "Yellow"},
    {"color": "orange", "name": "Orange"},
    {"color": "deeporange", "name": "Deep orange"},
    {"color": "pink", "name": "Pink"},
]

class ColorMenuItem(ft.PopupMenuItem):
    def __init__(self, color, name):
        super().__init__()

        self.icon_widget = ft.Icon(name=ft.icons.COLOR_LENS_OUTLINED, color=color)
        self.text_widget = ft.Text(name)

        self.content = ft.Row()
        self.content.controls = [
            self.icon_widget,
            self.text_widget
        ]

        self.on_click = self.change_color
        self.data = color

    def change_color(self, e):
        self.page.theme = self.page.dark_theme = ft.theme.Theme(color_scheme_seed=self.data)
        self.page.update()

class ColorMenuButton(ft.PopupMenuButton):
    def __init__(self):
        super().__init__()
        self.tooltip = "Change colors"
        self.icon = ft.icons.COLOR_LENS_OUTLINED
        self.items = [ColorMenuItem(color=data['color'], name=data['name']) for data in COLORS]

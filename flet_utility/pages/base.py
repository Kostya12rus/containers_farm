import flet as ft

class Title(ft.Row):
    def __init__(self, title_text: str, size: int = 20, color: ft.colors = ft.colors.BLUE, text_align: ft.TextAlign = ft.TextAlign.CENTER):
        super().__init__()
        self.spacing = 0
        self.run_spacing = 0
        self.alignment = ft.MainAxisAlignment.CENTER
        self.text_widget = ft.Text(value=title_text, size=size, color=color, text_align=text_align, weight=ft.FontWeight.BOLD)
        self.container = ft.Container(padding=0, expand=True, content=self.text_widget)
        self.controls = [
            self.container
        ]

class BasePage(ft.NavigationRailDestination):
    def __init__(self):
        super().__init__()
        self.name = None
        self.page_content = None

    def build(self):
        ...
    def will_unmount(self):
        ...
    def did_mount(self):
        ...
    def before_update(self):
        ...

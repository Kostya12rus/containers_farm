import flet as ft
from flet_utility.pages.base import BasePage, Title


class ExamplePageContent(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.title = Title('EXAMPLE PAGE')

        self.controls = [
            self.title,
        ]

class ExamplePage(BasePage):
    def __init__(self):
        super().__init__()
        self.name = 'example'
        self.label = 'Example'
        self.icon = ft.icons.PAYMENT
        self.selected_icon = ft.icons.PAYMENT_ROUNDED

        self.page_content = ExamplePageContent()


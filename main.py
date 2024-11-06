import os
import flet as ft
from flet_utility.main_page import MainPage

main_page = MainPage('Containers Farm')
ft.app(main_page.build)

os.abort()

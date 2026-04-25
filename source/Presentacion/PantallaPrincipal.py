import flet as ft

class pantallaPrincipal:

    def __init__(self):
        pass

    def init_GUI(page):
        page.title = "Sistema Biblioteca UNACH"
        page.bgcolor = "#9ec9ff"
        # Tamaño ventana
        page.window_width = 1400
        page.window_height = 900
        page.window_min_width = 1200
        page.window_min_height = 800

        # CONTENIDO DINÁMICO
        content_area = ft.Container(expand=True)

        # LAYOUT GLOBAL
        layout = ft.Row(expand=True)
import flet as ft

# Importamos tu nueva clase Login en lugar de la Principal
from Presentacion.PantallaLogin import PantallaLogin

def main(page: ft.Page):
    page.title = "Sistema Biblioteca UNACH"
    page.bgcolor = "#9ec9ff"
    page.padding = 0
    # Tamaño ventana
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 1200
    page.window_min_height = 800

    # Instanciamos el Login y lo agregamos a la página
    login_app = PantallaLogin(page)
    # Suponiendo que tu clase tiene un método "construir_vista" que devuelve el diseño
    page.add(login_app.construir_vista()) 

def run():
    ft.app(target=main, assets_dir="Presentacion/assets")
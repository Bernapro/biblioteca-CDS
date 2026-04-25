import flet as ft

from Presentacion.PantallaPrincipal import PantallaPrincipal as pp

def main(page: ft.Page):
    page.title = "Sistema Biblioteca UNACH"
    page.bgcolor = "#9ec9ff"
    
    # Tamaño ventana
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 1200
    page.window_min_height = 800

    app = pp(page)
    page.add(app)

def run():
    ft.run(main)
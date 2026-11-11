import flet as ft

# Importamos tu nueva clase Login en lugar de la Principal
from Presentacion.PantallaLogin import PantallaLogin
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp

def main(page: ft.Page):
    page.title = "Sistema Biblioteca UNACH"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#9ec9ff"
    page.padding = 0
    # Tamaño ventana
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 1200
    page.window_min_height = 800

    # Cierre automático de sesiones pendientes al iniciar la aplicación
    try:
        RepositorioImpl(CRUDimp()).cerrar_registros_pendientes()
    except Exception as e:
        print(f"Aviso en cierre inicial de registros: {e}")

    # Instanciamos el Login y lo agregamos a la página
    login_app = PantallaLogin(page)
    page.add(login_app.construir_vista()) 

def run():
    ft.app(target=main, assets_dir="Presentacion/assets")
import flet as ft

from Presentacion.MenuLateral import MenuLateral as ml
from Presentacion.PantallaAsistencia import PantallaAsistencia as pa
from Presentacion.PantallaDashboard import PantallaDashboard as dsh
from Presentacion.PantallaHistorial import PantallaHistorial as ph
from Presentacion.PantallaIncidencia import PantallaIncidencias as pin
from Presentacion.PantallaLibros import PantallaLibros as pl
from Presentacion.PantallaPrestamos import PantallaPrestamos as pp
from Presentacion.PantallaReportes import PantallaReportes as pr
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp

class PantallaPrincipal(ft.Container):

    def __init__(self, main_page: ft.Page):
        super().__init__()
        self.main_page = main_page

        self.repo = RepositorioImpl(CRUDimp())
        self.repo.backup_bd()
        # Arrancamos en modo claro por defecto
        self.main_page.theme_mode = ft.ThemeMode.LIGHT

        # Propiedades del contenedor principal
        self.expand = True
        self.margin = 20
        self.padding = 20
        self.border_radius = 30
        self.bgcolor = "#F1F5F9"
        self.shadow = ft.BoxShadow(
            blur_radius=30,
            color="black12",
            offset=ft.Offset(0, 10)
        )

        # Estado de la App
        self.index_actual = 0

        # Instanciar el Sidebar
        self.sidebar = ml(on_menu_click=self.cambiar_vista, active_index=0)

        # Lazy Loading de vistas
        self.vistas = [None] * 7

        # CARGAR PRIMERA VISTA MANUALMENTE DESDE AQUÍ
        self.vistas[0] = dsh(self.main_page)
        self.vistas[0].ir_reportes = lambda: self.sidebar.cambiar_seleccion(3)
        # Área de contenido
        self.content_area = ft.Container(
            expand=True,
            content=self.vistas[0]
        )

        # El switch del sol y la luna
        self.toggle_theme_container = ft.Row(
            controls=[
                ft.Icon(ft.Icons.LIGHT_MODE_OUTLINED, color="#3B82F6"),
                ft.Switch(
                    value=False,
                    on_change=self.cambiar_tema,
                    active_color="white",
                    active_track_color="#1E3A8A",
                    inactive_thumb_color="white",
                    inactive_track_color="#3B82F6"
                ),
                ft.Icon(ft.Icons.DARK_MODE_OUTLINED, color="#4B5563")
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=0
        )

        # Contenedor alineado con coordenadas seguras
        self.header_global = ft.Container(
            content=self.toggle_theme_container,
            padding=ft.padding.only(right=10, bottom=5),
            alignment=ft.Alignment(1, -1)
        )

        self.columna_derecha = ft.Column(
            expand=True,
            controls=[
                self.header_global,
                self.content_area
            ],
            spacing=0
        )

        # Layout general ensamblado
        self.content = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                self.sidebar,
                self.columna_derecha
            ]
        )
    # ==========================================
    # MODO OSCURO
    # ==========================================
    def cambiar_tema(self, e):
        if e.control.value:
            self.main_page.theme_mode = ft.ThemeMode.DARK
            self.bgcolor = "#0F172A"
        else:
            self.main_page.theme_mode = ft.ThemeMode.LIGHT
            self.bgcolor = "#F1F5F9"

        self.main_page.update()
        self.update()

    # ==========================================
    # ENRUTADOR DE VISTAS
    # ==========================================
    def cambiar_vista(self, index):

        if self.vistas[index] is None:

            if index == 0:
                self.vistas[index] = dsh(self.main_page)

            elif index == 1:
                self.vistas[index] = pa(self.main_page)

            elif index == 2:
                self.vistas[index] = ph(self.main_page)

            elif index == 3:
                self.vistas[index] = pr(self.main_page)

            elif index == 4:
                self.vistas[index] = pl(self.main_page)

            elif index == 5:
                self.vistas[index] = pp(self.main_page)

            elif index == 6:
                self.vistas[index] = pin(self.main_page)

        vista = self.vistas[index]
        self.content_area.content = vista

        if self.page is not None:
            self.content_area.update()
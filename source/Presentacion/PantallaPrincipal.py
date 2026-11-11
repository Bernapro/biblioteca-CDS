import threading
import time
from datetime import datetime
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

    def __init__(self, main_page: ft.Page, usuario_actual: dict = None):
        super().__init__()
        self.main_page = main_page
        self.usuario_actual = usuario_actual
        self.es_oscuro = False
        self._timer_activo = True

        self.repo = RepositorioImpl(CRUDimp())
        self.repo.cerrar_registros_pendientes()
        self.repo.backup_bd()

        # Configurar esquemas de color para modo claro y modo oscuro real
        self.main_page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#2563EB",
                on_primary="#FFFFFF",
                primary_container="#DBEAFE",
                on_primary_container="#1E40AF",
                surface="#FFFFFF",
                surface_container_highest="#F1F5F9",
                surface_container="#F8FAFC",
                on_surface="#000000",
                on_surface_variant="#6C757D",
                outline="#CBD5E1"
            )
        )
        self.main_page.dark_theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#3B82F6",
                on_primary="#FFFFFF",
                primary_container="#1E3A8A",
                on_primary_container="#DBEAFE",
                surface="#1E222A",
                surface_container_highest="#242832",
                surface_container="#181A1F",
                on_surface="#F8F9FA",
                on_surface_variant="#9CA3AF",
                outline="#2E3440"
            )
        )

        # Arrancamos en modo claro por defecto
        self.main_page.theme_mode = ft.ThemeMode.LIGHT
        self.main_page.bgcolor = "#9ec9ff"

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
        self.sidebar = ml(
            on_menu_click=self.cambiar_vista,
            active_index=0,
            on_logout=self.detener_timer
        )

        # Lazy Loading de vistas
        self.vistas = [None] * 7

        # CARGAR PRIMERA VISTA MANUALMENTE DESDE AQUÍ
        self.vistas[0] = dsh(self.main_page, usuario_actual=self.usuario_actual)
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
                ft.Icon(ft.Icons.DARK_MODE_OUTLINED, color="#9CA3AF")
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

        # Iniciar temporizador en segundo plano (cada 5 minutos y en cambio de turno 14:00 / 20:00)
        self._iniciar_timer_cierre_sesiones()

    def detener_timer(self):
        self._timer_activo = False

    def _iniciar_timer_cierre_sesiones(self):
        def loop_cierre():
            ultimo_cierre_turno = None
            segundos_transcurridos = 0
            while self._timer_activo:
                time.sleep(1)
                if not self._timer_activo:
                    break
                segundos_transcurridos += 1
                ahora = datetime.now()
                marca_turno = (ahora.date(), ahora.hour, ahora.minute)
                es_hora_corte = (ahora.hour in (14, 20) and ahora.minute == 0 and ultimo_cierre_turno != marca_turno)

                if segundos_transcurridos >= 300 or es_hora_corte:
                    segundos_transcurridos = 0
                    if es_hora_corte:
                        ultimo_cierre_turno = marca_turno
                    self._ejecutar_cierre_y_refrescar()

        hilo = threading.Thread(target=loop_cierre, daemon=True)
        hilo.start()

    def _ejecutar_cierre_y_refrescar(self):
        try:
            self.repo.cerrar_registros_pendientes()
            vista_activa = self.vistas[self.index_actual]
            if vista_activa is not None:
                if self.index_actual == 0 and hasattr(vista_activa, "cargar_datos"):
                    vista_activa.cargar_datos()
                elif self.index_actual == 2 and hasattr(vista_activa, "filtrar"):
                    vista_activa.filtrar()
                elif self.index_actual == 3 and hasattr(vista_activa, "actualizar"):
                    vista_activa.actualizar()
            if self.main_page is not None:
                self.main_page.update()
        except Exception as e:
            print(f"Aviso en timer de cierre automático: {e}")

    # MODO OSCURO
    def cambiar_tema(self, e):
        self.es_oscuro = bool(e.control.value)
        if self.es_oscuro:
            self.main_page.theme_mode = ft.ThemeMode.DARK
            self.main_page.bgcolor = "#181A1F"
            self.bgcolor = "#121212"
        else:
            self.main_page.theme_mode = ft.ThemeMode.LIGHT
            self.main_page.bgcolor = "#9ec9ff"
            self.bgcolor = "#F1F5F9"

        if hasattr(self.sidebar, "aplicar_tema"):
            self.sidebar.aplicar_tema(self.es_oscuro)

        for vista in self.vistas:
            if vista is not None:
                if hasattr(vista, "content") and vista.content is not None and hasattr(vista.content, "aplicar_tema"):
                    vista.content.aplicar_tema(self.es_oscuro)
                if hasattr(vista, "aplicar_tema"):
                    vista.aplicar_tema(self.es_oscuro)

        self.main_page.update()
        self.update()

    # ENRUTADOR DE VISTAS
    def cambiar_vista(self, index):
        self.index_actual = index

        if index in (0, 1, 2, 3):
            self.repo.cerrar_registros_pendientes()

        creada_ahora = False
        if self.vistas[index] is None:
            creada_ahora = True
            if index == 0:
                self.vistas[index] = dsh(self.main_page, usuario_actual=self.usuario_actual)
                self.vistas[index].ir_reportes = lambda: self.sidebar.cambiar_seleccion(3)

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
        if hasattr(vista, "aplicar_tema"):
            vista.aplicar_tema(self.es_oscuro)

        self.content_area.content = vista

        if not creada_ahora:
            if index == 0 and hasattr(vista, "cargar_datos"):
                vista.cargar_datos()
            elif index == 2 and hasattr(vista, "filtrar"):
                vista.filtrar()
            elif index == 3 and hasattr(vista, "actualizar"):
                vista.actualizar()

        if self.page is not None:
            self.content_area.update()
import flet as ft

from Presentacion.MenuLateral import MenuLateral as ml
from Presentacion.PantallaAsistencia import PantallaAsistencia as pa
from Presentacion.PantallaDashboard import PantallaDashboard as dsh
from Presentacion.PantallaHistorial import PantallaHistorial as ph
from Presentacion.PantallaIncidencia import PantallaIncidencias as pin
from Presentacion.PantallaLibros import PantallaLibros as pl
from Presentacion.PantallaPrestamos import PantallaPrestamos as pp
from Presentacion.PantallaReportes import PantallaReportes as pr

class PantallaPrincipal(ft.Container):
    
    def __init__(self, main_page: ft.Page):
        super().__init__()
        self.main_page = main_page
        
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
        
        self.vistas = [
            dsh(self.main_page), pa(self.main_page), 
            ph(self.main_page), pr(self.main_page), 
            pl(self.main_page), pp(self.main_page), 
            pin(self.main_page)
        ]
        
        # Área de contenido
        self.content_area = ft.Container(expand=True, content=self.vistas[0])
        
        # El switch del sol y la luna
        self.toggle_theme_container = ft.Row(
            controls=[
                ft.Icon(ft.Icons.LIGHT_MODE_OUTLINED, color="#3B82F6"),
                ft.Switch(
                    value=False,
                    on_change=self.cambiar_tema, # Llamamos a la nueva función de abajo
                    active_color="white",
                    active_track_color="#1E3A8A", # Azul oscuro
                    inactive_thumb_color="white",
                    inactive_track_color="#3B82F6" # Azul claro
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
            alignment=ft.Alignment(1, -1) # Arriba a la derecha a prueba de fallos
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
            controls=[
                self.sidebar,
                self.columna_derecha 
            ]
        )

    # ==========================================
    # 🔥 LA MAGIA DEL MODO OSCURO (MÉTODO OFICIAL)
    # ==========================================
    def cambiar_tema(self, e):
        if e.control.value: # Si la Luna está activa
            self.main_page.theme_mode = ft.ThemeMode.DARK
            self.bgcolor = "#0F172A" # Cambiamos el fondo global a oscuro
        else: # Si el Sol está activo
            self.main_page.theme_mode = ft.ThemeMode.LIGHT
            self.bgcolor = "#F1F5F9" # Regresamos al gris clarito
            
        self.main_page.update() # Refresca toda la ventana de Windows
        self.update() # Refresca este contenedor específico

    # ==========================================
    # ENRUTADOR DE VISTAS
    # ==========================================
    def cambiar_vista(self, index):
        vista = self.vistas[index]
        self.content_area.content = vista

        if hasattr(vista, "actualizar"):
            vista.actualizar()

        self.content_area.update()
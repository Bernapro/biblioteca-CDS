import flet as ft

from Presentacion.MenuLateral import MenuLateral as ml
from Presentacion.PantallaAsistencia import PantallaAsistencia as pa
from Presentacion.PantallaDashboard import PantallaDashboard as dsh
from Presentacion.PantallaHistorial import PantallaHistorial as ph
from Presentacion.PantallaIncidencia import PantallaIncidencias as pin
from Presentacion.PantallaLibros import PantallaLibros as pl

class PantallaPrincipal(ft.Container):
    
    def __init__(self, main_page: ft.Page):
        super().__init__()
        self.main_page = main_page
        
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
        self.sidebar = ml(self)
        
        self.vistas = [
            dsh(self.main_page), pa(self.main_page), 
            ph(self.main_page), ft.Text("Vista Reportes"), 
            pl(self.main_page), ft.Text("Vista Préstamos"), 
            pin(self.main_page)
        ]
        # Área de contenido
        self.content_area = ft.Container(expand=True, content=self.vistas[0])
        
        # Instanciar las vistas (Deben ser clases que hereden de ft.Container)
        # self.vistas = [
        #     DashboardView(self.page),
        #     AsistenciaView(self.page),
        #     ...
        # ]
        
        # Para propósitos de prueba sin los imports reales:

        # Layout general
        self.content = ft.Row(
            expand=True,
            controls=[
                self.sidebar,
                self.content_area
            ]
        )

    def cambiar_vista(self, index):
        # 1. Cambiamos el contenido
        self.content_area.content = self.vistas[index]
        # 2. Actualizamos la pantalla (ahora es 100% seguro)
        self.content_area.update()
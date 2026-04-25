import flet as ft

from Presentacion.MenuLateral import MenuLateral as ml
from Presentacion.PantallaAsistencia import PantallaAsistencia as pa

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
        
        # Área de contenido
        self.content_area = ft.Container(expand=True)
        
        # Instanciar las vistas (Deben ser clases que hereden de ft.Container)
        # self.vistas = [
        #     DashboardView(self.page),
        #     AsistenciaView(self.page),
        #     ...
        # ]
        
        # Para propósitos de prueba sin los imports reales:
        self.vistas = [
            ft.Text("Vista Principal"), pa(self.main_page), 
            ft.Text("Vista Historial"), ft.Text("Vista Reportes"), 
            ft.Text("Vista Libros"), ft.Text("Vista Préstamos"), 
            ft.Text("Vista Incidencias")
        ]

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
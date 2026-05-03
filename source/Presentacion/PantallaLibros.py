import flet as ft
from Presentacion.PantallaRegistrarLibro import PantallaRegistrarLibro
from Infraestructura.API.libros_api import obtener_libros

class PantallaLibros(ft.Container):

    # Constructor
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        self.AZUL = "#3B82F6"
        self.FONDO = "#EAF1F7"

        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        self.input_busqueda = ft.TextField(
            width=250,
            hint_text="Buscar por título o ISBN...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            bgcolor="white",
            cursor_color="black",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#6B7280"),
            label_style=ft.TextStyle(color="black"),
        )

        self.dropdown_disponibilidad = ft.Dropdown(
            width=180,
            label="Disponibilidad",
            color="black",
            bgcolor="white",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            options=[
                ft.dropdown.Option(text="Todos"),
                ft.dropdown.Option(text="Disponible"),
                ft.dropdown.Option(text="Prestado"),
            ]
        )

        self.grid_libros = ft.GridView(
            expand=True,
            runs_count=4,
            max_extent=220,
            spacing=20,
            run_spacing=20,
        )

        self.build_ui()
        self.refrescar_grid()
    
    # Card libro
    def build_card_libro(self, titulo, isbn, ejemplares):
        return ft.Container(
            width=200,
            height=220,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MENU_BOOK, size=60, color=self.AZUL),

                    ft.Text(
                        titulo,
                        weight="bold",
                        size=14,
                        color="black",
                        text_align="center"
                    ),

                    ft.Text(
                        f"ISBN: {isbn}",
                        size=12,
                        color="#374151"
                    ),

                    ft.Container(
                        padding=5,
                        border_radius=10,
                        bgcolor="#DBEAFE",
                        content=ft.Text(
                            f"Ejemplares: {ejemplares}",
                            size=11,
                            color="#1D4ED8"
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            )
        )

    # Refrescar grid
    def refrescar_grid(self, libros_filtrados=None):
        try:
            if libros_filtrados is not None:
                datos = libros_filtrados
            else:
                response = obtener_libros()

                if response.status_code != 200:
                    self._page.snack_bar = ft.SnackBar(
                        ft.Text("Error al cargar libros")
                    )
                    self._page.snack_bar.open = True
                    self.grid_libros.update()
                    return

                datos = response.json()["contenido"]

                # TEMPORAL:
                # Mostrar estructura real que devuelve la API
                # para verificar si ya viene cantidad de ejemplares
                print("LIBROS API:", datos)

            self.grid_libros.controls = [
                self.build_card_libro(
                    libro["titulo"],
                    libro["isbn"],
                    libro["Ejemplares"]
                )
                for libro in datos
            ]

            self._page.update()

        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(e)}")
            )
            self._page.snack_bar.open = True
            self._page.update()

    # Buscar libros
    def buscar_libros(self, e):
        texto = (self.input_busqueda.value or "").lower()
        estado = self.dropdown_disponibilidad.value or "Todos"

        response = obtener_libros()

        if response.status_code != 200:
            return

        libros_bd = response.json()["contenido"]

        filtrados = []

        for libro in libros_bd:
            coincide_texto = (
                texto in libro["titulo"].lower()
                or texto in libro["isbn"].lower()
            )

            coincide_estado = (
                estado == "Todos" or estado == "Disponible"
            )

            if coincide_texto and coincide_estado:
                filtrados.append(libro)

        self.refrescar_grid(filtrados)

    def ir_a_registro_libro(self, e):
        self.content = PantallaRegistrarLibro(
            self._page,
            vista_anterior=self
        )
        self.update()

    # UI principal
    def build_ui(self):

        filtros = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.input_busqueda,
                    self.dropdown_disponibilidad,

                    ft.ElevatedButton(
                        "Buscar",
                        on_click=self.buscar_libros,
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    ),

                    ft.ElevatedButton(
                        "Añadir libro",
                        icon=ft.Icons.ADD,
                        on_click=self.ir_a_registro_libro,
                        style=ft.ButtonStyle(
                            bgcolor="#10B981",
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

        self.content = ft.Column(
            [
                ft.Text(
                    "Catálogo de libros",
                    size=32,
                    weight="bold",
                    color="black"
                ),

                ft.Text(
                    "Busca y gestiona el catálogo de libros registrados en el sistema",
                    color="black"
                ),

                filtros,

                self.grid_libros
            ],
            spacing=20,
            expand=True
        )
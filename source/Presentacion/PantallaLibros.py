import flet as ft

class PantallaLibros(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.FONDO = "#EAF1F7"

        # Propiedades del Contenedor Principal (Fondo de la vista)
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== CONTROLES DINÁMICOS =====
        self.input_busqueda = ft.TextField(
            width=250,
            hint_text="Buscar por título o autor...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",               
            cursor_color="black",          
            hint_style=ft.TextStyle(color="#6B7280")  
        )

        self.dropdown_disponibilidad = ft.Dropdown(
            width=180,
            label="Disponibilidad",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Disponible"),
                ft.dropdown.Option("Prestado"),
            ]
        )

        self.grid_libros = ft.GridView(
            expand=True,
            runs_count=4,
            max_extent=220,
            spacing=20,
            run_spacing=20,
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== CARD LIBRO (Generador) =====
    def build_card_libro(self, titulo, autor, estado):
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

                    ft.Text(titulo, weight="bold", size=14, color="black", text_align=ft.TextAlign.CENTER),
                    ft.Text(autor, size=12, color="black", text_align=ft.TextAlign.CENTER),

                    ft.Container(
                        padding=5,
                        border_radius=10,
                        bgcolor="#DCFCE7" if estado == "Disponible" else "#FEE2E2",
                        content=ft.Text(
                            estado,
                            size=11,
                            color="green" if estado == "Disponible" else "red"
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            )
        )

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        # --- Llenar Grid con datos de prueba ---
        # 💡 FUTURO: Aquí es donde iterarás sobre los resultados de tu Base de Datos
        self.grid_libros.controls = [
            self.build_card_libro("El principito", "Antoine", "Disponible"),
            self.build_card_libro("1984", "Orwell", "Prestado"),
            self.build_card_libro("Cien años", "García Márquez", "Disponible"),
            self.build_card_libro("Don Quijote", "Cervantes", "Disponible"),
            self.build_card_libro("It", "Stephen King", "Prestado"),
            self.build_card_libro("Hábitos Atómicos", "James Clear", "Disponible"),
            self.build_card_libro("Clean Code", "Robert C.", "Disponible"),
            self.build_card_libro("Python Básico", "Autor X", "Prestado"),
        ]

        # --- Filtros superiores ---
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
                        # on_click=self.buscar_libros, # Próxima función para filtrar la BD
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

        # --- Ensamblaje final ---
        self.content = ft.Column(
            [
                ft.Text("Catálogo de libros", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona el catalogo de libros registrados en el sistema",
                    color="black"
                ),
                filtros,
                self.grid_libros
            ],
            spacing=20,
            expand=True
        )
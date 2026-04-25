import flet as ft

class PantallaPrestamos(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#22C55E"
        self.FONDO = "#EAF1F7"

        # Propiedades del Contenedor Principal (Fondo de la vista)
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== CONTROLES DINÁMICOS =====
        self.input_busqueda = ft.TextField(
            width=350,
            hint_text="Buscar por matrícula, nombre o libro...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            text_style=ft.TextStyle(color="black"),
        )

        self.dropdown_estado = ft.Dropdown(
            width=180,
            label="Estado",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("A tiempo"),
                ft.dropdown.Option("Atrasado"),
            ],
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            focused_border_color=self.AZUL
        )

        self.tabla = ft.DataTable(
            expand=True,
            column_spacing=40,
            heading_row_color="#F1F5F9",
            columns=[
                ft.DataColumn(ft.Text("Matrícula", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Nombre", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Libro", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Estado", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Acciones", color="black", weight="bold")),
            ],
            rows=[] # Iniciamos las filas vacías, se llenarán en build_ui()
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== BOTONES REUTILIZABLES =====
    def build_btn_extender(self):
        return ft.ElevatedButton(
            "Extender",
            height=35,
            style=ft.ButtonStyle(
                bgcolor=self.AZUL,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
            # Aquí podrías agregar: on_click=self.extender_prestamo
        )

    def build_btn_devolver(self):
        return ft.ElevatedButton(
            "Devolver",
            height=35,
            style=ft.ButtonStyle(
                bgcolor=self.VERDE,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
            # Aquí podrías agregar: on_click=self.devolver_prestamo
        )

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        
        # --- Llenar la tabla con datos de prueba estáticos ---
        # 💡 FUTURO: Reemplazar esto con un bucle que consulte tu base de datos
        self.tabla.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("100025787", color="black")),
                ft.DataCell(ft.Text("Carlos Daniel", color="black")),
                ft.DataCell(ft.Text("El principito", color="black")),
                ft.DataCell(ft.Text("A tiempo", color="black")),
                ft.DataCell(ft.Row([self.build_btn_extender(), self.build_btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("100025788", color="black")),
                ft.DataCell(ft.Text("Cruz Castillo", color="black")),
                ft.DataCell(ft.Text("1984", color="black")),
                ft.DataCell(ft.Text("Atrasado", color="black")),
                ft.DataCell(ft.Row([self.build_btn_extender(), self.build_btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ABCDEFGA", color="black")),
                ft.DataCell(ft.Text("Jose Angel", color="black")),
                ft.DataCell(ft.Text("Clean Code", color="black")),
                ft.DataCell(ft.Text("A tiempo", color="black")),
                ft.DataCell(ft.Row([self.build_btn_extender(), self.build_btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ABCDEFGA", color="black")),
                ft.DataCell(ft.Text("Figueroa Sales", color="black")),
                ft.DataCell(ft.Text("Python Básico", color="black")),
                ft.DataCell(ft.Text("Atrasado", color="black")),
                ft.DataCell(ft.Row([self.build_btn_extender(), self.build_btn_devolver()], spacing=10)),
            ]),
        ]

        # --- Contenedor de Filtros Superiores ---
        filtros = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.input_busqueda,
                    self.dropdown_estado,
                    ft.ElevatedButton(
                        "Buscar",
                        # on_click=self.buscar_prestamos, # Conectar a lógica futura
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

        # --- Contenedor con Scroll para la Tabla ---
        tabla_scroll = ft.Container(
            expand=True,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [self.tabla],
                scroll=ft.ScrollMode.AUTO  
            )
        )

        # --- Ensamblaje Final ---
        self.content = ft.Column(
            [
                ft.Text("Préstamos de libros", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona los préstamos de libros registrados en el sistema",
                    color="black"
                ),
                filtros,
                tabla_scroll
            ],
            spacing=20,
            expand=True
        )
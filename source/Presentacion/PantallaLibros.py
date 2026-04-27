import flet as ft


class PantallaLibros(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        self.AZUL = "#3B82F6"
        self.FONDO = "#EAF1F7"

        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # =============================
        # BASE LOCAL TEMPORAL
        # =============================
        self.libros = [
            {"titulo": "El principito", "autor": "Antoine", "estado": "Disponible"},
            {"titulo": "1984", "autor": "Orwell", "estado": "Prestado"},
            {"titulo": "Cien años", "autor": "García Márquez", "estado": "Disponible"},
            {"titulo": "Don Quijote", "autor": "Cervantes", "estado": "Disponible"},
        ]

        # =============================
        # FILTROS
        # =============================
        self.input_busqueda = ft.TextField(
            width=250,
            hint_text="Buscar por título o autor...",
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

    # =====================================================
    # CAMPO ESTILIZADO
    # =====================================================
    def campo_negro(self, label, hint=None):
        return ft.TextField(
            label=label,
            hint_text=hint,
            color="black",
            bgcolor="white",
            cursor_color="black",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#6B7280"),
            label_style=ft.TextStyle(color="black"),
            expand=True
        )

    # =====================================================
    # CARD LIBRO
    # =====================================================
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
                    ft.Text(titulo, weight="bold", size=14, color="black"),
                    ft.Text(autor, size=12, color="black"),
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

    # =====================================================
    # REFRESCAR GRID
    # =====================================================
    def refrescar_grid(self, libros_filtrados=None):
        datos = libros_filtrados if libros_filtrados else self.libros

        self.grid_libros.controls = [
            self.build_card_libro(
                libro["titulo"],
                libro["autor"],
                libro["estado"]
            )
            for libro in datos
        ]

        self._page.update()

    # =====================================================
    # BUSCAR
    # =====================================================
    def buscar_libros(self, e):
        texto = (self.input_busqueda.value or "").lower()
        estado = self.dropdown_disponibilidad.value or "Todos"

        filtrados = []

        for libro in self.libros:
            coincide_texto = (
                texto in libro["titulo"].lower()
                or texto in libro["autor"].lower()
            )

            coincide_estado = (
                estado == "Todos"
                or libro["estado"] == estado
            )

            if coincide_texto and coincide_estado:
                filtrados.append(libro)

        self.refrescar_grid(filtrados)

    # =====================================================
    # CERRAR DIALOG
    # =====================================================
    def cerrar_dialog(self, dialog):
        dialog.open = False
        self._page.update()

    # =====================================================
    # MODAL
    # =====================================================
    def abrir_modal_agregar(self, e):

        isbn = self.campo_negro("ISBN")
        titulo = self.campo_negro("Título")

        autor = ft.Dropdown(
            label="Autor",
            bgcolor="white",
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            expand=True,
            options=[
                ft.dropdown.Option(text="Gabriel García Márquez"),
                ft.dropdown.Option(text="George Orwell"),
            ]
        )

        editorial = ft.Dropdown(
            label="Editorial",
            bgcolor="white",
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            expand=True,
            options=[
                ft.dropdown.Option(text="Penguin"),
                ft.dropdown.Option(text="Planeta"),
            ]
        )

        categoria = ft.Dropdown(
            label="Categoría",
            bgcolor="white",
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            expand=True,
            options=[
                ft.dropdown.Option(text="Literatura"),
                ft.dropdown.Option(text="Programación"),
            ]
        )

        edicion = self.campo_negro("Edición")
        fecha = self.campo_negro("Fecha impresión", "YYYY-MM-DD")
        dewey = self.campo_negro("Dewey")
        cdu = self.campo_negro("CDU")
        lcc = self.campo_negro("LCC")
        ejemplares = self.campo_negro("Cantidad de ejemplares")

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#F8FAFC",
            title=ft.Text("Añadir libro", color="black"),
            content=ft.Container(
                width=800,
                content=ft.Column(
                    [
                        ft.Row([isbn, titulo], spacing=15),
                        ft.Row([autor, editorial], spacing=15),
                        ft.Row([categoria, edicion], spacing=15),
                        ft.Row([fecha, ejemplares], spacing=15),
                        ft.Row([dewey, cdu, lcc], spacing=15),
                    ],
                    spacing=15,
                    tight=True
                )
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(color="#2563EB"),
                    on_click=lambda ev: self.cerrar_dialog(dialog)
                ),
                ft.ElevatedButton(
                    "Guardar",
                    bgcolor=self.AZUL,
                    color="white",
                    on_click=lambda ev: self.guardar_libro(
                        dialog,
                        titulo,
                        autor
                    )
                )
            ]
        )

        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()

    # =====================================================
    # GUARDAR
    # =====================================================
    def guardar_libro(self, dialog, titulo, autor):

        if not titulo.value or not autor.value:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Título y Autor son obligatorios")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        self.libros.append({
            "titulo": titulo.value,
            "autor": autor.value,
            "estado": "Disponible"
        })

        dialog.open = False

        self.refrescar_grid()

        self._page.snack_bar = ft.SnackBar(
            ft.Text("Libro añadido correctamente")
        )
        self._page.snack_bar.open = True
        self._page.update()

    # =====================================================
    # UI
    # =====================================================
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
                        on_click=self.abrir_modal_agregar,
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
                ft.Text("Catálogo de libros", size=32, weight="bold", color="black"),
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
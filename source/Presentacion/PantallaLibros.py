import flet as ft
from Infraestructura.API.libros_api import crear_libro, obtener_libros

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

        self.autores_seleccionados = []
        self.categorias_seleccionadas = []

        self.chips_autores = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8
        )

        self.chips_categorias = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8
        )

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

    # Campo de texto estilizado
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
    
    # Card libro
    def build_card_libro(self, titulo, isbn, estado):
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

    # Refrescar grid
    def refrescar_grid(self, libros_filtrados=None):
        try:
            if libros_filtrados:
                datos = libros_filtrados
            else:
                response = obtener_libros()

                if response.status_code != 200:
                    self._page.snack_bar = ft.SnackBar(
                        ft.Text("Error al cargar libros")
                    )
                    self._page.snack_bar.open = True
                    self._page.update()
                    return

                datos = response.json()["contenido"]

            self.grid_libros.controls = [
                self.build_card_libro(
                    libro["titulo"],
                    libro["isbn"],
                    "Disponible"
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

    # Cerrar dialog
    def cerrar_dialog(self, dialog):
        dialog.open = False
        self._page.update()

    def agregar_autor_chip(self, autor_input):
        nombre = autor_input.value.strip()

        if not nombre:
            return

        if nombre in self.autores_seleccionados:
            return

        self.autores_seleccionados.append(nombre)

        chip = ft.Chip(
            label=ft.Text(nombre),
            on_delete=lambda e, n=nombre: self.eliminar_autor_chip(n)
        )

        self.chips_autores.controls.append(chip)

        autor_input.value = ""

        self._page.update()

    def eliminar_autor_chip(self, nombre):
        self.autores_seleccionados.remove(nombre)

        self.chips_autores.controls = [
            chip for chip in self.chips_autores.controls
            if chip.label.value != nombre
        ]

        self._page.update()

    def agregar_categoria_chip(self, categoria_input):
        nombre = categoria_input.value.strip()

        if not nombre:
            return

        if nombre in self.categorias_seleccionadas:
            return

        self.categorias_seleccionadas.append(nombre)

        chip = ft.Chip(
            label=ft.Text(nombre),
            on_delete=lambda e, n=nombre: self.eliminar_categoria_chip(n)
        )

        self.chips_categorias.controls.append(chip)

        categoria_input.value = ""

        self._page.update()

    def eliminar_categoria_chip(self, nombre):
        self.categorias_seleccionadas.remove(nombre)

        self.chips_categorias.controls = [
            chip for chip in self.chips_categorias.controls
            if chip.label.value != nombre
        ]

        self._page.update()                

    # Modal agregar libro
    def abrir_modal_agregar(self, e):

        self.autores_seleccionados = []
        self.categorias_seleccionadas = []

        self.chips_autores.controls.clear()
        self.chips_categorias.controls.clear()

        isbn = self.campo_negro("ISBN")
        titulo = self.campo_negro("Título")

        # INPUT AUTORES
        autor_input = self.campo_negro("Autor")

        boton_agregar_autor = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="white",
            bgcolor="#6366F1",
            on_click=lambda ev: self.agregar_autor_chip(autor_input)
        )

        # INPUT CATEGORIAS
        categoria_input = self.campo_negro("Categoría")

        boton_agregar_categoria = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="white",
            bgcolor="#10B981",
            on_click=lambda ev: self.agregar_categoria_chip(categoria_input)
        )

        editorial = self.campo_negro("Editorial")
        edicion = self.campo_negro("Edición")
        fecha = self.campo_negro("Fecha impresión", "YYYY-MM-DD")
        ejemplares = self.campo_negro("Cantidad de ejemplares")
        dewey = self.campo_negro("Dewey")
        cdu = self.campo_negro("CDU")
        lcc = self.campo_negro("LCC")

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#F8FAFC",
            title=ft.Text("Añadir libro", color="black"),
            content=ft.Container(
                width=900,
                content=ft.Column(
                    [
                        ft.Row([isbn, titulo], spacing=15),

                        ft.Text(
                            "Autores",
                            size=13,
                            weight="bold",
                            color="#374151"
                        ),

                        ft.Row(
                            [
                                autor_input,
                                boton_agregar_autor
                            ],
                            spacing=10
                        ),

                        self.chips_autores,

                        ft.Text(
                            "Categorías",
                            size=13,
                            weight="bold",
                            color="#374151"
                        ),

                        ft.Row(
                            [
                                categoria_input,
                                boton_agregar_categoria
                            ],
                            spacing=10
                        ),

                        self.chips_categorias,

                        ft.Row([editorial], spacing=15),
                        ft.Row([edicion, fecha], spacing=15),
                        ft.Row([ejemplares], spacing=15),
                        ft.Row([dewey, cdu, lcc], spacing=15),
                    ],
                    spacing=15,
                    tight=True
                )
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda ev: self.cerrar_dialog(dialog)
                ),
                ft.ElevatedButton(
                    "Guardar",
                    bgcolor=self.AZUL,
                    color="white",
                    on_click=lambda ev: self.guardar_libro(
                        dialog,
                        isbn,
                        titulo,
                        editorial,
                        ejemplares
                    )
                )
            ]
        )

        self._page.overlay.append(dialog)
        dialog.open = True
        self._page.update()

    # Guardar libro
    def guardar_libro(self, dialog, isbn, titulo, editorial, ejemplares):

        if not isbn.value or not titulo.value:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("ISBN y Título son obligatorios")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        if not editorial.value:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar una editorial")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        if not ejemplares.value.strip():
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Debes ingresar la cantidad de ejemplares")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        if not ejemplares.value.isdigit() or int(ejemplares.value) <= 0:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("La cantidad de ejemplares debe ser un número mayor a 0")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        if not self.autores_seleccionados:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Debes agregar al menos un autor")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        if not self.categorias_seleccionadas:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Debes agregar al menos una categoría")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        try:
            data = {
                "isbn": isbn.value.strip(),
                "titulo": titulo.value.strip(),
                "editorial": editorial.value.strip(),
                "edicion": "",
                "fechaPublicacion": None,
                "dewey": "",
                "clasificacionDelCongreso": "",
                "clasificacionDecimalUniversal": "",
                "autores": self.autores_seleccionados,
                "categorias": self.categorias_seleccionadas,
                "nEjemplares": int(ejemplares.value)
            }

            print("DATA ENVIADA:", data)

            response = crear_libro(data)

            print("STATUS:", response.status_code)
            print("RESPUESTA:", response.text)

            if response.status_code == 201:
                dialog.open = False

                self.refrescar_grid()

                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Libro añadido correctamente")
                )
            else:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error API: {response.text}")
                )

            self._page.snack_bar.open = True
            self._page.update()

        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"Error conexión API: {str(e)}")
            )
            self._page.snack_bar.open = True
            self._page.update()

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
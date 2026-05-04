import flet as ft
import datetime

from Infraestructura.API.libros_api import crear_libro


class PantallaRegistrarLibro(ft.Container):

    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()

        self._page = page
        self.vista_anterior = vista_anterior

        self.expand = True
        self.alignment = ft.Alignment(0, 0)

        # Colores
        self.AZUL = "#3B82F6"
        self.GRIS_BORDE = "#D1D5DB"
        self.GRIS_TEXTO = "#6B7280"
        self.TEXT = "#111827"
        self.CARD = "white"

        # Datos dinámicos
        self.autores_seleccionados = []
        self.categorias_seleccionadas = []

        # ========================
        # INPUTS
        # ========================
        self.txt_isbn = self.crear_input("ISBN", 350)
        self.txt_titulo = self.crear_input("Título", 350)
        self.txt_editorial = self.crear_input("Editorial", 350)

        self.txt_edicion = self.crear_input("Edición", 165)
        self.txt_ejemplares = self.crear_input("Cantidad de ejemplares", 165)

        self.txt_dewey = self.crear_input("Dewey", 110)
        self.txt_cdu = self.crear_input("CDU", 110)
        self.txt_lcc = self.crear_input("LCC", 110)

        # ========================
        # AUTORES
        # ========================
        self.txt_autor = self.crear_input("Autor", 300)

        self.chips_autores = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8
        )

        # ========================
        # CATEGORÍAS
        # ========================
        self.txt_categoria = self.crear_input("Categoría", 300)

        self.chips_categorias = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8
        )

        # ========================
        # CALENDARIO
        # ========================
        self.calendario = ft.DatePicker(
            on_change=self.seleccionar_fecha,
            first_date=datetime.datetime(1900, 1, 1),
            last_date=datetime.datetime.now()
        )

        self._page.overlay.append(self.calendario)

        self.txt_fecha = ft.TextField(
            label="Fecha de publicación",
            width=350,
            read_only=True,
            border_radius=12,
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.abrir_calendario
        )

        self.build_ui()

    # ========================
    # HELPERS
    # ========================
    def crear_input(self, label, width):
        return ft.TextField(
            label=label,
            width=width,
            border_radius=12,
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT)
        )

    # ========================
    # FECHA
    # ========================
    def abrir_calendario(self, e):
        self.calendario.open = True
        self._page.update()

    def seleccionar_fecha(self, e):
        if self.calendario.value:
            self.txt_fecha.value = self.calendario.value.strftime("%Y-%m-%d")
            self.txt_fecha.update()

    # ========================
    # AUTORES
    # ========================
    def agregar_autor(self, e):
        nombre = self.txt_autor.value.strip()

        if not nombre or nombre in self.autores_seleccionados:
            return

        self.autores_seleccionados.append(nombre)

        chip = ft.Chip(
            label=ft.Text(nombre),
            on_delete=lambda ev, n=nombre: self.eliminar_autor(n)
        )

        self.chips_autores.controls.append(chip)

        self.txt_autor.value = ""

        self.update()

    def eliminar_autor(self, nombre):
        self.autores_seleccionados.remove(nombre)

        self.chips_autores.controls = [
            chip for chip in self.chips_autores.controls
            if chip.label.value != nombre
        ]

        self.update()

    # ========================
    # CATEGORÍAS
    # ========================
    def agregar_categoria(self, e):
        nombre = self.txt_categoria.value.strip()

        if not nombre or nombre in self.categorias_seleccionadas:
            return

        self.categorias_seleccionadas.append(nombre)

        chip = ft.Chip(
            label=ft.Text(nombre),
            on_delete=lambda ev, n=nombre: self.eliminar_categoria(n)
        )

        self.chips_categorias.controls.append(chip)

        self.txt_categoria.value = ""

        self.update()

    def eliminar_categoria(self, nombre):
        self.categorias_seleccionadas.remove(nombre)

        self.chips_categorias.controls = [
            chip for chip in self.chips_categorias.controls
            if chip.label.value != nombre
        ]

        self.update()

    # ========================
    # REGRESAR
    # ========================
    def regresar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.refrescar_grid()

            parent = self.parent
            if parent:
                parent.content = self.vista_anterior
                parent.update()

    # ========================
    # LIMPIAR FORMULARIO
    # ========================
    def limpiar_formulario(self):
        self.txt_isbn.value = ""
        self.txt_titulo.value = ""
        self.txt_editorial.value = ""
        self.txt_edicion.value = ""
        self.txt_fecha.value = ""
        self.txt_ejemplares.value = ""
        self.txt_dewey.value = ""
        self.txt_cdu.value = ""
        self.txt_lcc.value = ""
        self.txt_autor.value = ""
        self.txt_categoria.value = ""

        self.autores_seleccionados.clear()
        self.categorias_seleccionadas.clear()

        self.chips_autores.controls.clear()
        self.chips_categorias.controls.clear()

        self.update()

    # ========================
    # GUARDAR
    # ========================
    def guardar_libro(self, e):

        if not self.txt_isbn.value or not self.txt_titulo.value:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("ISBN y Título son obligatorios")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        try:
            n_ejemplares = int(self.txt_ejemplares.value)

        except ValueError:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("La cantidad de ejemplares debe ser un número válido")
            )
            self._page.snack_bar.open = True
            self._page.update()
            return

        data = {
            "isbn": self.txt_isbn.value.strip(),
            "titulo": self.txt_titulo.value.strip(),
            "editorial": self.txt_editorial.value.strip(),
            "edicion": self.txt_edicion.value.strip(),
            "fechaPublicacion": self.txt_fecha.value or None,
            "dewey": self.txt_dewey.value.strip(),
            "clasificacionDelCongreso": self.txt_lcc.value.strip(),
            "clasificacionDecimalUniversal": self.txt_cdu.value.strip(),
            "autores": self.autores_seleccionados,
            "categorias": self.categorias_seleccionadas,
            "nEjemplares": n_ejemplares
        }

        response = crear_libro(data)

        if response.status_code == 201:

            self._page.snack_bar = ft.SnackBar(
                ft.Text("Libro registrado correctamente")
            )

            self.limpiar_formulario()

            # Refresca catálogo en segundo plano
            if self.vista_anterior:
                self.vista_anterior.refrescar_grid()

        else:

            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"Error API: {response.text}")
            )

        self._page.snack_bar.open = True
        self._page.update()

    # ========================
    # UI
    # ========================
    def build_ui(self):

        formulario = ft.Column(
            [
                self.txt_isbn,
                self.txt_titulo,
                self.txt_editorial,

                ft.Row(
                    [
                        self.txt_edicion,
                        self.txt_fecha
                    ],
                    spacing=20
                ),

                self.txt_ejemplares,

                ft.Row(
                    [
                        self.txt_dewey,
                        self.txt_cdu,
                        self.txt_lcc
                    ],
                    spacing=15
                ),

                ft.Divider(),

                ft.Text("Autores", weight="bold"),

                ft.Row(
                    [
                        self.txt_autor,
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            bgcolor=self.AZUL,
                            icon_color="white",
                            on_click=self.agregar_autor
                        )
                    ]
                ),

                self.chips_autores,

                ft.Divider(),

                ft.Text("Categorías", weight="bold"),

                ft.Row(
                    [
                        self.txt_categoria,
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            bgcolor="#10B981",
                            icon_color="white",
                            on_click=self.agregar_categoria
                        )
                    ]
                ),

                self.chips_categorias
            ],
            spacing=15
        )

        inner_card = ft.Container(
            bgcolor=self.CARD,
            padding=40,
            border_radius=30,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color="black26"
            ),
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.MENU_BOOK,
                        size=50,
                        color=self.AZUL
                    ),

                    ft.Text(
                        "Registrar Libro",
                        size=26,
                        weight="bold",
                        color=self.TEXT
                    ),

                    ft.Text(
                        "Registro detallado de libros al catálogo",
                        size=14,
                        color=self.GRIS_TEXTO
                    ),

                    ft.Divider(height=15, color="transparent"),

                    formulario,

                    ft.Divider(height=15, color="transparent"),

                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "Regresar",
                                on_click=self.regresar,
                                style=ft.ButtonStyle(
                                    color="red"
                                )
                            ),

                            ft.ElevatedButton(
                                "Guardar Libro",
                                bgcolor=self.AZUL,
                                color="white",
                                width=180,
                                on_click=self.guardar_libro
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.content = ft.Column(
            [
                ft.Container(
                    width=700,
                    border_radius=40,
                    padding=30,
                    gradient=ft.LinearGradient(
                        colors=["#cfe8ff", "#9ec9ff"],
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1)
                    ),
                    content=inner_card
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
import flet as ft
import datetime
from Negocio.Controlador.ControladorRegistroLibro import ControladorRegistroLibro

class PantallaRegistrarLibro(ft.Container):

    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()

        self._page = page
        self.vista_anterior = vista_anterior
        self.controller = ControladorRegistroLibro()
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

        # INPUTS
        self.txt_isbn = self.crear_input("ISBN", 300)
        self.txt_isbn.on_change = self.limpiar_mensaje_isbn

        self.boton_buscar_isbn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SEARCH, size=18),
                    ft.Text("Buscar ISBN")
                ],
                spacing=5,
                tight=True
            ),
            bgcolor=self.AZUL,
            color="white",
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            on_click=self.buscar_isbn
        )

        self.txt_titulo = self.crear_input("Título", 350)
        self.txt_editorial = self.crear_input("Editorial", 350)

        self.txt_edicion = self.crear_input("Edición", 165)
        self.txt_ejemplares = self.crear_input("Cantidad de ejemplares", 165)

        self.txt_dewey = self.crear_input("Dewey", 110)
        self.txt_cdu = self.crear_input("CDU", 110)
        self.txt_lcc = self.crear_input("LCC", 110)

        self.txt_autor = self.crear_input("Autor", 300)

        self.chips_autores = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.txt_categoria = self.crear_input("Categoría", 300)

        self.chips_categorias = ft.Row(
            wrap=True,
            spacing=8,
            run_spacing=8,
            alignment=ft.MainAxisAlignment.CENTER
        )

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

    # HELPERS
    def crear_input(self, label, width):
        return ft.TextField(
            label=label,
            width=width,
            border_radius=12,
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            on_change=self.verificar_campos_completos
        )

    # FECHA
    def abrir_calendario(self, e):
        self.calendario.open = True
        self._page.update()

    def seleccionar_fecha(self, e):
        if self.calendario.value:
            self.txt_fecha.value = self.calendario.value.strftime("%Y-%m-%d")
            self.txt_fecha.update()

    # AUTORES
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

    # CATEGORÍAS
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

    # REGRESAR
    def regresar(self, e):
        from Presentacion.PantallaLibros import PantallaLibros

        parent = self.parent

        if parent:
            parent.content = PantallaLibros(self._page)
            parent.update()

    def validar_campos(self):

        valido = True

        campos_obligatorios = [
            self.txt_isbn,
            self.txt_titulo,
            self.txt_editorial,
            self.txt_fecha,
            self.txt_ejemplares
        ]

        for campo in campos_obligatorios:
            if not campo.value.strip():
                campo.border_color = "red"
                valido = False
            else:
                campo.border_color = self.GRIS_BORDE

        self.update()

        return valido

    def verificar_campos_completos(self, e=None):

        obligatorios = [
            self.txt_isbn,
            self.txt_titulo,
            self.txt_editorial,
            self.txt_ejemplares
        ]

        for campo in obligatorios:
            if campo.value and campo.value.strip():
                campo.border_color = self.GRIS_BORDE

        self.update()

    # LIMPIAR FORMULARIO
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

        self.verificar_campos_completos()

        self.update()

    # GUARDAR
    def guardar_libro(self, e):

        if not self.validar_campos():
            self.lbl_mensaje.value = "Completa los campos obligatorios"
            self.lbl_mensaje.color = "red"
            self.lbl_mensaje.visible = True
            self.update()
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
            "nEjemplares": self.txt_ejemplares.value
        }

        resultado = self.controller.crear_libro(data)

        self.lbl_mensaje.value = resultado["mensaje"]
        self.lbl_mensaje.color = "green" if resultado["ok"] else "red"
        self.lbl_mensaje.visible = True

        if resultado["ok"]:
            self.limpiar_formulario()

        self.update()

    # UI
    def build_ui(self):

        self.btn_guardar = ft.ElevatedButton(
            "Guardar Libro",
            bgcolor=self.AZUL,
            color="white",
            width=180,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            on_click=self.guardar_libro
        )

        self.lbl_mensaje = ft.Text(
            "",
            size=13,
            weight="bold",
            text_align=ft.TextAlign.CENTER,
            visible=False
        )

        self.lbl_isbn = ft.Text(
            "",
            size=12,
            color="red",
            visible=False
        )

        formulario = ft.Column(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.txt_isbn,
                                self.boton_buscar_isbn
                            ],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),

                        ft.Row(
                            [self.lbl_isbn],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    spacing=5
                ),

                ft.Row(
                    [self.txt_titulo],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [self.txt_editorial],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [
                        self.txt_edicion,
                        self.txt_ejemplares
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [self.txt_fecha],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [
                        self.txt_dewey,
                        self.txt_cdu,
                        self.txt_lcc
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Divider(),

                ft.Row(
                    [ft.Text("Autores", weight="bold")],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [
                        self.txt_autor,
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            bgcolor=self.AZUL,
                            icon_color="white",
                            on_click=self.agregar_autor
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),

                ft.Container(
                    content=self.chips_autores,
                    alignment=ft.Alignment(0, 0)
                ),

                ft.Divider(),

                ft.Row(
                    [ft.Text("Categorías", weight="bold")],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Row(
                    [
                        self.txt_categoria,
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            bgcolor="#10B981",
                            icon_color="white",
                            on_click=self.agregar_categoria
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),

                ft.Container(
                    content=self.chips_categorias,
                    alignment=ft.Alignment(0, 0)
                )
            ],
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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

                    ft.Divider(height=10, color="transparent"),

                    self.lbl_mensaje,

                    ft.Divider(height=5, color="transparent"),

                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "Regresar",
                                on_click=self.regresar,
                                style=ft.ButtonStyle(color="red")
                            ),

                            self.btn_guardar
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
                    width=760,
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

    def buscar_isbn(self, e):

        isbn = self.txt_isbn.value.strip()

        resultado = self.controller.buscar_por_isbn(isbn)

        if not resultado["ok"]:
            self.lbl_isbn.value = resultado["mensaje"]
            self.lbl_isbn.color = "red"
            self.lbl_isbn.visible = True
            self.update()
            return

        self.lbl_isbn.value = "ISBN encontrado correctamente"
        self.lbl_isbn.color = "green"
        self.lbl_isbn.visible = True

        data = resultado["data"]

        self.txt_titulo.value = data["titulo"]
        self.txt_editorial.value = data["editorial"]
        self.txt_fecha.value = data["fecha"]
        self.txt_edicion.value = data["edicion"]
        self.txt_dewey.value = data["dewey"]
        self.txt_cdu.value = data["cdu"]
        self.txt_lcc.value = data["lcc"]

        self.autores_seleccionados = data["autores"]
        self.chips_autores.controls.clear()

        for autor in data["autores"]:
            self.chips_autores.controls.append(
                ft.Chip(
                    label=ft.Text(autor),
                    on_delete=lambda ev, n=autor: self.eliminar_autor(n)
                )
            )

        self.categorias_seleccionadas = data["categorias"]
        self.chips_categorias.controls.clear()

        for cat in data["categorias"]:
            self.chips_categorias.controls.append(
                ft.Chip(
                    label=ft.Text(cat),
                    on_delete=lambda ev, n=cat: self.eliminar_categoria(n)
                )
            )

        self.verificar_campos_completos()
        self.update()


    def limpiar_mensaje_isbn(self, e):
        self.lbl_isbn.visible = False
        self.update()
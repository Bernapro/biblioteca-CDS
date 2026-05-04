import flet as ft
from Presentacion.PantallaRegistrarLibro import PantallaRegistrarLibro
from Infraestructura.API.libros_api import obtener_libros


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

        # PAGINACIÓN
        self.pagina_actual = 0
        self.tamano_pagina = 10
        self.total_paginas = 1
        self.total_elementos = 0
        self.busqueda_actual = ""

        # COMPONENTES PAGINACIÓN
        self.info_paginacion = ft.Text(
            "",
            color="black",
            size=14
        )

        self.paginacion = ft.Row(
            spacing=8,
            wrap=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.END
        )

        # FILTROS
        self.input_busqueda = ft.TextField(
            width=250,
            hint_text="Buscar por título o ISBN...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            bgcolor="white",
            on_submit=self.buscar_libros
        )

        # GRID
        self.grid_libros = ft.GridView(
            expand=True,
            runs_count=4,
            max_extent=220,
            spacing=20,
            run_spacing=20,
        )

        self.build_ui()
        self.refrescar_grid()

    # ===============================
    # CARD LIBRO
    # ===============================
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

    # ===============================
    # CARGAR LIBROS PAGINADOS
    # ===============================
    def refrescar_grid(self):
        print("ENTRO A refrescar_grid()", flush=True)
        try:
            response = obtener_libros(
                n_page=self.pagina_actual,
                length=self.tamano_pagina,
                busqueda=self.busqueda_actual
            )

            if response.status_code != 200:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Error al cargar libros")
                )
                self._page.snack_bar.open = True
                self._page.update()
                return

            datos = response.json()
            print("RESPUESTA API:", datos, flush=True)

            libros = datos["contenido"]
            if not libros:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("No se encontraron libros")
                )
                self._page.snack_bar.open = True

            self.total_paginas = datos["totalPaginas"]
            self.total_elementos = datos["totalElementos"]

            self.grid_libros.controls = [
                self.build_card_libro(
                    libro["titulo"],
                    libro["isbn"],
                    libro["Ejemplares"]
                )
                for libro in libros
            ]

            if self.total_elementos == 0:
                inicio = 0
                fin = 0
            else:
                inicio = (self.pagina_actual * self.tamano_pagina) + 1
                fin = min(
                    inicio + len(libros) - 1,
                    self.total_elementos
                )

            self.info_paginacion.value = (
                f"Mostrando {inicio}-{fin} de "
                f"{self.total_elementos} libros"
            )

            self.actualizar_paginacion()

            self._page.update()

        except Exception as e:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(e)}")
            )
            self._page.snack_bar.open = True
            self._page.update()

    # ===============================
    # CAMBIAR PÁGINA
    # ===============================
    def cambiar_pagina(self, nueva_pagina):
        self.pagina_actual = nueva_pagina
        self.refrescar_grid()

    def ir_a_pagina_directa(self, e):
        try:
            pagina = int(e.control.value)

            if 1 <= pagina <= self.total_paginas:
                self.cambiar_pagina(pagina - 1)
            else:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Página fuera de rango")
                )
                self._page.snack_bar.open = True
                self._page.update()

        except ValueError:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Ingresa un número válido")
            )
            self._page.snack_bar.open = True
            self._page.update()    

    # ===============================
    # GENERAR BOTONES PAGINACIÓN
    # ===============================
    def actualizar_paginacion(self):
        self.paginacion.controls.clear()

        inicio = max(0, self.pagina_actual - 2)
        fin = min(self.total_paginas, inicio + 5)

        if fin - inicio < 5:
            inicio = max(0, fin - 5)

        # BOTÓN ANTERIOR
        self.paginacion.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                disabled=self.pagina_actual == 0,
                on_click=lambda e: self.cambiar_pagina(self.pagina_actual - 1)
            )
        )

        # BOTONES NUMÉRICOS
        for i in range(inicio, fin):
            activo = i == self.pagina_actual

            self.paginacion.controls.append(
                ft.ElevatedButton(
                    str(i + 1),
                    width=45,
                    height=45,
                    on_click=lambda e, pagina=i: self.cambiar_pagina(pagina),
                    style=ft.ButtonStyle(
                        bgcolor=self.AZUL if activo else "white",
                        color="white" if activo else "black",
                        padding=0,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                )
            )

        # BOTÓN SIGUIENTE
        self.paginacion.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                disabled=self.pagina_actual >= self.total_paginas - 1,
                on_click=lambda e: self.cambiar_pagina(self.pagina_actual + 1)
            )
        )

        # INPUT IR A PÁGINA
        self.paginacion.controls.append(
            ft.TextField(
                width=65,
                height=40,
                value=str(self.pagina_actual + 1),
                hint_text="Página",
                text_align=ft.TextAlign.CENTER,
                content_padding=8,
                border_radius=8,
                on_submit=self.ir_a_pagina_directa
            )
        )

    # ===============================
    # BUSCAR (TEMPORAL)
    # ===============================
    def buscar_libros(self, e):
        self.busqueda_actual = self.input_busqueda.value.strip()
        self.pagina_actual = 0
        self.refrescar_grid()

    # ===============================
    # IR A REGISTRO
    # ===============================
    def ir_a_registro_libro(self, e):
        self.content = PantallaRegistrarLibro(
            self._page,
            vista_anterior=self
        )
        self.update()

    # ===============================
    # UI
    # ===============================
    def build_ui(self):

        filtros = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.input_busqueda,

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

                ft.Container(
                    expand=True,
                    content=self.grid_libros
                ),

                ft.Container(
                    padding=ft.padding.only(top=10),
                    content=ft.Row(
                        [
                            self.info_paginacion,

                            ft.Container(
                                expand=True,
                                alignment=ft.Alignment(1, 0),
                                content=self.paginacion
                            )
                        ]
                    )
                )
            ],
            spacing=20,
            expand=True
        )
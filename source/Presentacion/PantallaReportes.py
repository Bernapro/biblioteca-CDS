import flet as ft

class PantallaReportes(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.AZUL_FUERTE = "#2563EB"
        self.AZUL_CLARO = "#60A5FA"
        self.FONDO = "#EAF1F7"

        # Propiedades del Contenedor Principal (Fondo de la vista)
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== TARJETAS =====
    def build_stat_card(self, title, value, icon):
        return ft.Container(
            width=260,
            height=110,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    ft.Icon(icon, size=30, color=self.AZUL),
                    ft.Column(
                        [
                            ft.Text(title, size=14, color="black"),
                            ft.Text(str(value), size=28, weight="bold", color="black"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=15
            )
        )

    # ===== FILTROS =====
    def build_combo(self, label):
        return ft.Dropdown(
            width=150,
            label=label,
            options=[
                ft.dropdown.Option("Opción 1"),
                ft.dropdown.Option("Opción 2")
            ],
            color="black",  # texto seleccionado
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            border_color="#D1D5DB",
            focused_border_color=self.AZUL
        )

    def build_filtros(self):
        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.build_combo("Fecha inicio"),
                    self.build_combo("Fecha fin"),
                    self.build_combo("Todos"),
                    self.build_combo("Usuario"),

                    ft.ElevatedButton(
                        "Generar reporte",
                        # on_click=self.generar_reporte, # Para cuando conectes la BD
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

    # ===== GRÁFICA BARRAS =====
    def build_visitas_chart(self):
        return ft.Container(
            expand=True,
            height=300,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Visitas por día", size=14, color="black"),
                    ft.Text("Gráfica", weight="bold", color="black"),

                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 1),
                        content=ft.Row(
                            [
                                ft.Container(width=35, height=110, bgcolor=self.AZUL, border_radius=6),
                                ft.Container(width=35, height=170, bgcolor=self.AZUL_FUERTE, border_radius=6),
                                ft.Container(width=35, height=90, bgcolor=self.AZUL_CLARO, border_radius=6),
                                ft.Container(width=35, height=150, bgcolor=self.AZUL_FUERTE, border_radius=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        )
                    )
                ]
            )
        )

    # ===== DONUT CHART =====
    def build_donut_chart(self):
        return ft.Container(
            expand=True,
            height=260,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Préstamos totales", size=14, color="black"),

                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Stack(
                            alignment=ft.Alignment(0, 0),
                            controls=[
                                ft.ProgressRing(
                                    value=1,
                                    stroke_width=20,
                                    width=160,
                                    height=160,
                                    color="#E5E7EB",
                                ),
                                ft.ProgressRing(
                                    value=0.72,
                                    stroke_width=20,
                                    width=160,
                                    height=160,
                                    color=self.AZUL,
                                ),
                                ft.Column(
                                    [
                                        ft.Text("72%", size=22, weight="bold", color="black"),
                                        ft.Text("Completados", size=10, color="black"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ]
                        )
                    )
                ]
            )
        )

    # ===== TOP LIBROS =====
    def build_item_libro(self, nombre, cantidad):
        return ft.Row(
            [
                ft.Icon(ft.Icons.MENU_BOOK, size=18, color=self.AZUL),
                ft.Text(nombre, color="black"),
                ft.Text(f"{cantidad} préstamos", color="black")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def build_top_books(self):
        return ft.Container(
            expand=True,
            height=160,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Libros más prestados", weight="bold", color="black"),
                    self.build_item_libro("Libro 1", 28),
                    self.build_item_libro("Libro 2", 32),
                    self.build_item_libro("Libro 3", 12),
                ]
            )
        )

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        self.content = ft.Column(
            [
                ft.Text("Reportes", size=32, weight="bold", color="black"),
                ft.Text("Estadísticas generales del sistema", color="black"),

                self.build_filtros(),

                ft.Row(
                    [
                        self.build_stat_card("Asistencias", 532, ft.Icons.PERSON),
                        self.build_stat_card("Préstamos", 292, ft.Icons.SWAP_HORIZ),
                        self.build_stat_card("Vencidos", 93, ft.Icons.WARNING),
                    ],
                    spacing=20
                ),

                ft.Row(
                    [
                        ft.Container(expand=2, content=self.build_visitas_chart()),
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                [
                                    self.build_donut_chart(),
                                    self.build_top_books()
                                ],
                                spacing=15
                            )
                        )
                    ],
                    expand=True
                )
            ],
            spacing=20
        )
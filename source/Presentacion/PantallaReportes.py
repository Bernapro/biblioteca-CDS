import flet as ft


class PantallaReportes(ft.Container):

    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page

        # ===== COLORES (modo oscuro) =====
        self.AZUL = "#2563EB"
        self.PURPURA = "#7C3AED"
        self.VERDE = "#059669"

        self.TEXT = "onSurface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.CARD = "surface"
        self.BORDER = "outline"

        self.expand = True
        self.padding = 20
        self.bgcolor = "transparent"

        self.tipo_actual = "Alumnos"

        self.fecha_inicio_picker = ft.DatePicker()
        self.fecha_fin_picker = ft.DatePicker()

        # labels distribución
        self.total_usuarios = 185

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        self.cards_row = ft.Row(spacing=20)

        self.content = ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                # ===== HEADER =====
                ft.Column([
                    ft.Text("Reportes", size=28, weight="bold", color=self.TEXT),
                    ft.Text("Estadísticas del sistema", color=self.TEXT_SECONDARY),
                ]),

                # ===== FILTROS =====
                self.build_filtros(),

                # ===== CARDS =====
                self.cards_row,

                # ===== GRAFICAS =====
                ft.Row(
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        self.build_bar_chart(),
                        self.build_distribution_panel()
                    ]
                ),

                # ===== FOOTER =====
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Última actualización: 31/05/2025 10:30 AM",
                                color=self.TEXT_SECONDARY),
                        ft.TextButton("Actualizar datos")
                    ]
                )
            ]
        )

        self.cargar_cards()

    # ================= FILTROS =================
    def build_filtros(self):

        self.dropdown = ft.Dropdown(
            width=200,
            value=self.tipo_actual,
            border_color=self.BORDER,
            bgcolor=self.CARD,
            color=self.TEXT,
            options=[
                ft.dropdown.Option("Alumnos"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitantes"),
            ],
        )

        return ft.Container(
            padding=15,
            border_radius=15,
            bgcolor=self.CARD,
            border=ft.border.all(1, self.BORDER),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Row(
                        spacing=15,
                        controls=[
                            self.input_fecha("01/05/2025"),
                            self.input_fecha("31/05/2025"),
                            self.dropdown
                        ]
                    ),

                    ft.ElevatedButton(
                        "Exportar reporte",
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor=self.AZUL,
                        color="white"
                    )
                ]
            )
        )

    def input_fecha(self, text):
        return ft.Container(
            padding=10,
            border_radius=10,
            bgcolor="surfaceVariant",
            border=ft.border.all(1, self.BORDER),
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=self.TEXT),
                ft.Text(text, color=self.TEXT)
            ])
        )

    # ================= CARDS =================
    def cargar_cards(self):

        data = [
            ("Alumnos", "120", self.AZUL),
            ("Personal", "40", self.PURPURA),
            ("Visitantes", "25", self.VERDE),
        ]

        self.cards_row.controls = [
            self.card(t, v, c) for t, v, c in data
        ]

    def card(self, title, value, color):
        return ft.Container(
            expand=True,
            padding=20,
            border_radius=15,
            bgcolor=self.CARD,
            border=ft.border.all(1, self.BORDER),
            content=ft.Column([
                ft.Text(title, color=self.TEXT_SECONDARY),
                ft.Text(value, size=28, weight="bold", color=color),
            ])
        )

    # ================= GRAFICA BARRAS (ESTILO DASHBOARD) =================
    def build_bar_chart(self):

        labels = ["Alumnos", "Personal", "Visitantes"]
        values = [120, 40, 25]
        colors = [self.AZUL, self.PURPURA, self.VERDE]
        max_val = max(values)

        bars = []

        for i in range(len(labels)):
            bars.append(
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(str(values[i]), size=12, color=self.TEXT_SECONDARY),
                        ft.Container(
                            width=35,
                            height=80 + int((values[i] / max_val) * 160),
                            bgcolor=colors[i],
                            border_radius=6
                        ),
                        ft.Text(labels[i], size=12, color=self.TEXT_SECONDARY)
                    ]
                )
            )

        return ft.Container(
            expand=True,
            padding=20,
            border_radius=15,
            bgcolor=self.CARD,
            border=ft.border.all(1, self.BORDER),
            content=ft.Column([
                ft.Text("Reporte: Tipo Usuario",
                        weight="bold", color=self.TEXT),

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=bars
                )
            ])
        )

    # ================= DISTRIBUCIÓN (SIN DONA) =================
    def build_distribution_panel(self):

        data = [
            ("Alumnos", 120, self.AZUL),
            ("Personal", 40, self.PURPURA),
            ("Visitantes", 25, self.VERDE),
        ]

        items = []

        for name, value, color in data:
            percent = round((value / self.total_usuarios) * 100, 1)

            items.append(
                ft.Column([
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, color=color, size=18),
                                ft.Text(name, color=self.TEXT)
                            ]),
                            ft.Text(f"{value} ({percent}%)",
                                    color=self.TEXT_SECONDARY)
                        ]
                    ),
                    ft.Container(
                        height=6,
                        border_radius=10,
                        bgcolor="surfaceVariant",
                        content=ft.Container(
                            width=percent * 2,
                            bgcolor=color,
                            border_radius=10
                        )
                    ),
                    ft.Container(height=10)
                ])
            )

        return ft.Container(
            width=320,
            padding=20,
            border_radius=15,
            bgcolor=self.CARD,
            border=ft.border.all(1, self.BORDER),
            content=ft.Column([
                ft.Text("Distribución: Tipo Usuario",
                        weight="bold", color=self.TEXT),

                ft.Container(height=10),

                *items,

                ft.Container(height=10),

                ft.Container(
                    padding=10,
                    border_radius=12,
                    bgcolor="surfaceVariant",
                    content=ft.Column([
                        ft.Text("Total usuarios",
                                color=self.TEXT_SECONDARY, size=12),
                        ft.Text(str(self.total_usuarios),
                                size=20, weight="bold", color=self.TEXT)
                    ])
                )
            ])
        )
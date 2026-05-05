import flet as ft


class PantallaReportes(ft.Container):

    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page

        self.AZUL = "#2563EB"
        self.GRIS = "#6B7280"
        self.FONDO = "#F3F4F6"

        self.expand = True
        self.bgcolor = self.FONDO
        self.padding = 20

        self.tipo_actual = "Tipo Usuario"

        self.fecha_inicio_picker = ft.DatePicker()
        self.fecha_fin_picker = ft.DatePicker()

        self.build_ui()

    def did_mount(self):
        self._page.overlay.append(self.fecha_inicio_picker)
        self._page.overlay.append(self.fecha_fin_picker)
        self._page.update()

    # ================= UI =================
    def build_ui(self):

        self.cards_row = ft.Row(spacing=20)

        self.content = ft.Column(
            spacing=20,
            controls=[

                # ===== HEADER =====
                ft.Column([
                    ft.Text("Reportes", size=28, weight="bold"),
                    ft.Text("Estadísticas del sistema de asistencia", color=self.GRIS),
                ]),

                # ===== FILTROS =====
                self.build_filtros(),

                # ===== CARDS =====
                self.cards_row,

                # ===== GRAFICAS =====
                ft.Row(
                    spacing=20,
                    controls=[
                        self.build_bar_chart(),
                        self.build_donut_chart()
                    ]
                ),

                # FOOTER
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Última actualización: 31/05/2025 10:30 AM", color=self.GRIS),
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
            options=[
                ft.dropdown.Option("Alumnos"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitantes"),
            ],
        )
        self.dropdown.on_change = self.cambiar_reporte

        return ft.Container(
            padding=15,
            border_radius=15,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Row(
                        spacing=15,
                        controls=[
                            self.input_fecha("01/05/2025", self.fecha_inicio_picker),
                            self.input_fecha("31/05/2025", self.fecha_fin_picker),
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

    def input_fecha(self, text, picker):
        return ft.Container(
            padding=10,
            border_radius=10,
            bgcolor="#F9FAFB",
            on_click=lambda e: self.abrir_picker(picker),
            content=ft.Row([
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=18),
                ft.Text(text)
            ])
        )

    def abrir_picker(self, picker):
        picker.open = True
        self._page.update()

    # ================= CARDS =================
    def cargar_cards(self):

        data = [
            ("Alumnos", "120", "#2563EB"),
            ("Personal", "40", "#7C3AED"),
            ("Visitantes", "25", "#059669"),
        ]

        self.cards_row.controls = [
            self.card(*d) for d in data
        ]

    def card(self, title, value, color):
        return ft.Container(
            expand=True,
            padding=20,
            border_radius=15,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Column([
                        ft.Text(title, color=self.GRIS),
                        ft.Text(value, size=28, weight="bold", color=color),
                        ft.Text("+12% vs mes anterior", size=12, color="#16A34A")
                    ]),

                    ft.Icon(ft.Icons.SHOW_CHART, color=color)
                ]
            )
        )

    # ================= GRAFICA BARRAS (FAKE) =================
    def build_bar_chart(self):
        return ft.Container(
            expand=True,
            padding=20,
            border_radius=15,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
            content=ft.Column(
                controls=[
                    ft.Text("Reporte: Tipo Usuario", weight="bold"),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            self.bar(120, "Alumnos", "#2563EB"),
                            self.bar(40, "Personal", "#7C3AED"),
                            self.bar(25, "Visitantes", "#059669"),
                        ]
                    )
                ]
            )
        )

    def bar(self, value, label, color):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=30,
                    height=value,
                    bgcolor=color,
                    border_radius=5
                ),
                ft.Text(label, size=12)
            ]
        )

    # ================= DONUT FAKE =================
    def build_donut_chart(self):
        return ft.Container(
            expand=True,
            padding=20,
            border_radius=15,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=10, color="#00000010"),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Distribución: Tipo Usuario", weight="bold"),

                    ft.Container(
                        width=150,
                        height=150,
                        border_radius=75,
                        bgcolor="#E5E7EB",
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("185\nTotal", text_align="center")
                    ),

                    ft.Column([
                        ft.Text("Alumnos 120 (64%)"),
                        ft.Text("Personal 40 (21%)"),
                        ft.Text("Visitantes 25 (13%)"),
                    ])
                ]
            )
        )

    # ================= EVENTOS =================
    def cambiar_reporte(self, e):
        self.tipo_actual = e.control.value
        self._page.update()
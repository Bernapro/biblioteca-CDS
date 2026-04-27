import flet as ft


class PantallaReportes(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        # ===== ESTADO =====
        self.tipo_actual = "Tipo Usuario"

        # ===== COLORES =====
        self.AZUL = "#3B82F6"
        self.AZUL_FUERTE = "#2563EB"
        self.AZUL_CLARO = "#60A5FA"
        self.FONDO = "#EAF1F7"
        self.BORDE = "#E5E7EB"
        self.TEXTO = "#111827"

        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== FECHAS =====
        self.txt_fecha_inicio = ft.Text("Fecha inicio", color=self.TEXTO)
        self.txt_fecha_fin = ft.Text("Fecha fin", color=self.TEXTO)

        self.fecha_inicio_picker = ft.DatePicker(on_change=self.seleccionar_inicio)
        self.fecha_fin_picker = ft.DatePicker(on_change=self.seleccionar_fin)

        # 🔥 NO AQUÍ (error)
        # self._page.overlay.extend(...)

        # ===== CONTENEDORES DINÁMICOS =====
        self.row_cards = ft.Row(spacing=20)
        self.chart_container = ft.Container(expand=2)
        self.donut_container = ft.Container(expand=1)

        self.build_ui()

    # 🔥 FIX
    def did_mount(self):
        self._page.overlay.extend([
            self.fecha_inicio_picker,
            self.fecha_fin_picker
        ])
        self.actualizar_reporte()

    # =========================
    # FECHAS
    # =========================
    def seleccionar_inicio(self, e):
        if e.control.value:
            self.txt_fecha_inicio.value = e.control.value.strftime("%Y-%m-%d")
            self.update()

    def seleccionar_fin(self, e):
        if e.control.value:
            self.txt_fecha_fin.value = e.control.value.strftime("%Y-%m-%d")
            self.update()

    def abrir_picker(self, picker):
        picker.open = True
        self._page.update()

    def campo_fecha(self, texto_ref, picker):
        return ft.Container(
            width=170,
            height=45,
            border=ft.border.all(1, self.BORDE),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12),
            bgcolor="white",
            on_click=lambda e: self.abrir_picker(picker),
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=self.AZUL),
                    texto_ref
                ],
                spacing=10
            )
        )

    # =========================
    # DROPDOWN
    # =========================
    def combo_reporte(self):
        self.dropdown = ft.Dropdown(
            width=220,
            label="Tipo de reporte",
            options=[
                ft.dropdown.Option("Tipo Usuario"),
                ft.dropdown.Option("Carrera"),
                ft.dropdown.Option("Facultad"),
                ft.dropdown.Option("Semestre"),
                ft.dropdown.Option("Incidencias"),
            ],
            on_select=self.cambiar_reporte,

            # 🔥 ESTILO NEGRO
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
        )
        return self.dropdown

    # =========================
    # CAMBIO
    # =========================
    def cambiar_reporte(self, e):
        self.tipo_actual = self.dropdown.value
        self.actualizar_reporte()

    # =========================
    # 🔥 LÓGICA REAL
    # =========================
    def actualizar_reporte(self):

        # ===== TARJETAS =====
        if self.tipo_actual == "Tipo Usuario":
            self.row_cards.controls = [
                self.build_stat_card("Alumnos", 120, ft.Icons.SCHOOL),
                self.build_stat_card("Personal", 40, ft.Icons.BADGE),
                self.build_stat_card("Visitantes", 25, ft.Icons.PERSON),
            ]

        elif self.tipo_actual == "Carrera":
            self.row_cards.controls = [
                self.build_stat_card("Top Carrera", 80, ft.Icons.COMPUTER),
                self.build_stat_card("Promedio visitas", 50, ft.Icons.TRENDING_UP),
                self.build_stat_card("Total registros", 200, ft.Icons.GROUP),
            ]

        elif self.tipo_actual == "Facultad":
            self.row_cards.controls = [
                self.build_stat_card("Facultad mayor uso", 120, ft.Icons.APARTMENT),
                self.build_stat_card("Promedio", 70, ft.Icons.BAR_CHART),
                self.build_stat_card("Total", 300, ft.Icons.GROUP),
            ]

        elif self.tipo_actual == "Semestre":
            self.row_cards.controls = [
                self.build_stat_card("Más activo", 90, ft.Icons.SCHOOL),
                self.build_stat_card("Promedio", 60, ft.Icons.TRENDING_UP),
                self.build_stat_card("Total", 210, ft.Icons.GROUP),
            ]

        elif self.tipo_actual == "Incidencias":
            self.row_cards.controls = [
                self.build_stat_card("Pendientes", 10, ft.Icons.WARNING),
                self.build_stat_card("Resueltas", 5, ft.Icons.CHECK),
                self.build_stat_card("Totales", 15, ft.Icons.REPORT),
            ]

        # ===== GRÁFICA =====
        self.chart_container.content = self.build_chart(self.tipo_actual)

        # ===== DONUT =====
        self.donut_container.content = self.build_donut(self.tipo_actual)

        self.update()

    # =========================
    # TARJETAS
    # =========================
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

    # =========================
    # GRÁFICA DINÁMICA
    # =========================
    def build_chart(self, titulo):
        return ft.Container(
            height=300,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text(f"Reporte: {titulo}", size=14, color="black"),

                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 1),
                        content=ft.Row(
                            [
                                ft.Container(width=35, height=120, bgcolor=self.AZUL, border_radius=6),
                                ft.Container(width=35, height=160, bgcolor=self.AZUL_FUERTE, border_radius=6),
                                ft.Container(width=35, height=100, bgcolor=self.AZUL_CLARO, border_radius=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        )
                    )
                ]
            )
        )

    # =========================
    # DONUT DINÁMICO
    # =========================
    def build_donut(self, titulo):
        return ft.Container(
            height=260,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text(f"Distribución: {titulo}", size=14, color="black"),

                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.ProgressRing(
                            value=0.6,
                            stroke_width=25,   
                            width=140,       
                            height=140,        
                            color=self.AZUL
                        )
                    )
                ]
            )
        )

    # =========================
    # FILTROS
    # =========================
    def build_filtros(self):
        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.campo_fecha(self.txt_fecha_inicio, self.fecha_inicio_picker),
                    self.campo_fecha(self.txt_fecha_fin, self.fecha_fin_picker),
                    self.combo_reporte(),

                    ft.ElevatedButton(
                        "Exportar reporte",
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

    # =========================
    # UI
    # =========================
    def build_ui(self):
        self.content = ft.Column(
            [
                ft.Text("Reportes", size=32, weight="bold", color="black"),
                ft.Text("Estadísticas del sistema de asistencia", color="black"),

                self.build_filtros(),

                self.row_cards,

                ft.Row(
                    [
                        self.chart_container,
                        self.donut_container
                    ],
                    expand=True
                )
            ],
            spacing=20
        )
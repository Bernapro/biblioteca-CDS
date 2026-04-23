import flet as ft

def dashboard_view(page):
    # ===== COLORES =====
    BG = "#EEF3F8"
    CARD = "white"
    TEXT_SECONDARY = "#6B7280"
    PRIMARY = "#3B82F6"
    TEXT_MAIN = "#111827"  # ✅ NUEVO (negro)

    # ===== CARD =====
    def card(title, value):
        return ft.Container(
            width=float("inf"),
            height=120,
            padding=20,
            bgcolor=CARD,
            border_radius=18,
            shadow=ft.BoxShadow(blur_radius=10, color="black12"),
            content=ft.Column(
                [
                    ft.Text(title, size=14, color=TEXT_SECONDARY, weight="w500"),
                    ft.Text(str(value), size=32, weight="bold", color=TEXT_MAIN),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=5
            )
        )

    # ===== DONUT =====
    def donut_chart():
        return ft.Container(
            width=float("inf"),
            height=280,
            bgcolor=CARD,
            border_radius=18,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Uso del sistema", size=15, color=TEXT_SECONDARY, weight="bold"),
                    ft.Container(
                        expand=True,
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
                                    value=0.75,
                                    stroke_width=20,
                                    width=160,
                                    height=160,
                                    color=PRIMARY,
                                ),
                                ft.Column(
                                    [
                                        ft.Text("75%", size=26, weight="bold", color=TEXT_MAIN),
                                        ft.Text("ocupación", size=12, color=TEXT_SECONDARY),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0
                                )
                            ]
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    # ===== BAR CHART =====
    def bar_chart():
        return ft.Container(
            expand=True,
            width=float("inf"),
            bgcolor=CARD,
            border_radius=18,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Visitas totales", size=14, color=TEXT_MAIN),
                    ft.Text("Gráfica de la semana", size=18, weight="bold",color=TEXT_MAIN),
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 1),
                        content=ft.Row(
                            [
                                ft.Container(width=40, height=140, bgcolor="#3B82F6", border_radius=6),
                                ft.Container(width=40, height=200, bgcolor="#2563EB", border_radius=6),
                                ft.Container(width=40, height=110, bgcolor="#60A5FA", border_radius=6),
                                ft.Container(width=40, height=170, bgcolor="#1D4ED8", border_radius=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        )
                    )
                ]
            )
        )

    # ===== BOTÓN =====
    def boton():
        return ft.Container(
            height=55,
            width=float("inf"),
            alignment=ft.Alignment(0, 0),
            border_radius=15,
            gradient=ft.LinearGradient(colors=["#60A5FA", "#1D4ED8"]),
            content=ft.Text("Generar Reporte", size=16, color="white", weight="bold")
        )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=35,
        bgcolor=BG,
        content=ft.Column(
            [
                # HEADER
                ft.Row(
                    [
                        ft.Column(
                            [
                                # ✅ COLOR NEGRO
                                ft.Text("Panel de Control", size=36, weight="bold", color=TEXT_MAIN),
                                ft.Text("Bienvenido José, hora de hacer tarea", size=15, color=TEXT_MAIN),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, color=PRIMARY, size=22),

                                # ✅ BARRA MÁS LARGA
                                ft.Container(
                                    width=300, height=30,  # 🔥 MÁS GRANDE
                                    bgcolor="#D1D5DB",
                                    border_radius=20,
                                    padding=4,
                                    content=ft.Container(
                                        width=50,
                                        bgcolor=PRIMARY,
                                        border_radius=20,
                                        alignment=ft.Alignment(-1, 0)
                                    )
                                ),

                                ft.Icon(ft.Icons.NIGHTLIGHT_ROUND, size=22, color=TEXT_SECONDARY),
                            ],
                            spacing=15
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                # GRID
                ft.Row(
                    [
                        ft.Column(
                            [
                                card("Sesiones activas actualmente", 67),
                                donut_chart(),
                            ],
                            expand=3, spacing=25
                        ),

ft.Column(
    [
        card("Préstamos activos", 19),
        card("Préstamos vencidos", 28),
        card("Cubículos ocupados", 4),

        ft.Container(
            margin=ft.margin.only(top=10),
            content=boton()
        )
    ],
    expand=3,
    spacing=25,
    scroll=ft.ScrollMode.AUTO  # 🔥 CLAVE
),

                        ft.Column(
                            [
                                bar_chart()
                            ],
                            expand=4, spacing=25
                        ),
                    ],
                    expand=True,
                    spacing=30,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH
                )
            ],
            spacing=30
        )
    )
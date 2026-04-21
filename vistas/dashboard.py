import flet as ft

def dashboard_view(page):
    def card(title, value):
        return ft.Container(
            width=320,
            height=150,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text(title, size=15, color="black"),
                    ft.Text(str(value), size=36, weight="bold", color="black"),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def donut_chart():
        return ft.Container(
            width=320,
            height=280,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Uso del sistema", size=14, color="black"),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Stack(
                            alignment=ft.alignment.Alignment(0, 0),
                            controls=[
                                ft.ProgressRing(
                                    value=1,
                                    stroke_width=25,
                                    width=180,
                                    height=180,
                                    color="#E5E7EB",
                                ),
                                ft.ProgressRing(
                                    value=0.75,
                                    stroke_width=25,
                                    width=180,
                                    height=180,
                                    color="#2563EB",
                                ),
                                ft.Column(
                                    [
                                        ft.Text("75%", size=28, weight="bold", color="black"),
                                        ft.Text("ocupación", size=12, color="#6B7280"),
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

    def bar_chart():
        return ft.Container(
            width=320,
            height=340,
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Text("Visitas totales", size=14, color="black"),
                    ft.Text("Gráfica", weight="bold", color="black"),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.Alignment(0, 1),
                        content=ft.Row(
                            [
                                ft.Container(width=35, height=110, bgcolor="#3B82F6", border_radius=6),
                                ft.Container(width=35, height=170, bgcolor="#2563EB", border_radius=6),
                                ft.Container(width=35, height=90, bgcolor="#60A5FA", border_radius=6),
                                ft.Container(width=35, height=150, bgcolor="#1D4ED8", border_radius=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        )
                    )
                ]
            )
        )

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Panel de Control", size=36, weight="bold", color="black"),
                                ft.Text("Bienvenido José, hora de hacer tarea", color="black"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.WB_SUNNY, color="#3B82F6"),
                                ft.Container(
                                    width=140,
                                    height=28,
                                    border_radius=20,
                                    gradient=ft.LinearGradient(colors=["#60A5FA", "#1D4ED8"])
                                ),
                                ft.Icon(ft.Icons.NIGHTLIGHT, color="black"),
                            ],
                            spacing=12
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Row(
                    [
                        ft.Column([card("Sesiones activas", 67), donut_chart()], spacing=25),

                        ft.Column(
                            [
                                card("Préstamos activos", 19),
                                card("Préstamos vencidos", 28),
                                card("Cubículos ocupados", 4),
                            ],
                            spacing=20
                        ),

                        ft.Column([bar_chart()])
                    ],
                    expand=True
                )
            ]
        )
    )
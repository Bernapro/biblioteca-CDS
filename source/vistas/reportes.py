import flet as ft

def reportes_view(page):

    # ===== COLORES =====
    AZUL = "#3B82F6"
    AZUL_FUERTE = "#2563EB"
    AZUL_CLARO = "#60A5FA"
    FONDO = "#EAF1F7"

    # ===== TARJETAS =====
    def stat_card(title, value, icon):
        return ft.Container(
            width=260,
            height=110,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    ft.Icon(icon, size=30, color=AZUL),
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

    # ===== FILTROS (FIX REAL) =====
    def filtros():
        def combo(label):
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
                focused_border_color=AZUL
            )

        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    combo("Fecha inicio"),
                    combo("Fecha fin"),
                    combo("Todos"),
                    combo("Usuario"),

                    ft.ElevatedButton(
                        "Generar reporte",
                        style=ft.ButtonStyle(
                            bgcolor=AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

    # ===== GRÁFICA =====
    def visitas_chart():
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
                        alignment=ft.alignment.Alignment(0, 1),
                        content=ft.Row(
                            [
                                ft.Container(width=35, height=110, bgcolor=AZUL, border_radius=6),
                                ft.Container(width=35, height=170, bgcolor=AZUL_FUERTE, border_radius=6),
                                ft.Container(width=35, height=90, bgcolor=AZUL_CLARO, border_radius=6),
                                ft.Container(width=35, height=150, bgcolor=AZUL_FUERTE, border_radius=6),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        )
                    )
                ]
            )
        )

    # ===== DONUT =====
    def donut_chart():
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
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Stack(
                            alignment=ft.alignment.Alignment(0, 0),
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
                                    color=AZUL,
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
    def item(nombre, cantidad):
        return ft.Row(
            [
                ft.Icon(ft.Icons.MENU_BOOK, size=18, color=AZUL),
                ft.Text(nombre, color="black"),
                ft.Text(f"{cantidad} préstamos", color="black")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def top_books():
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
                    item("Libro 1", 28),
                    item("Libro 2", 32),
                    item("Libro 3", 12),
                ]
            )
        )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        border_radius=30,  
        content=ft.Column(
            [
                ft.Text("Reportes", size=32, weight="bold", color="black"),
                ft.Text("Estadísticas generales del sistema", color="black"),

                filtros(),

                ft.Row(
                    [
                        stat_card("Asistencias", 532, ft.Icons.PERSON),
                        stat_card("Préstamos", 292, ft.Icons.SWAP_HORIZ),
                        stat_card("Vencidos", 93, ft.Icons.WARNING),
                    ],
                    spacing=20
                ),

                ft.Row(
                    [
                        ft.Container(expand=2, content=visitas_chart()),
                        ft.Container(
                            expand=1,
                            content=ft.Column(
                                [
                                    donut_chart(),
                                    top_books()
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
    )
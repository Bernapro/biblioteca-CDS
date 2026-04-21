import flet as ft

def prestamos_view(page):

    # ===== COLORES =====
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    FONDO = "#EAF1F7"

    # ===== FILTROS =====
    filtros = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Row(
            [
                ft.TextField(
                    width=350,
                    hint_text="Buscar por matrícula, nombre o libro...",
                    prefix_icon=ft.Icons.SEARCH,
                    color="black",
                    text_style=ft.TextStyle(color="black"),
                ),

                ft.Dropdown(
                    width=180,
                    label="Estado",
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("A tiempo"),
                        ft.dropdown.Option("Atrasado"),
                    ],
                    color="black",
                    text_style=ft.TextStyle(color="black"),
                    label_style=ft.TextStyle(color="black"),
                    focused_border_color=AZUL
                ),

                ft.ElevatedButton(
                    "Buscar",
                    style=ft.ButtonStyle(
                        bgcolor=AZUL,
                        color="white"
                    )
                )
            ],
            spacing=15
        )
    )

    # ===== BOTONES =====
    def btn_extender():
        return ft.ElevatedButton(
            "Extender",
            height=35,
            style=ft.ButtonStyle(
                bgcolor=AZUL,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    def btn_devolver():
        return ft.ElevatedButton(
            "Devolver",
            height=35,
            style=ft.ButtonStyle(
                bgcolor=VERDE,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    # ===== TABLA REAL =====
    tabla = ft.DataTable(
        expand=True,
        column_spacing=40,
        heading_row_color="#F1F5F9",

        columns=[
            ft.DataColumn(ft.Text("Matrícula", color="black", weight="bold")),
            ft.DataColumn(ft.Text("Nombre", color="black", weight="bold")),
            ft.DataColumn(ft.Text("Libro", color="black", weight="bold")),
            ft.DataColumn(ft.Text("Estado", color="black", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", color="black", weight="bold")),
        ],

        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("100025787", color="black")),
                ft.DataCell(ft.Text("Carlos Daniel", color="black")),
                ft.DataCell(ft.Text("El principito", color="black")),
                ft.DataCell(ft.Text("A tiempo", color="black")),
                ft.DataCell(ft.Row([btn_extender(), btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("100025788", color="black")),
                ft.DataCell(ft.Text("Cruz Castillo", color="black")),
                ft.DataCell(ft.Text("1984", color="black")),
                ft.DataCell(ft.Text("Atrasado", color="black")),
                ft.DataCell(ft.Row([btn_extender(), btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ABCDEFGA", color="black")),
                ft.DataCell(ft.Text("Jose Angel", color="black")),
                ft.DataCell(ft.Text("Clean Code", color="black")),
                ft.DataCell(ft.Text("A tiempo", color="black")),
                ft.DataCell(ft.Row([btn_extender(), btn_devolver()], spacing=10)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ABCDEFGA", color="black")),
                ft.DataCell(ft.Text("Figueroa Sales", color="black")),
                ft.DataCell(ft.Text("Python Básico", color="black")),
                ft.DataCell(ft.Text("Atrasado", color="black")),
                ft.DataCell(ft.Row([btn_extender(), btn_devolver()], spacing=10)),
            ]),
        ]
    )

    # ===== CONTENEDOR CON SCROLL =====
    tabla_scroll = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Column(
            [tabla],
            scroll=ft.ScrollMode.AUTO  # 🔥 scroll SOLO en filas
        )
    )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        content=ft.Column(
            [
                ft.Text("Préstamos de libros", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona el catalogo de libros registrados en el sistema",
                    color="black"
                ),

                filtros,

                tabla_scroll
            ],
            spacing=20,
            expand=True
        )
    )
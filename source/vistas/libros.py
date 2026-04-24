import flet as ft

def libros_view(page):

    AZUL = "#3B82F6"
    FONDO = "#EAF1F7"

    # ===== CARD LIBRO =====
    def card_libro(titulo, autor, estado):
        return ft.Container(
            width=200,
            height=220,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MENU_BOOK, size=60, color=AZUL),

                    ft.Text(titulo, weight="bold", size=14, color="black"),
                    ft.Text(autor, size=12, color="black"),

                    ft.Container(
                        padding=5,
                        border_radius=10,
                        bgcolor="#DCFCE7" if estado == "Disponible" else "#FEE2E2",
                        content=ft.Text(
                            estado,
                            size=11,
                            color="green" if estado == "Disponible" else "red"
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            )
        )

    # ===== FILTROS =====
    filtros = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Row(
            [
                ft.TextField(
                    width=250,
                    hint_text="Buscar por título o autor...",
                    prefix_icon=ft.Icons.SEARCH,
                    color="black",               
                    cursor_color="black",          
                    hint_style=ft.TextStyle(color="#6B7280")  
                ),
                ft.Dropdown(
                    width=180,
                    label="Disponibilidad",
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Disponible"),
                        ft.dropdown.Option("Prestado"),
                    ]
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

    # ===== GRID DE LIBROS =====
    grid_libros = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=220,
        spacing=20,
        run_spacing=20,
        controls=[
            card_libro("El principito", "Antoine", "Disponible"),
            card_libro("1984", "Orwell", "Prestado"),
            card_libro("Cien años", "García Márquez", "Disponible"),
            card_libro("Don Quijote", "Cervantes", "Disponible"),
            card_libro("It", "Stephen King", "Prestado"),
            card_libro("Hábitos Atómicos", "James Clear", "Disponible"),
            card_libro("Clean Code", "Robert C.", "Disponible"),
            card_libro("Python Básico", "Autor X", "Prestado"),
        ]
    )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        border_radius=30,  
        content=ft.Column(
            [
                ft.Text("Catálogo de libros", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona el catalogo de libros registrados en el sistema",
                    color="black"
                ),

                filtros,

                grid_libros
            ],
            spacing=20,
            expand=True
        )
    )
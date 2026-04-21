import flet as ft

def incidencias_view(page):

    # ===== COLORES =====
    AZUL = "#3B82F6"
    VERDE = "#22C55E"
    ROJO = "#EF4444"
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
                    width=300,
                    hint_text="Buscar por identificador o nombre...",
                    prefix_icon=ft.Icons.SEARCH,
                    color="black",
                    text_style=ft.TextStyle(color="black"),
                ),

                ft.Dropdown(
                    width=180,
                    label="Estado",
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("Pendiente"),
                        ft.dropdown.Option("Resuelto"),
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
    def btn_resuelto():
        return ft.ElevatedButton(
            "Resuelto",
            style=ft.ButtonStyle(
                bgcolor=VERDE,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    def btn_pendiente():
        return ft.ElevatedButton(
            "Pendiente",
            style=ft.ButtonStyle(
                bgcolor=ROJO,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    def btn_detalles():
        return ft.OutlinedButton(
            "Ver detalles",
            style=ft.ButtonStyle(
                color=AZUL,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    # ===== CARD INCIDENCIA =====
    def card(nombre, matricula, razon, lugar, fecha, estado="Pendiente"):
        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    # IZQUIERDA (INFO)
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON, size=40, color=AZUL),

                            ft.Column(
                                [
                                    ft.Text(nombre, weight="bold", size=16, color="black"),
                                    ft.Text(f"Matrícula: {matricula}", size=12, color="black"),

                                    ft.Container(height=5),

                                    ft.Text(razon, size=13, color="black"),
                                    ft.Text(f"Lugar: {lugar}", size=12, color="black"),
                                    ft.Text(f"Fecha: {fecha}", size=12, color="black"),
                                ],
                                spacing=2
                            )
                        ],
                        spacing=15
                    ),

                    # DERECHA (BOTONES)
                    ft.Row(
                        [
                            btn_resuelto() if estado == "Pendiente" else btn_pendiente(),
                            btn_detalles()
                        ],
                        spacing=10
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    # ===== LISTA =====
    lista = ft.Column(
        [
            card("Carlos Daniel", "100025787", "Ruido excesivo", "Cubículo 1", "24/Marzo/2026", "Pendiente"),
            card("Cruz Castillo", "100025788", "Uso indebido del equipo", "Cubículo 2", "25/Marzo/2026", "Resuelto"),
            card("Jose Angel", "ABCDEFGA", "Comportamiento inapropiado", "Cubículo 3", "26/Marzo/2026", "Pendiente"),
            card("Figueroa Sales", "ABCDEFGA", "Ruido excesivo", "Cubículo 1", "27/Marzo/2026", "Resuelto"),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # ===== PAGINACIÓN =====
    paginacion = ft.Row(
        [
            ft.Text("1-10 de 100 incidencias", color="black"),

            ft.Row(
                [
                    ft.OutlinedButton("Anterior"),
                    ft.OutlinedButton("Siguiente"),
                ],
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        content=ft.Column(
            [
                ft.Text("Incidencias", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona el catalogo de incidencias registrados en el sistema",
                    color="black"
                ),

                filtros,

                lista,

                paginacion
            ],
            spacing=20,
            expand=True
        )
    )
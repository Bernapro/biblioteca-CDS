import flet as ft

# IMPORTAR VISTAS
from vistas.dashboard import dashboard_view
from vistas.asistencia import asistencia_view
from vistas.historial import historial_view
from vistas.reportes import reportes_view
from vistas.libros import libros_view
from vistas.prestamos import prestamos_view
from vistas.incidencias import incidencias_view


def main(page: ft.Page):
    page.title = "Sistema Biblioteca UNACH"
    page.bgcolor = "#EAF1F7"

    # Tamaño ventana
    page.window_width = 1400
    page.window_height = 900
    page.window_min_width = 1200
    page.window_min_height = 800

    # CONTENEDOR PRINCIPAL
    content_area = ft.Container(expand=True)

    # LAYOUT GLOBAL (para actualizar sidebar)
    layout = ft.Row(expand=True)

    # ===== CAMBIO DE VISTA =====
    def cambiar_vista(vista):
        content_area.content = vista(page)
        page.update()

    # ===== ESTADO DEL MENU =====
    selected = {"index": 0}

    # ===== SELECCIONAR =====
    def seleccionar(index):
        selected["index"] = index

        if index == 0:
            cambiar_vista(dashboard_view)
        elif index == 1:
            cambiar_vista(asistencia_view)
        elif index == 2:
            cambiar_vista(historial_view)
        elif index == 3:
            cambiar_vista(reportes_view)
        elif index == 4:
            cambiar_vista(libros_view)
        elif index == 5:
            cambiar_vista(prestamos_view)
        elif index == 6:
            cambiar_vista(incidencias_view)

        # 🔥 reconstruir sidebar
        layout.controls[0] = build_sidebar()
        page.update()

    # ===== ITEM DEL MENU =====
    def menu_item(icon, texto, index):
        activo = selected["index"] == index

        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=5,
                        height=40,
                        bgcolor="#3B82F6" if activo else "transparent",
                        border_radius=5
                    ),

                    ft.Icon(
                        icon,
                        size=22,
                        color="#3B82F6" if activo else "#6B7280"
                    ),

                    ft.Text(
                        texto,
                        size=15,
                        weight="bold" if activo else "normal",
                        color="#111827" if activo else "#374151"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12
            ),
            padding=12,
            border_radius=12,
            bgcolor="#EFF6FF" if activo else "transparent",
            on_click=lambda e: seleccionar(index)
        )

    # ===== SIDEBAR =====
    def build_sidebar():
        return ft.Container(
            width=250,
            margin=ft.margin.only(left=10, top=10, bottom=10),
            padding=20,
            border_radius=20,
            bgcolor="white",
            shadow=ft.BoxShadow(blur_radius=20, color="black12"),
            content=ft.Column(
                [
                    ft.Text("UNACH", size=22, weight="bold", color="#111827"),

                    ft.Divider(height=20, color="transparent"),

                    menu_item(ft.Icons.HOME, "Principal", 0),
                    menu_item(ft.Icons.QR_CODE, "Asistencia", 1),
                    menu_item(ft.Icons.HISTORY, "Historial", 2),
                    menu_item(ft.Icons.BAR_CHART, "Reportes", 3),
                    menu_item(ft.Icons.MENU_BOOK, "Libros", 4),
                    menu_item(ft.Icons.SWAP_HORIZ, "Préstamos", 5),
                    menu_item(ft.Icons.WARNING, "Incidencias", 6),
                ],
                spacing=10
            )
        )

    # ===== VISTA INICIAL =====
    cambiar_vista(dashboard_view)

    # ===== ARMAR LAYOUT =====
    layout.controls = [
        build_sidebar(),
        content_area
    ]

    # ===== FONDO DEGRADADO =====
    page.add(
    ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            colors=["#cfe8ff", "#9ec9ff"],
            begin=ft.alignment.Alignment(-1, -1),
            end=ft.alignment.Alignment(1, 1)
        ),
        content=ft.Container(
            expand=True,
            margin=20,
            padding=20,
            border_radius=30,
            bgcolor="#F8FAFC",  # 🔥 blanco semi transparente
            shadow=ft.BoxShadow(
                blur_radius=30,
                color="black26",
                offset=ft.Offset(0, 10)
            ),
            content=layout
        )
    )
)

ft.run(main)
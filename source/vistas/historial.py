import flet as ft
import json
from datetime import datetime
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "datos" / "datos.json"

def historial_view(page):

    # ===== COLORES =====
    AZUL = "#3B82F6"
    FONDO = "#EAF1F7"

    # ===== CARGAR DATOS =====
    def cargar_datos():
        with DATA_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    data = cargar_datos()

    # ===== VALIDAR FECHA =====
    def fecha_valida(fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except:
            return False

    # ===== INPUTS =====
    input_busqueda = ft.TextField(
        hint_text="Buscar por identificador o nombre...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        color="black",
        text_style=ft.TextStyle(color="black"),
    )

    input_fecha_inicio = ft.TextField(
        hint_text="Fecha inicio (YYYY-MM-DD)",
        width=200,
        color="black",
        text_style=ft.TextStyle(color="black"),
    )

    input_fecha_fin = ft.TextField(
        hint_text="Fecha fin (YYYY-MM-DD)",
        width=200,
        color="black",
        text_style=ft.TextStyle(color="black"),
    )

    tabla_container = ft.Column(scroll="auto", expand=True)

    # ===== FILTROS =====
    filtros = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Row(
            [
                input_busqueda,
                input_fecha_inicio,
                input_fecha_fin,
                ft.ElevatedButton(
                    "Buscar",
                    on_click=lambda e: filtrar(),
                    style=ft.ButtonStyle(
                        bgcolor=AZUL,
                        color="white"
                    )
                )
            ],
            spacing=15
        )
    )

    # ===== FILTRAR Y MOSTRAR RESULTADOS =====
    def filtrar(e=None):
        texto = input_busqueda.value.strip().lower() if input_busqueda.value else ""
        f_inicio = input_fecha_inicio.value.strip()
        f_fin = input_fecha_fin.value.strip()

        # VALIDAR FECHAS
        if f_inicio and not fecha_valida(f_inicio):
            return

        if f_fin and not fecha_valida(f_fin):
            return

        registros_filtrados = []

        for r in data["registros"]:
            if texto:
                if texto not in r["identificador"].lower() and texto not in r["nombre"].lower():
                    continue

            if f_inicio and r["fecha"] < f_inicio:
                continue

            if f_fin and r["fecha"] > f_fin:
                continue

            registros_filtrados.append(r)

        # CREAR FILAS PARA LA TABLA
        filas = []

        for r in registros_filtrados:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(r["identificador"], color="black")),
                        ft.DataCell(ft.Text(r["nombre"], color="black")),
                        ft.DataCell(ft.Text(r["fecha"], color="black")),
                        ft.DataCell(ft.Text(r["hora_entrada"], color="black")),
                        ft.DataCell(ft.Text(r["hora_salida"] or "-", color="black")),
                    ]
                )
            )

        # CREAR TABLA CON LOS RESULTADOS
        tabla = ft.DataTable(
            expand=True,
            columns=[
                ft.DataColumn(ft.Text("Identificador", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Nombre completo", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Fecha", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Hora entrada", color="black", weight="bold")),
                ft.DataColumn(ft.Text("Hora salida", color="black", weight="bold")),
            ],
            rows=filas,
            column_spacing=40,
            heading_row_height=50,
            data_row_min_height=50,
            heading_row_color="#F1F5F9",
        )

        tabla_container.controls.clear()
        tabla_container.controls.append(tabla)

        page.update()

    # FILTRAR AL INICIAR
    filtrar()

    # FILTRAR AL CAMBIAR TEXTO
    input_busqueda.on_change = filtrar

    # ===== TABLA SCROLL =====
    tabla_scroll = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Column(
            [tabla_container],
            scroll=ft.ScrollMode.AUTO
        )
    )

    # ===== MAIN =====
    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        content=ft.Column(
            [
                ft.Text("Historial de visitas", size=32, weight="bold", color="black"),
                ft.Text(
                    "Sistema de control digital - Registro de asistencias",
                    color="black"
                ),

                filtros,

                tabla_scroll
            ],
            spacing=20,
            expand=True
        )
    )
import flet as ft
import json
from datetime import datetime
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "datos" / "datos.json"

def historial_view(page: ft.Page):

    AZUL = "#3B82F6"
    FONDO = "#EAF1F7"
    TEXTO = "#111827"
    BORDE = "#E5E7EB"

    def cargar_datos():
        try:
            with DATA_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"registros": []}

    data = cargar_datos()

    def fecha_valida(fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except:
            return False

    # ===== TEXTOS DINÁMICOS =====
    txt_fecha_inicio = ft.Text("Fecha inicio", color="#6B7280")
    txt_fecha_fin = ft.Text("Fecha fin", color="#6B7280")

    # ===== DATE PICKERS =====
    def seleccionar_inicio(e):
        if e.control.value:
            txt_fecha_inicio.value = e.control.value.strftime("%Y-%m-%d")
            filtrar()
            page.update()

    def seleccionar_fin(e):
        if e.control.value:
            txt_fecha_fin.value = e.control.value.strftime("%Y-%m-%d")
            filtrar()
            page.update()

    fecha_inicio_picker = ft.DatePicker(on_change=seleccionar_inicio)
    fecha_fin_picker = ft.DatePicker(on_change=seleccionar_fin)

    page.overlay.extend([fecha_inicio_picker, fecha_fin_picker])

    # ===== FUNCIÓN PARA ABRIR PICKER =====
    def abrir_picker(picker):
        picker.open = True
        page.update()

    # ===== BOTONES DE FECHA =====
    def boton_fecha(texto_ref, picker):
        return ft.Container(
            width=170,
            height=45,
            border=ft.border.all(1, BORDE),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12),
            bgcolor="white",
            on_click=lambda e: abrir_picker(picker),
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=AZUL),
                    texto_ref
                ],
                spacing=10
            )
        )

    fecha_inicio_btn = boton_fecha(txt_fecha_inicio, fecha_inicio_picker)
    fecha_fin_btn = boton_fecha(txt_fecha_fin, fecha_fin_picker)

    # ===== BUSCADOR =====
    input_busqueda = ft.TextField(
        hint_text="Buscar por identificador o nombre...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        border_radius=12,
        on_change=lambda e: filtrar()
    )

    tabla_container = ft.Column(scroll="auto", expand=True)

    # ===== FILTRAR =====
    def filtrar(e=None):
        texto = input_busqueda.value.strip().lower() if input_busqueda.value else ""

        f_inicio = txt_fecha_inicio.value if txt_fecha_inicio.value != "Fecha inicio" else ""
        f_fin = txt_fecha_fin.value if txt_fecha_fin.value != "Fecha fin" else ""

        if f_inicio and not fecha_valida(f_inicio):
            return
        if f_fin and not fecha_valida(f_fin):
            return

        registros_filtrados = []

        for r in data.get("registros", []):
            if texto and (texto not in r["identificador"].lower() and texto not in r["nombre"].lower()):
                continue

            if f_inicio and r["fecha"] < f_inicio:
                continue

            if f_fin and r["fecha"] > f_fin:
                continue

            registros_filtrados.append(r)

        filas = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(r["identificador"], color=TEXTO)),
                    ft.DataCell(ft.Text(r["nombre"], color=TEXTO)),
                    ft.DataCell(ft.Text(r["fecha"], color=TEXTO)),
                    ft.DataCell(ft.Text(r["hora_entrada"], color=TEXTO)),
                    ft.DataCell(ft.Text(r["hora_salida"] or "-", color=TEXTO)),
                ]
            )
            for r in registros_filtrados
        ]

        tabla = ft.DataTable(
            columns=[
            ft.DataColumn(ft.Text("Identificador", weight="bold", color=TEXTO)),
            ft.DataColumn(ft.Text("Nombre completo", weight="bold", color=TEXTO)),
            ft.DataColumn(ft.Text("Fecha", weight="bold", color=TEXTO)),
            ft.DataColumn(ft.Text("Hora entrada", weight="bold", color=TEXTO)),
            ft.DataColumn(ft.Text("Hora salida", weight="bold", color=TEXTO)),
            ],
            rows=filas,
            heading_row_color="#F3F4F6",
        )

        tabla_container.controls.clear()
        tabla_container.controls.append(tabla)
        page.update()

    # ===== LIMPIAR =====
    def limpiar(e):
        input_busqueda.value = ""
        txt_fecha_inicio.value = "Fecha inicio"
        txt_fecha_fin.value = "Fecha fin"
        filtrar()

    # ===== FILTROS =====
    filtros = ft.Container(
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Row(
            [
                input_busqueda,
                fecha_inicio_btn,
                fecha_fin_btn,
                ft.IconButton(
                    icon=ft.Icons.CLEAR,
                    tooltip="Limpiar",
                    on_click=limpiar
                )
            ],
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    tabla_scroll = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=20,
        padding=15,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=tabla_container
    )

    filtrar()

    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=FONDO,
        border_radius=30,  
        content=ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Historial de visitas", size=32, weight="bold", color=TEXTO),
                        ft.Text("Sistema de control digital - Registro de asistencias", color=TEXTO),
                    ],
                    spacing=5
                ),
                filtros,
                tabla_scroll
            ],
            spacing=20,
            expand=True
        )
    )
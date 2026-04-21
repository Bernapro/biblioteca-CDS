import flet as ft
import json
from datetime import datetime


def historial_view(page):

    # cargar datos desde JSON
    def cargar_datos():
        with open("source/datos/datos.json", "r") as f:
            return json.load(f)

    data = cargar_datos()

    mensaje = ft.Text("", size=14)

    # CONTROLES DE FILTRO
    input_busqueda = ft.TextField(
        hint_text="Buscar por Identificador o nombre...",
        expand=True,
        color="black",
        border_color="black"
    )

    input_fecha_inicio = ft.TextField(
        hint_text="Fecha inicio (YYYY-MM-DD)",
        width=200,
        color="black",
        border_color="black"
    )

    input_fecha_fin = ft.TextField(
        hint_text="Fecha fin (YYYY-MM-DD)",
        width=200,
        color="black",
        border_color="black"
    )

    tabla_container = ft.Column(scroll="auto", expand=True)

    # FUNCION PARA VALIDAR FECHA
    def fecha_valida(fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except:
            return False

    # FUNCION PARA FILTRAR Y MOSTRAR RESULTADOS
    def filtrar(e=None):

        texto = input_busqueda.value.strip().lower() if input_busqueda.value else ""
        f_inicio = input_fecha_inicio.value.strip()
        f_fin = input_fecha_fin.value.strip()

        # RESET VISUAL
        input_fecha_inicio.border_color = "black"
        input_fecha_fin.border_color = "black"
        mensaje.value = ""

        # VALIDAR FECHAS
        if f_inicio and not fecha_valida(f_inicio):
            mensaje.value = "⚠️ Fecha inicio inválida (YYYY-MM-DD)"
            mensaje.color = "red"
            input_fecha_inicio.border_color = "red"
            page.update()
            return

        if f_fin and not fecha_valida(f_fin):
            mensaje.value = "⚠️ Fecha fin inválida (YYYY-MM-DD)"
            mensaje.color = "red"
            input_fecha_fin.border_color = "red"
            page.update()
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

      
        if not filas:
            mensaje.value = "⚠️ No se encontraron registros"
            mensaje.color = "orange"

        # CREAR TABLA CON LOS RESULTADOS
        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Identificador", color="black")),
                ft.DataColumn(ft.Text("Nombre completo", color="black")),
                ft.DataColumn(ft.Text("Fecha", color="black")),
                ft.DataColumn(ft.Text("Hora entrada", color="black")),
                ft.DataColumn(ft.Text("Hora salida", color="black")),
            ],
            rows=filas,
            column_spacing=40,
            heading_row_height=50,
            data_row_min_height=50,
        )

        tabla_container.controls.clear()
        tabla_container.controls.append(tabla)

        page.update()

    # FILTRAR AL CAMBIAR TEXTO O FECHAS
    input_busqueda.on_change = filtrar

    # BUSCAR AL PRESIONAR BOTÓN
    btn_buscar = ft.ElevatedButton(
        "Buscar",
        on_click=filtrar
    )

    # FILTRAR AL INICIAR
    filtrar()

    return ft.Container(
        expand=True,
        padding=25,
        content=ft.Column(
            [
                ft.Text("Historial de visitas", size=32, weight="bold", color="black"),
                ft.Text("Sistema de control digital - Registro de asistencias", color="black"),

                #  FILTROS
                ft.Row(
                    [
                        input_busqueda,
                        input_fecha_inicio,
                        input_fecha_fin,
                        btn_buscar
                    ],
                    spacing=15
                ),

                mensaje, 

                # tabla
                ft.Container(
                    expand=True,
                    padding=20,
                    bgcolor="white",
                    border_radius=25,
                    shadow=ft.BoxShadow(blur_radius=20, color="black12"),
                    content=tabla_container
                )
            ],
            spacing=20
        )
    )
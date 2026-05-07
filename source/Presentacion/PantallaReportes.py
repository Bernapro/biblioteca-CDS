import flet as ft
import flet_charts as fch
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from Negocio.Controlador.ControladorReportes import ControladorReportes


class PantallaReportes(ft.Container):

    def __init__(self, page: ft.Page):
        super().__init__()

        self._page = page
        self.controlador = ControladorReportes()

        # ===== COLORES =====
        self.AZUL = "#2563EB"
        self.PURPURA = "#7C3AED"
        self.VERDE = "#059669"

        self.TEXT = "onSurface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.CARD = "surface"
        self.BORDER = "outline"

        self.expand = True
        self.padding = 20

        # ===== ESTADO =====
        self.tipo_actual = "Alumnos"
        self.tipo_reporte = "Asistencia"

        # ===== FECHAS =====
        self.fecha_inicio = "2026-05-01"
        self.fecha_fin = "2026-05-31"

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        self.cards_row = ft.Row(spacing=20)

        self.chart_container = ft.Container(expand=True)

        self.distribution_container = ft.Container(expand=True)

        self.text_actualizacion = ft.Text(
            "Sin actualizar",
            color=self.TEXT_SECONDARY
        )

        self.content = ft.Container(

            expand=True,

            bgcolor=ft.Colors.GREY_100,

            padding=20,

            content=ft.Column(

                expand=True,

                spacing=20,

                scroll=ft.ScrollMode.AUTO,

                controls=[

                    # ===== HEADER =====
                    ft.Column(
                        spacing=5,
                        controls=[

                            ft.Text(
                                "Reportes",
                                size=28,
                                weight="bold"
                            ),

                            ft.Text(
                                "Estadísticas del sistema",
                                color=self.TEXT_SECONDARY
                            ),
                        ]
                    ),

                    # ===== FILTROS =====
                    self.build_filtros(),

                    # ===== CARDS =====
                    self.cards_row,

                    # ===== GRAFICAS + TABLAS =====
                    ft.Row(

                        expand=True,

                        spacing=20,

                        vertical_alignment=ft.CrossAxisAlignment.START,

                        controls=[

                            # ===== GRAFICA =====
                            ft.Container(

                                expand=1,

                                padding=15,

                                bgcolor=ft.Colors.WHITE,

                                border_radius=20,

                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=10,
                                    color=ft.Colors.BLACK12,
                                    offset=ft.Offset(0, 4)
                                ),

                                content=self.chart_container
                            ),

                            # ===== TABLA =====
                            ft.Container(

                                expand=2,

                                padding=15,

                                bgcolor=ft.Colors.WHITE,

                                border_radius=20,

                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=10,
                                    color=ft.Colors.BLACK12,
                                    offset=ft.Offset(0, 4)
                                ),

                                content=self.distribution_container
                            )
                        ]
                    ),

                    # ===== FOOTER =====
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            self.text_actualizacion
                        ]
                    )
                ]
            )
        )

        # ===== CARGA INICIAL =====
        self.actualizar(None)

    # ================= FILTROS =================
    def build_filtros(self):

        # ===== DATE PICKERS =====
        self.dp_inicio = ft.DatePicker(
            on_change=lambda e: self.set_fecha_inicio(
                e.control.value
            )
        )

        self.dp_fin = ft.DatePicker(
            on_change=lambda e: self.set_fecha_fin(
                e.control.value
            )
        )

        self._page.overlay.append(self.dp_inicio)
        self._page.overlay.append(self.dp_fin)

        # ===== INPUTS FECHAS =====
        self.input_inicio = ft.TextField(
            label="Fecha inicio",
            value=self.fecha_inicio,
            width=150,
            read_only=True,
            on_click=lambda e: self.abrir_fecha_inicio()
        )

        self.input_fin = ft.TextField(
            label="Fecha fin",
            value=self.fecha_fin,
            width=150,
            read_only=True,
            on_click=lambda e: self.abrir_fecha_fin()
        )

        # ===== FILTRO USUARIO =====
        self.dropdown = ft.Dropdown(
            width=180,
            value="Todos",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Alumnos"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitantes"),
            ],
        )

        # ===== TIPO REPORTE =====
        self.tipo_reporte_dd = ft.Dropdown(
            width=240,
            value="Asistencia completa",
            options=[
                ft.dropdown.Option("Asistencia completa"),
                ft.dropdown.Option("Usuarios más activos"),
                ft.dropdown.Option("Horas pico avanzado"),
                ft.dropdown.Option("Tendencia diaria"),
                ft.dropdown.Option("Reporte por carrera"),
                ft.dropdown.Option("Reporte por facultad"),
                ft.dropdown.Option("Reporte por semestre"),
                ft.dropdown.Option("Visitantes externos"),
                ft.dropdown.Option("Reporte de saturación"),
                ft.dropdown.Option("Reporte de crecimiento"),
            ],
        )

        return ft.Container(
            padding=20,
            border_radius=15,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[

                    # ===== FILTROS =====
                    ft.Row(
                        spacing=10,
                        controls=[
                            self.input_inicio,
                            self.input_fin,
                            self.dropdown,
                            self.tipo_reporte_dd,

                            # ===== BOTON ACTUALIZAR =====
                            ft.ElevatedButton(
                                "Actualizar",
                                icon=ft.Icons.REFRESH,
                                on_click=self.actualizar
                            ),
                        ]
                    ),

                    # ===== EXPORTAR =====
                    ft.ElevatedButton(
                        "Exportar",
                        icon=ft.Icons.DOWNLOAD,
                        on_click=self.exportar_excel
                    )
                ]
            )
        )
    
    def obtener_tipo_usuario(self):

        mapa = {
            "Alumnos": "ALUMNO",
            "Personal": "PERSONAL",
            "Visitantes": "VISITANTE"
        }

        if self.dropdown.value == "Todos":
            return None

        return mapa.get(self.dropdown.value)
    
    def mostrar_sin_datos(self):

        self.cards_row.controls = [
            self.card("Sin datos", "0", self.AZUL)
        ]

        self.chart_container.content = ft.Text("Sin datos")

        self.distribution_container.content = ft.Text("Sin datos")

        self._page.update()

    # ================= ACTUALIZAR =================
    def actualizar(self, e):

        tipo = self.tipo_reporte_dd.value

        # validar fechas
        if self.fecha_inicio > self.fecha_fin:

            self._page.snack_bar = ft.SnackBar(
                ft.Text("La fecha inicio no puede ser mayor a la fecha fin")
            )

            self._page.snack_bar.open = True
            self._page.update()

            return

        usuario = self.obtener_tipo_usuario()

        datos = self.controlador.generar_reporte(
            tipo=tipo,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            tipo_usuario=usuario
        )

        # guardar cache
        self.ultimo_reporte = datos

        if not datos:
            self.mostrar_sin_datos()
            return

        renderizadores = {

            "Asistencia completa": self.render_asistencia,

            "Usuarios más activos": self.render_usuarios_activos,

            "Horas pico avanzado": self.render_horas_pico,

            "Tendencia diaria": self.render_tendencia,

            "Reporte por carrera": self.render_carreras,

            "Reporte por facultad": self.render_facultades,

            "Reporte por semestre": self.render_semestres,

            "Visitantes externos": self.render_visitantes,

            "Reporte de saturación": self.render_saturacion,

            "Reporte de crecimiento": self.render_crecimiento,
        }

        render = renderizadores.get(tipo)

        if render:
            render(datos)

        self.text_actualizacion.value = (
            f"Actualizado: "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )

        self._page.update()

    # ================= GRAFICA DINAMICA =================
    def generar_grafica(self, tipo, datos):

        if tipo != "Horas pico":
            return ft.Text("Sin gráfica")

        grupos = []

        for i, d in enumerate(datos):

            grupos.append(

                fch.BarChartGroup(

                    x=i,

                    rods=[

                        fch.BarChartRod(

                            from_y=0,

                            to_y=d["total"],

                            width=30,

                            color=self.AZUL,
                        )
                    ]
                )
            )

        return ft.Container(

            expand=True,

            padding=20,

            content=fch.BarChart(

                expand=True,

                max_y=max(d["total"] for d in datos) + 5,

                groups=grupos,

                border=ft.border.all(
                    1,
                    ft.Colors.GREY_300
                ),

                left_axis=fch.ChartAxis(
                    label_size=40
                ),

                bottom_axis=fch.ChartAxis(

                    label_size=35,

                    labels=[

                        fch.ChartAxisLabel(

                            value=i,

                            label=ft.Text(
                                f"{int(d['hora'])}:00"
                            )
                        )

                        for i, d in enumerate(datos)
                    ]
                )
            )
        )

    # ================= DISTRIBUCION =================
    def generar_distribucion(self, datos):

        total = len(datos)

        return ft.Container(
            width=300,
            padding=20,
            content=ft.Column([
                ft.Text("Total registros"),
                ft.Text(str(total), size=24, weight="bold")
            ])
        )

    # ================= EXPORTAR =================
    def exportar_excel(self, e):

        usuario = self.obtener_tipo_usuario()

        nombre = f"reporte_{self.tipo_reporte_dd.value}.xlsx"

        # ventana oculta
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        ruta = filedialog.asksaveasfilename(
            title="Guardar reporte",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=nombre
        )

        root.destroy()

        if not ruta:
            return

        try:

            generado = self.controlador.exportar_excel(
                ruta=ruta,
                tipo=self.tipo_reporte_dd.value,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
                tipo_usuario=usuario
            )

            if generado:

                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Reporte exportado correctamente")
                )

            else:

                self._page.snack_bar = ft.SnackBar(
                    ft.Text("No hay datos para exportar")
                )

        except Exception as ex:

            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {str(ex)}")
            )

        self._page.snack_bar.open = True
        self._page.update()

    # ================= CARD =================
    def card(self, title, value, color):

        return ft.Container(
            expand=True,

            padding=20,

            bgcolor=ft.Colors.WHITE,

            border_radius=20,

            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 4)
            ),

            content=ft.Column(
                spacing=10,
                controls=[

                    ft.Text(
                        title,
                        size=14,
                        color=ft.Colors.GREY_700
                    ),

                    ft.Text(
                        value,
                        size=30,
                        weight="bold",
                        color=color
                    ),
                ]
            )
        )
    
    def set_fecha_inicio(self, fecha):
        if fecha:
            self.fecha_inicio = fecha.strftime("%Y-%m-%d")
            self.input_inicio.value = self.fecha_inicio
            self._page.update()


    def set_fecha_fin(self, fecha):
        if fecha:
            self.fecha_fin = fecha.strftime("%Y-%m-%d")
            self.input_fin.value = self.fecha_fin
            self._page.update()

    def abrir_fecha_inicio(self):
        self.dp_inicio.open = True
        self._page.update()


    def abrir_fecha_fin(self):
        self.dp_fin.open = True
        self._page.update()

    def crear_tabla(self, columnas, filas):

        tabla = ft.DataTable(

            heading_row_height=45,
            data_row_min_height=40,
            column_spacing=30,

            columns=[
                ft.DataColumn(ft.Text(col))
                for col in columnas
            ],

            rows=[

                ft.DataRow(

                    color=(
                        ft.Colors.GREY_100
                        if i % 2 == 0
                        else ft.Colors.WHITE
                    ),

                    cells=[

                        ft.DataCell(
                            ft.Text(str(valor))
                        )

                        for valor in fila
                    ]
                )

                for i, fila in enumerate(filas)
            ]
        )

        return ft.Container(
            expand=True,
            height=500,
            padding=10,

            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,

                controls=[
                    ft.Row(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[tabla]
                    )
                ]
            )
        )

    def render_asistencia(self, datos):

        total = len(datos)

        self.cards_row.controls = [
            self.card("Registros", str(total), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte de asistencia completa"
        )

        filas = []

        for d in datos:

            filas.append([
                d["identificador"],
                d["nombre_completo"],
                d["tipo_usuario"],
                str(d["fecha_entrada"]),
                str(d["fecha_salida"]) if d["fecha_salida"] else "ACTIVO",
                d["estado"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "ID",
                "Nombre",
                "Tipo",
                "Entrada",
                "Salida",
                "Estado"
            ],
            filas=filas
        )

    def render_usuarios_activos(self, datos):

        total = len(datos)

        horas = sum(d["horas_totales"] for d in datos)

        self.cards_row.controls = [
            self.card("Usuarios", str(total), self.AZUL),

            self.card(
                "Horas acumuladas",
                str(round(horas, 2)),
                self.VERDE
            ),
        ]

        self.chart_container.content = ft.Text(
            "Usuarios más activos"
        )

        filas = []

        for d in datos:

            filas.append([
                d["nombre_completo"],
                d["tipo_usuario"],
                d["visitas"],
                d["horas_totales"],
                d["promedio_horas"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Nombre",
                "Tipo",
                "Visitas",
                "Horas",
                "Promedio"
            ],
            filas=filas
        )

    def render_horas_pico(self, datos):

        total = sum(d["total"] for d in datos)

        self.cards_row.controls = [
            self.card("Entradas", str(total), self.AZUL),

            self.card(
                "Horas",
                str(len(datos)),
                self.VERDE
            ),
        ]

        self.chart_container.content = self.generar_grafica(
            "Horas pico",
            datos
        )

        filas = []

        for d in datos:

            filas.append([
                f"{int(d['hora'])}:00",
                d["total"],
                d["alumnos"],
                d["personal"],
                d["visitantes"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Hora",
                "Total",
                "Alumnos",
                "Personal",
                "Visitantes"
            ],
            filas=filas
        )

    def render_tendencia(self, datos):

        total = sum(d["total_usuarios"] for d in datos)

        self.cards_row.controls = [
            self.card("Total", str(total), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Tendencia diaria"
        )

        filas = []

        for d in datos:

            filas.append([
                str(d["fecha"]),
                d["total_usuarios"],
                d["alumnos"],
                d["personal"],
                d["visitantes"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Fecha",
                "Total",
                "Alumnos",
                "Personal",
                "Visitantes"
            ],
            filas=filas
        )

    def render_carreras(self, datos):

        self.cards_row.controls = [
            self.card("Carreras", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte por carrera"
        )

        filas = []

        for d in datos:

            filas.append([
                d["carrera"],
                d["total_visitas"],
                d["usuarios_unicos"],
                d["promedio_horas"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Carrera",
                "Visitas",
                "Usuarios",
                "Promedio hrs"
            ],
            filas=filas
        )

    def render_facultades(self, datos):

        self.cards_row.controls = [
            self.card("Facultades", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte por facultad"
        )

        filas = []

        for d in datos:

            filas.append([
                d["facultad"],
                d["total_visitas"],
                d["usuarios_unicos"],
                d["promedio_horas"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Facultad",
                "Visitas",
                "Usuarios",
                "Promedio hrs"
            ],
            filas=filas
        )

    def render_semestres(self, datos):

        self.cards_row.controls = [
            self.card("Semestres", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte por semestre"
        )

        filas = []

        for d in datos:

            filas.append([
                d["semestre"],
                d["total_visitas"],
                d["usuarios_unicos"],
                d["promedio_horas"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Semestre",
                "Visitas",
                "Usuarios",
                "Promedio hrs"
            ],
            filas=filas
        )

    def render_visitantes(self, datos):

        self.cards_row.controls = [
            self.card("Instituciones", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Visitantes externos"
        )

        filas = []

        for d in datos:

            filas.append([
                d["institucion"],
                d["total_visitas"],
                d["usuarios_unicos"],
                d["promedio_horas"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Institución",
                "Visitas",
                "Usuarios",
                "Promedio hrs"
            ],
            filas=filas
        )

    def render_saturacion(self, datos):

        pico = max(d["total_usuarios"] for d in datos)

        self.cards_row.controls = [
            self.card("Pico máximo", str(pico), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte de saturación"
        )

        filas = []

        for d in datos:

            filas.append([
                f"{int(d['hora'])}:00",
                d["total_usuarios"],
                d["alumnos"],
                d["personal"],
                d["visitantes"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Hora",
                "Total",
                "Alumnos",
                "Personal",
                "Visitantes"
            ],
            filas=filas
        )

    def render_crecimiento(self, datos):

        self.cards_row.controls = [
            self.card("Meses", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Reporte de crecimiento"
        )

        filas = []

        for d in datos:

            filas.append([
                d["mes"],
                d["total_visitas"],
                d["usuarios_unicos"],
                d["alumnos"],
                d["personal"],
                d["visitantes"]
            ])

        self.distribution_container.content = self.crear_tabla(
            columnas=[
                "Mes",
                "Visitas",
                "Usuarios",
                "Alumnos",
                "Personal",
                "Visitantes"
            ],
            filas=filas
        )




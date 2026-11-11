import os
from datetime import datetime, timedelta
import flet as ft
from Negocio.Controlador.ControladorReportes import ControladorReportes


class PantallaReportes(ft.Container):

    def __init__(self, page: ft.Page, controlador=None):
        super().__init__()

        self._page = page
        self.controlador = controlador or ControladorReportes()

        # ===== COLORES SEMÁNTICOS (COMPATIBLE CON MODO CLARO/OSCURO) =====
        self.AZUL = "#2563EB"
        self.PURPURA = "#7C3AED"
        self.VERDE = "#059669"
        self.NARANJA = "#F59E0B"

        self.PRIMARY = "primary"
        self.TEXT = "onSurface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.CARD = "surface"
        self.SURFACE_VARIANT = "surfaceVariant"
        self.BORDER = "outline"

        self.expand = True
        self.padding = 20
        self.bgcolor = "transparent"

        # ===== ESTADO =====
        self.tipo_actual = "Alumnos"
        self.tipo_reporte = "Asistencia completa"
        self.ultimo_reporte = []
        self.columnas_actuales = []
        self.filas_actuales = []

        # ===== FECHAS DINÁMICAS =====
        hoy = datetime.now()
        self.fecha_inicio = hoy.replace(day=1).strftime("%Y-%m-%d")
        self.fecha_fin = hoy.strftime("%Y-%m-%d")

        self.build_ui()

    def _safe_page_update(self):
        try:
            if self._page is not None and hasattr(self._page, "update"):
                self._page.update()
        except Exception:
            pass

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
            bgcolor="transparent",
            padding=10,
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
                                weight="bold",
                                color=self.TEXT
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
                                bgcolor=self.CARD,
                                border=ft.Border.all(1, self.BORDER),
                                border_radius=20,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=10,
                                    color="black12",
                                    offset=ft.Offset(0, 4)
                                ),
                                content=self.chart_container
                            ),

                            # ===== TABLA =====
                            ft.Container(
                                expand=2,
                                padding=15,
                                bgcolor=self.CARD,
                                border=ft.Border.all(1, self.BORDER),
                                border_radius=20,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=10,
                                    color="black12",
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

        if self._page is not None and hasattr(self._page, "overlay"):
            self._page.overlay.append(self.dp_inicio)
            self._page.overlay.append(self.dp_fin)

        # ===== INPUTS FECHAS =====
        self.input_inicio = ft.TextField(
            label="Fecha inicio",
            value=self.fecha_inicio,
            width=150,
            read_only=True,
            bgcolor=self.CARD,
            color=self.TEXT,
            border_color=self.BORDER,
            text_style=ft.TextStyle(color=self.TEXT),
            label_style=ft.TextStyle(color=self.TEXT_SECONDARY),
            on_click=lambda e: self.abrir_fecha_inicio()
        )

        self.input_fin = ft.TextField(
            label="Fecha fin",
            value=self.fecha_fin,
            width=150,
            read_only=True,
            bgcolor=self.CARD,
            color=self.TEXT,
            border_color=self.BORDER,
            text_style=ft.TextStyle(color=self.TEXT),
            label_style=ft.TextStyle(color=self.TEXT_SECONDARY),
            on_click=lambda e: self.abrir_fecha_fin()
        )

        # ===== FILTRO USUARIO =====
        self.dropdown = ft.Dropdown(
            width=180,
            value="Todos",
            bgcolor=self.CARD,
            color=self.TEXT,
            border_color=self.BORDER,
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
            bgcolor=self.CARD,
            color=self.TEXT,
            border_color=self.BORDER,
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
            bgcolor=self.CARD,
            border=ft.Border.all(1, self.BORDER),
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
                            ft.Button(
                                "Actualizar",
                                icon=ft.Icons.REFRESH,
                                bgcolor=self.PRIMARY,
                                color="onPrimary",
                                on_click=self.actualizar
                            ),
                        ]
                    ),

                    # ===== EXPORTAR =====
                    ft.Button(
                        "Exportar",
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor=self.VERDE,
                        color="white",
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
        self.columnas_actuales = []
        self.filas_actuales = []

        self.cards_row.controls = [
            self.card("Sin datos", "0", self.AZUL)
        ]

        self.chart_container.content = ft.Text(
            "Sin datos",
            color=self.TEXT_SECONDARY
        )

        self.distribution_container.content = ft.Text(
            "Sin datos",
            color=self.TEXT_SECONDARY
        )

        self._safe_page_update()

    # ================= ACTUALIZAR =================
    def actualizar(self, e=None):

        tipo = self.tipo_reporte_dd.value

        # validar fechas
        if self.fecha_inicio > self.fecha_fin:
            if self._page is not None:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("La fecha inicio no puede ser mayor a la fecha fin")
                )
                self._page.snack_bar.open = True
                self._safe_page_update()
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

        self._safe_page_update()

    # ================= GRAFICA DINAMICA CON CONTROLES NATIVOS FLET =================
    def _construir_barras_dinamicas(self, titulo, items, unidad=""):
        if not items:
            return ft.Container(
                expand=True,
                padding=20,
                content=ft.Text("Sin datos para graficar", color=self.TEXT_SECONDARY)
            )

        valores = [float(val or 0) for _, val, _ in items]
        max_valor = max(valores, default=0)
        divisor = max_valor if max_valor > 0 else 1

        columnas_barras = []
        filas_resumen = []

        for etiqueta, valor, color in items[:12]:
            val_num = float(valor or 0)
            proporcion = val_num / divisor
            altura = max(12, int(proporcion * 160)) if val_num > 0 else 8
            val_texto = f"{int(val_num)}" if val_num.is_integer() else f"{round(val_num, 2)}"

            columnas_barras.append(
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                    spacing=5,
                    controls=[
                        ft.Text(
                            val_texto,
                            size=11,
                            weight="bold",
                            color=self.TEXT
                        ),
                        ft.Container(
                            width=32,
                            height=altura,
                            border_radius=6,
                            bgcolor=color,
                            tooltip=f"{etiqueta}: {val_texto} {unidad}".strip()
                        ),
                        ft.Container(
                            width=64,
                            content=ft.Text(
                                str(etiqueta),
                                size=10,
                                color=self.TEXT_SECONDARY,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS
                            )
                        )
                    ]
                )
            )

            filas_resumen.append(
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    str(etiqueta),
                                    size=12,
                                    color=self.TEXT,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=True
                                ),
                                ft.Text(
                                    f"{val_texto} {unidad}".strip(),
                                    size=12,
                                    weight="bold",
                                    color=color
                                )
                            ]
                        ),
                        ft.ProgressBar(
                            value=max(0.0, min(1.0, proporcion)),
                            color=color,
                            bgcolor=self.SURFACE_VARIANT,
                            height=6,
                            border_radius=4
                        )
                    ]
                )
            )

        return ft.Container(
            expand=True,
            padding=10,
            bgcolor=self.CARD,
            content=ft.Column(
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text(
                        titulo,
                        size=16,
                        weight="bold",
                        color=self.TEXT
                    ),
                    ft.Container(
                        height=230,
                        padding=ft.Padding.symmetric(horizontal=10, vertical=10),
                        border_radius=12,
                        bgcolor=self.SURFACE_VARIANT,
                        alignment=ft.Alignment(0, 1),
                        content=ft.Row(
                            scroll=ft.ScrollMode.AUTO,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            spacing=12,
                            controls=columnas_barras
                        )
                    ),
                    ft.Column(
                        spacing=8,
                        controls=filas_resumen
                    )
                ]
            )
        )

    def generar_grafica(self, tipo, datos):
        if not datos:
            return ft.Container(
                expand=True,
                padding=20,
                content=ft.Text(
                    "Sin datos para graficar",
                    color=self.TEXT_SECONDARY
                )
            )

        paleta = [self.AZUL, self.VERDE, self.PURPURA, self.NARANJA]

        if tipo == "Asistencia completa":
            activos = sum(
                1 for d in datos
                if str(d.get("estado", "")).upper() == "ACTIVO"
                or (d.get("estado") is None and d.get("fecha_salida") is None)
            )
            finalizados = max(0, len(datos) - activos)
            alumnos = sum(1 for d in datos if str(d.get("tipo_usuario", "")).upper() == "ALUMNO")
            personal = sum(1 for d in datos if str(d.get("tipo_usuario", "")).upper() == "PERSONAL")
            visitantes = sum(1 for d in datos if str(d.get("tipo_usuario", "")).upper() == "VISITANTE")

            items = [
                ("Activos", activos, self.VERDE),
                ("Finalizados", finalizados, self.AZUL),
                ("Alumnos", alumnos, self.AZUL),
                ("Personal", personal, self.PURPURA),
                ("Visitantes", visitantes, self.NARANJA),
            ]
            return self._construir_barras_dinamicas(
                "Resumen de Asistencia",
                items,
                unidad="registros"
            )

        elif tipo == "Usuarios más activos":
            items = []
            for i, d in enumerate(datos[:10]):
                nombre = str(d.get("nombre_completo", "Usuario"))
                valor = d.get("horas_totales", 0) or d.get("visitas", 0)
                items.append((nombre, valor, paleta[i % len(paleta)]))
            return self._construir_barras_dinamicas(
                "Top Usuarios Más Activos",
                items,
                unidad="hrs"
            )

        elif tipo in ("Horas pico avanzado", "Horas pico"):
            items = [
                (
                    f"{int(d.get('hora', 0))}:00",
                    d.get("total", d.get("total_usuarios", 0)),
                    self.AZUL
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Entradas por Hora del Día",
                items,
                unidad="entradas"
            )

        elif tipo == "Tendencia diaria":
            items = [
                (
                    str(d.get("fecha", "")),
                    d.get("total_usuarios", d.get("total", 0)),
                    self.VERDE
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Tendencia Diaria de Visitas",
                items,
                unidad="visitas"
            )

        elif tipo == "Reporte por carrera":
            items = [
                (
                    str(d.get("carrera", "Sin carrera")),
                    d.get("total_visitas", 0),
                    paleta[i % len(paleta)]
                )
                for i, d in enumerate(datos)
            ]
            return self._construir_barras_dinamicas(
                "Visitas por Carrera",
                items,
                unidad="visitas"
            )

        elif tipo == "Reporte por facultad":
            items = [
                (
                    str(d.get("facultad", "Sin facultad")),
                    d.get("total_visitas", 0),
                    paleta[i % len(paleta)]
                )
                for i, d in enumerate(datos)
            ]
            return self._construir_barras_dinamicas(
                "Visitas por Facultad",
                items,
                unidad="visitas"
            )

        elif tipo == "Reporte por semestre":
            items = [
                (
                    f"Sem {d.get('semestre', '?')}",
                    d.get("total_visitas", 0),
                    self.VERDE
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Visitas por Semestre",
                items,
                unidad="visitas"
            )

        elif tipo == "Visitantes externos":
            items = [
                (
                    str(d.get("institucion", "Sin institución")),
                    d.get("total_visitas", 0),
                    self.NARANJA
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Visitantes por Institución",
                items,
                unidad="visitas"
            )

        elif tipo == "Reporte de saturación":
            items = [
                (
                    f"{int(d.get('hora', 0))}:00",
                    d.get("total_usuarios", d.get("total", 0)),
                    self.PURPURA
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Saturación por Hora",
                items,
                unidad="usuarios"
            )

        elif tipo == "Reporte de crecimiento":
            items = [
                (
                    str(d.get("mes", "")),
                    d.get("total_visitas", 0),
                    self.VERDE
                )
                for d in datos
            ]
            return self._construir_barras_dinamicas(
                "Crecimiento Mensual",
                items,
                unidad="visitas"
            )

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Text("Sin gráfica", color=self.TEXT_SECONDARY)
        )

    # ================= DISTRIBUCION =================
    def generar_distribucion(self, datos):
        total = len(datos) if datos else 0

        return ft.Container(
            width=300,
            padding=20,
            bgcolor=self.CARD,
            content=ft.Column([
                ft.Text("Total registros", color=self.TEXT_SECONDARY),
                ft.Text(str(total), size=24, weight="bold", color=self.TEXT)
            ])
        )

    # ================= EXPORTAR =================
    def exportar_excel(self, e=None, ruta=None):
        if not self.filas_actuales and not self.ultimo_reporte:
            if self._page is not None:
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("No hay datos para exportar")
                )
                self._page.snack_bar.open = True
                self._safe_page_update()
            return False

        usuario = self.obtener_tipo_usuario()
        tipo = self.tipo_reporte_dd.value
        nombre_limpio = tipo.lower().replace(" ", "_")
        nombre = f"reporte_{nombre_limpio}.xlsx"

        if not ruta:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            root.lift()
            root.focus()
            ruta = filedialog.asksaveasfilename(
                title="Guardar reporte",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=nombre
            )
            root.destroy()

        if not ruta:
            return False

        try:
            generado = self.controlador.exportar_excel(
                ruta=ruta,
                tipo=tipo,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
                tipo_usuario=usuario,
                columnas=self.columnas_actuales,
                filas=self.filas_actuales
            )

            if generado:
                mensaje = f"Reporte exportado correctamente en: {ruta}"
            else:
                mensaje = "No hay datos para exportar"

        except Exception as ex:
            generado = False
            mensaje = f"Error: {str(ex)}"

        if self._page is not None:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(mensaje)
            )
            self._page.snack_bar.open = True
            self._safe_page_update()

        return generado

    # ================= CARD =================
    def card(self, title, value, color):
        return ft.Container(
            expand=True,
            padding=20,
            bgcolor=self.CARD,
            border=ft.Border.all(1, self.BORDER),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color="black12",
                offset=ft.Offset(0, 4)
            ),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(
                        title,
                        size=14,
                        color=self.TEXT_SECONDARY
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
            self._safe_page_update()

    def set_fecha_fin(self, fecha):
        if fecha:
            self.fecha_fin = fecha.strftime("%Y-%m-%d")
            self.input_fin.value = self.fecha_fin
            self._safe_page_update()

    def abrir_fecha_inicio(self):
        self.dp_inicio.open = True
        self._safe_page_update()

    def abrir_fecha_fin(self):
        self.dp_fin.open = True
        self._safe_page_update()

    def crear_tabla(self, columnas, filas):
        self.columnas_actuales = list(columnas) if columnas else []
        self.filas_actuales = list(filas) if filas else []

        tabla = ft.DataTable(
            heading_row_height=45,
            data_row_min_height=40,
            column_spacing=30,
            heading_row_color=self.SURFACE_VARIANT,
            columns=[
                ft.DataColumn(ft.Text(col, weight="bold", color=self.TEXT))
                for col in columnas
            ],
            rows=[
                ft.DataRow(
                    color=(
                        self.SURFACE_VARIANT
                        if i % 2 == 0
                        else self.CARD
                    ),
                    cells=[
                        ft.DataCell(
                            ft.Text(str(valor), color=self.TEXT)
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
            bgcolor=self.CARD,
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
        datos = datos or []
        total = len(datos)

        self.cards_row.controls = [
            self.card("Registros", str(total), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Asistencia completa",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("identificador", ""),
                d.get("nombre_completo", ""),
                d.get("tipo_usuario", ""),
                str(d.get("fecha_entrada", "")),
                str(d["fecha_salida"]) if d.get("fecha_salida") else "ACTIVO",
                d.get("estado", "ACTIVO" if not d.get("fecha_salida") else "FINALIZADO")
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
        datos = datos or []
        total = len(datos)
        horas = sum(float(d.get("horas_totales", 0) or 0) for d in datos)

        self.cards_row.controls = [
            self.card("Usuarios", str(total), self.AZUL),
            self.card(
                "Horas acumuladas",
                str(round(horas, 2)),
                self.VERDE
            ),
        ]

        self.chart_container.content = self.generar_grafica(
            "Usuarios más activos",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("nombre_completo", ""),
                d.get("tipo_usuario", ""),
                d.get("visitas", 0),
                d.get("horas_totales", 0),
                d.get("promedio_horas", 0)
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
        datos = datos or []
        total = sum(int(d.get("total", 0) or 0) for d in datos)

        self.cards_row.controls = [
            self.card("Entradas", str(total), self.AZUL),
            self.card(
                "Horas",
                str(len(datos)),
                self.VERDE
            ),
        ]

        self.chart_container.content = self.generar_grafica(
            "Horas pico avanzado",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                f"{int(d.get('hora', 0))}:00",
                d.get("total", 0),
                d.get("alumnos", 0),
                d.get("personal", 0),
                d.get("visitantes", 0)
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
        datos = datos or []
        total = sum(int(d.get("total_usuarios", 0) or 0) for d in datos)

        self.cards_row.controls = [
            self.card("Total", str(total), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Tendencia diaria",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                str(d.get("fecha", "")),
                d.get("total_usuarios", 0),
                d.get("alumnos", 0),
                d.get("personal", 0),
                d.get("visitantes", 0)
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
        datos = datos or []
        self.cards_row.controls = [
            self.card("Carreras", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Reporte por carrera",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("carrera", ""),
                d.get("total_visitas", 0),
                d.get("usuarios_unicos", 0),
                d.get("promedio_horas", 0)
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
        datos = datos or []
        self.cards_row.controls = [
            self.card("Facultades", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Reporte por facultad",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("facultad", ""),
                d.get("total_visitas", 0),
                d.get("usuarios_unicos", 0),
                d.get("promedio_horas", 0)
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
        datos = datos or []
        self.cards_row.controls = [
            self.card("Semestres", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Reporte por semestre",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("semestre", ""),
                d.get("total_visitas", 0),
                d.get("usuarios_unicos", 0),
                d.get("promedio_horas", 0)
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
        datos = datos or []
        self.cards_row.controls = [
            self.card("Instituciones", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Visitantes externos",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("institucion", ""),
                d.get("total_visitas", 0),
                d.get("usuarios_unicos", 0),
                d.get("promedio_horas", 0)
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
        datos = datos or []
        pico = max((int(d.get("total_usuarios", 0) or 0) for d in datos), default=0)

        self.cards_row.controls = [
            self.card("Pico máximo", str(pico), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Reporte de saturación",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                f"{int(d.get('hora', 0))}:00",
                d.get("total_usuarios", 0),
                d.get("alumnos", 0),
                d.get("personal", 0),
                d.get("visitantes", 0)
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
        datos = datos or []
        self.cards_row.controls = [
            self.card("Meses", str(len(datos)), self.AZUL)
        ]

        self.chart_container.content = self.generar_grafica(
            "Reporte de crecimiento",
            datos
        )

        filas = []
        for d in datos:
            filas.append([
                d.get("mes", ""),
                d.get("total_visitas", 0),
                d.get("usuarios_unicos", 0),
                d.get("alumnos", 0),
                d.get("personal", 0),
                d.get("visitantes", 0)
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

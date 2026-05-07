import flet as ft
from Negocio.Controlador.ControladorHistorial import ControladorHistorial
from Negocio.Utilidades.Herramientas import Herramientas

from tkinter import filedialog
import tkinter as tk


class PantallaHistorial(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        self.controlador_historial = ControladorHistorial()
        
        self.expand = True
        self.padding = 30
        self.bgcolor = "transparent"
        self.border_radius = 30

        self.AZUL = "#3B82F6"
        self.TEXT = "onSurface"
        self.GRIS_TEXTO = "onSurfaceVariant"
        self.GRIS_BORDE = "outline"
        self.FONDO_HEADER = "surfaceVariant"
        self.CARD = "surface"
        self.VERDE = "#10B981"
        self.ROJO = "#EF4444"
        self.NARANJA = "#F59E0B"

        self.txt_fecha_inicio = ft.Text("Fecha inicio", color=self.TEXT)
        self.txt_fecha_fin = ft.Text("Fecha fin", color=self.TEXT)

        self.fecha_inicio_picker = ft.DatePicker(on_change=self.seleccionar_inicio)
        self.fecha_fin_picker = ft.DatePicker(on_change=self.seleccionar_fin)
        self._page.overlay.extend([self.fecha_inicio_picker, self.fecha_fin_picker])

        self.btn_limpiar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CLEAR, color="white", size=18),
                ft.Text("Limpiar filtros", color="white", size=12, weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            bgcolor=self.ROJO,
            ink=True,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=10,
            on_click=self.limpiar_filtros
        )

        self.input_busqueda = ft.TextField(
            label="Buscar por identificador o nombre...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=12,
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            bgcolor=self.CARD,
            on_change=self.filtrar, 
            text_style=ft.TextStyle(color=self.TEXT),
            label_style=ft.TextStyle(color=self.GRIS_TEXTO),
        )
        
        self.combo_tipo = ft.Dropdown(
            expand=True,
            label="Tipo de usuario",
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="surface",
            color="onSurface",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Alumno"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitante"),
            ],
            value="Todos",
            on_select=self.filtrar
        )

        self.combo_estado = ft.Dropdown(
            expand=True,
            label="Estado",
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="surface",
            color="onSurface",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Activos"),
                ft.dropdown.Option("Finalizados"),
            ],
            value="Todos",
            on_select=self.filtrar
        )

        self.exportando = False

        self.btn_exportar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DOWNLOAD, color="white", size=18),
                ft.Text("Exportar resultados", color="white", weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            bgcolor=self.AZUL,
            border_radius=12,
            ink=True,
            padding=ft.padding.symmetric(horizontal=15),
            height=38,
            expand=True,
            on_click=self.toggle_exportar
        )

        self.btn_excel = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.TABLE_CHART, color=self.VERDE),
                ft.Text("Excel", color=self.VERDE, weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            border=ft.border.all(1, self.VERDE),
            border_radius=10,
            bgcolor="transparent",
            height=38,
            ink=True,
            expand=True,
            on_click=self.exportar_excel
        )

        self.btn_pdf = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PICTURE_AS_PDF, color=self.ROJO),
                ft.Text("PDF", color=self.ROJO, weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            border=ft.border.all(1, self.ROJO),
            bgcolor="transparent",
            border_radius=10,
            height=38,
            ink=True,
            expand=True,
            on_click=self.exportar_pdf
        )

        self.export_container = ft.Row(expand=True)
        self.actualizar_exportar()

        self.txt_hoy = ft.Text("0", size=18, weight="bold", color=self.TEXT)
        
        self.card_hoy = ft.Container(
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            bgcolor=self.CARD,
            border_radius=20,
            border=ft.border.all(1, self.GRIS_BORDE),
            expand=True,
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.PEOPLE_ALT_ROUNDED, color=self.CARD, size=20),
                    bgcolor=self.TEXT,
                    padding=8,
                    border_radius=12
                ),
                ft.Column([
                    ft.Text("Usuarios únicos hoy", size=12, color=self.GRIS_TEXTO),
                    self.txt_hoy,
                    ft.Text("Asistieron hoy a la biblioteca", size=12, color=self.GRIS_TEXTO)
                ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=10)
        )

        self.tabla_container = ft.Column(
            scroll="auto",
            expand=True,
            spacing=0   
        )
        self.pagina_actual = 1
        self.registros_por_pagina = 10
        self.total_registros = 0

        self.footer_tabla = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER  
        )

        self.build_ui()

    def did_mount(self):
        
        self.controlador_historial.cerrar_registros()
        self.filtrar()
        
    def seleccionar_inicio(self, e):
        if e.control.value:
            self.txt_fecha_inicio.value = e.control.value.strftime("%Y-%m-%d")
            self.filtrar()
            self.update()

    def seleccionar_fin(self, e):
        if e.control.value:
            self.txt_fecha_fin.value = e.control.value.strftime("%Y-%m-%d")
            self.filtrar()
            self.update()

    def abrir_picker(self, e, picker):
        picker.open = True
        self._page.update()

    def build_boton_fecha(self, texto_ref, picker):
        return ft.Container(
            expand=True,
            height=38,
            border=ft.border.all(1, self.GRIS_BORDE),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12),
            bgcolor=self.CARD,
            on_click=lambda e: self.abrir_picker(e, picker),
            content=ft.Row(
                [ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=self.AZUL), texto_ref],
                spacing=10
            )
        )

    def toggle_exportar(self, e):
        self.exportando = True
        self.actualizar_exportar()
        self.update()

    def generar_nombre_excel(self):
        partes = ["Historial"]
        if self.input_busqueda.value:
            texto = self.input_busqueda.value.strip().replace(" ", "")
            partes.append(texto[:6])
        if self.combo_tipo.value != "Todos":
            partes.append(self.combo_tipo.value)
        if self.combo_estado.value != "Todos":
            partes.append(self.combo_estado.value)
        if self.txt_fecha_inicio.value != "Fecha inicio":
            partes.append(self.txt_fecha_inicio.value)
        if self.txt_fecha_fin.value != "Fecha fin":
            partes.append(self.txt_fecha_fin.value)
        return "_".join(partes) + ".xlsx"
    
    def exportar_excel(self, e):
        nombre = self.generar_nombre_excel()

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)  
        root.lift()
        root.focus()
        
        ruta = filedialog.asksaveasfilename(
            title="Guardar Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=nombre
        )
        
        root.destroy()

        if ruta:
            self.resultado_guardar_excel_path(ruta)

        self.exportando = False
        self.actualizar_exportar()
        self.update()

    def resultado_guardar_excel_path(self, ruta):
        if not ruta:
            return

        try:
            self.controlador_historial.exportar_excel(
                ruta=ruta,
                texto=self.input_busqueda.value or "",
                fecha_inicio=self.txt_fecha_inicio.value if self.txt_fecha_inicio.value != "Fecha inicio" else None,
                fecha_fin=self.txt_fecha_fin.value if self.txt_fecha_fin.value != "Fecha fin" else None,
                tipo=self.combo_tipo.value,
                estado=self.combo_estado.value
            )

            print("Archivo guardado en:", ruta)

        except Exception as ex:
            print("Error:", ex)

    def exportar_pdf(self, e):
        print("Exportar PDF")
        self.exportando = False
        self.actualizar_exportar()
        self.update()

    def actualizar_exportar(self):
        if self.exportando:
            self.export_container.controls = [
                self.btn_excel,
                self.btn_pdf
            ]
        else:
            self.export_container.controls = [
                self.btn_exportar
            ]

    def limpiar_filtros(self, e=None):
        Herramientas.limpiar_control(self.input_busqueda)
        Herramientas.reset_dropdown(self.combo_tipo)
        Herramientas.reset_dropdown(self.combo_estado)
        Herramientas.reset_datepicker(self.fecha_inicio_picker)
        Herramientas.reset_datepicker(self.fecha_fin_picker)

        self.txt_fecha_inicio.value = "Fecha inicio"
        self.txt_fecha_fin.value = "Fecha fin"
        self.combo_tipo.value = "Todos"
        self.combo_estado.value = "Todos"

        self.filtrar()

        if self._page:
            self.update()

    def filtrar(self, e=None):
        if e:
            self.pagina_actual = 1

        inicio = (self.pagina_actual - 1) * self.registros_por_pagina

        datos, total = self.controlador_historial.obtener_historial(
            texto=self.input_busqueda.value or "",
            fecha_inicio=None if self.txt_fecha_inicio.value == "Fecha inicio" else self.txt_fecha_inicio.value,
            fecha_fin=None if self.txt_fecha_fin.value == "Fecha fin" else self.txt_fecha_fin.value,
            tipo=self.combo_tipo.value,
            estado=self.combo_estado.value,
            limit=self.registros_por_pagina,
            offset=inicio
        )
        total_hoy = self.controlador_historial.contar_usuarios_hoy()
        self.txt_hoy.value = str(total_hoy)

        self.total_registros = total
        self.datos_completos = self.controlador_historial._datos_completos
        filas = []

        for d in datos:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d.get("identificador","")), color=self.TEXT)),

                        ft.DataCell(
                            ft.Row([
                                self.obtener_icono_tipo(d.get("tipo")),
                                ft.Text(str(d.get("nombre","")), color=self.TEXT)
                            ], spacing=6)
                        ),

                        ft.DataCell(ft.Text(d.get("fecha", ""), color=self.GRIS_TEXTO)),
                        ft.DataCell(ft.Text(d.get("entrada", ""), color=self.GRIS_TEXTO)),
                        ft.DataCell(ft.Text(d.get("salida", ""), color=self.GRIS_TEXTO)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.VISIBILITY,
                                icon_color=self.AZUL,
                                tooltip="Ver detalles",
                                on_click=lambda e, d=d: self.ver_detalles(d)
                            )
                        )
                    ]
                )
            )

        tabla = ft.DataTable(
            expand=True,
            column_spacing=45,
            heading_row_height=55,
            horizontal_lines=ft.border.BorderSide(1, self.GRIS_BORDE),
            heading_row_color=self.FONDO_HEADER,
            columns=[
                ft.DataColumn(ft.Text("ID", weight="bold", color=self.TEXT)),
                ft.DataColumn(ft.Text("Nombre completo", weight="bold", color=self.TEXT)),
                ft.DataColumn(ft.Text("Fecha", weight="bold", color=self.TEXT)),
                ft.DataColumn(ft.Text("Entrada", weight="bold", color=self.TEXT)),
                ft.DataColumn(ft.Text("Salida", weight="bold", color=self.TEXT)),
                ft.DataColumn(ft.Text("Acciones", weight="bold", color=self.TEXT)),
            ],
            rows=filas
        )
        self.tabla_container.controls = [
            ft.Row(
                [tabla],
                expand=True
            )
        ]
        self.footer_tabla.controls = [
            ft.Text(
                f"Mostrando {len(datos)} de {self.total_registros} registros encontrados",
                size=14,
                color=self.GRIS_TEXTO
            ),
            self.construir_paginacion()
        ]
        self.update()
        
    def obtener_icono_tipo(self, tipo):
        if tipo == "ALUMNO":
            return ft.Container(
                content=ft.Icon(ft.Icons.SCHOOL, color=self.AZUL, size=16),
                tooltip="Alumno"
            )
        elif tipo == "PERSONAL":
            return ft.Container(
                content=ft.Icon(ft.Icons.BADGE, color=self.VERDE, size=16),
                tooltip="Personal"
            )
        elif tipo == "VISITANTE":
            return ft.Container(
                content=ft.Icon(ft.Icons.PERSON, color=self.NARANJA, size=16),
                tooltip="Visitante"
            )
        else:
            return ft.Container(
                content=ft.Icon(ft.Icons.HELP_OUTLINE, size=16),
                tooltip="Desconocido"
            )
        
    def _input_focus(self, e):
        e.control.value = ""
        e.control.color = self.TEXT
        self.update()

    def _input_blur(self, e):
        if not e.control.value:
            e.control.value = str(self.pagina_actual)
            e.control.color = self.GRIS_TEXTO
        self.update()

    def construir_paginacion(self):
        total_paginas = max(
            1,
            (self.total_registros // self.registros_por_pagina) +
            (1 if self.total_registros % self.registros_por_pagina else 0)
        )

        def cambiar_pagina(nueva):
            if 1 <= nueva <= total_paginas:
                self.pagina_actual = nueva
                self.filtrar()

        input_pagina = ft.TextField(
            width=60,
            height=35,
            text_align=ft.TextAlign.CENTER,
            value=str(self.pagina_actual),
            border_radius=8,
            color=self.GRIS_TEXTO,
            content_padding=5, 
            on_focus=lambda e: self._input_focus(e),
            on_blur=lambda e: self._input_blur(e),
            on_submit=lambda e: cambiar_pagina(
                int(e.control.value) if e.control.value.isdigit() else self.pagina_actual
            )
        )

        botones = []

        botones.append(ft.IconButton(ft.Icons.FIRST_PAGE, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(1)))
        botones.append(ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(self.pagina_actual - 1)))

        rango = 2
        paginas = []

        if total_paginas <= 7:
            paginas = list(range(1, total_paginas + 1))
        else:
            paginas = [1]
            if self.pagina_actual > 3:
                paginas.append("...")

            inicio = max(2, self.pagina_actual - rango)
            fin = min(total_paginas - 1, self.pagina_actual + rango)

            for i in range(inicio, fin + 1):
                paginas.append(i)

            if self.pagina_actual < total_paginas - 2:
                paginas.append("...")

            paginas.append(total_paginas)

        for p in paginas:
            if p == "...":
                botones.append(ft.Text("...", color=self.TEXT))
            else:
                botones.append(
                    ft.TextButton(
                        content=ft.Text(str(p)),
                        on_click=lambda e, p=p: cambiar_pagina(p),
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL if p == self.pagina_actual else "transparent",
                            color="white" if p == self.pagina_actual else self.TEXT
                        )
                    )
                )

        botones.append(ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(self.pagina_actual + 1)))
        botones.append(ft.IconButton(ft.Icons.LAST_PAGE, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(total_paginas)))

        botones.append(input_pagina)

        return ft.Row(botones, spacing=5)
    
    def actualizar(self):
        self.filtrar()

    def build_ui(self):
        fila_superior = ft.Row([
            ft.Container(self.input_busqueda, expand=2),
            ft.Container(self.build_boton_fecha(self.txt_fecha_inicio, self.fecha_inicio_picker), expand=1),
            ft.Container(self.build_boton_fecha(self.txt_fecha_fin, self.fecha_fin_picker), expand=1),
        ], spacing=10)

        fila_inferior = ft.Row([
            self.combo_tipo,
            self.combo_estado,
            self.export_container, 
            self.card_hoy
        ], spacing=10)

        filtros_panel = ft.Container(
            bgcolor=self.CARD,
            border_radius=20,
            padding=10,
            width=float('inf'),
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column([fila_superior, fila_inferior], spacing=5)
        )

        # Panel de tabla con ancho completo
        tabla_panel = ft.Container(
            expand=True,
            height=520,
            bgcolor=self.CARD,
            border_radius=20,
            padding=15,
            width=float('inf'),
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=self.tabla_container
        )

        footer_panel = ft.Container(
            padding=ft.padding.symmetric(horizontal=5),
            content=self.footer_tabla
        )

        self.content = ft.Column([
            ft.Row(
                [
                    ft.Column([
                        ft.Text("Historial de asistencias", size=28, weight="bold", color=self.TEXT),
                        ft.Text("Sistema de control digital - Registro de asistencias", color=self.GRIS_TEXTO, size=13),
                    ], spacing=2),
                    self.btn_limpiar
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),

            filtros_panel,
            tabla_panel,
            footer_panel  
        ], spacing=15, expand=True)
    
    def crear_badge_icono(self, icono, color_icono, color_fondo, titulo, valor):
        return ft.Row([
            ft.Container(
                content=ft.Icon(icono, color=color_icono, size=18),
                bgcolor=color_fondo,
                padding=8,
                border_radius=8
            ),
            ft.Container(
                width=160, # <-- Limitamos el ancho para evitar que rompa el diseño
                content=ft.Column([
                    ft.Text(titulo, size=11, color=self.GRIS_TEXTO, weight="w500"),
                    ft.Text(
                        valor, size=13, weight="bold", color=self.TEXT
                    ),
                ], spacing=2)
            )
        ], spacing=10)

    def ver_detalles(self, d):

        registro = next(
            (x for x in self.datos_completos 
            if x["identificador"] == d["identificador"]),
            None
        )

        if not registro:
            return

        nombre = str(registro.get("nombre_completo", "Desconocido"))
        identificador = str(registro.get("identificador", "N/A"))
        tipo = str(registro.get("tipo", "ALUMNO")).upper()

        fecha = registro["fecha_entrada"].strftime("%Y-%m-%d")
        entrada = registro["fecha_entrada"].strftime("%H:%M:%S")

        salida = (
            registro["fecha_salida"].strftime("%H:%M:%S")
            if registro["fecha_salida"]
            else ""
        )

        semestre = str(registro.get("semestre") or "N/A")
        grupo = str(registro.get("grupo") or "N/A")
        carrera = str(registro.get("carrera") or "N/A")
        n_plaza = str(registro.get("n_plaza") or "N/A")
        institucion = str(registro.get("institucion") or "N/A")

        badges_dinamicos = []
        
        if tipo == "ALUMNO":
            badges_dinamicos.append(self.crear_badge_icono(ft.Icons.HEXAGON_OUTLINED, "#8B5CF6", "transparent", "Semestre:", semestre))
            badges_dinamicos.append(self.crear_badge_icono(ft.Icons.PEOPLE_ALT_OUTLINED, self.VERDE, "transparent", "Grupo:", grupo))
            badges_dinamicos.append(self.crear_badge_icono(ft.Icons.SCHOOL_OUTLINED, self.AZUL, "transparent", "Carrera:", carrera))
        elif tipo == "PERSONAL":
            badges_dinamicos.append(self.crear_badge_icono(ft.Icons.BADGE_OUTLINED, self.VERDE, "transparent", "No. Plaza:", n_plaza))
        elif tipo == "VISITANTE":
            badges_dinamicos.append(self.crear_badge_icono(ft.Icons.ACCOUNT_BALANCE_OUTLINED, self.NARANJA, "transparent", "Institución:", institucion))

        en_curso = (salida == "" or salida == "-" or salida == "None")

        color_estado = self.NARANJA if en_curso else self.VERDE
        bg_estado = "transparent"
        borde_estado = color_estado
        texto_estado_h1 = "EN CURSO" if en_curso else "FINALIZADO"
        texto_estado_h2 = "El usuario aún no ha registrado su salida en la biblioteca." if en_curso else "El usuario registró su salida correctamente."
        icono_estado = ft.Icons.ACCESS_TIME if en_curso else ft.Icons.CHECK_CIRCLE

        seccion_perfil = ft.Container(
            bgcolor="surfaceVariant", border_radius=15, padding=20,
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PERSON, size=50, color="surface"),
                        bgcolor="#3B82F6", width=80, height=80, border_radius=40, alignment=ft.Alignment(0, 0)
                    ),
                    ft.Column([
                        ft.Text(nombre, size=20, weight="bold", color=self.TEXT),
                        ft.Text(f"ID: {identificador}", size=13, color=self.GRIS_TEXTO),
                        ft.Container(
                            content=ft.Row([ft.Icon(ft.Icons.SCHOOL if tipo == "ALUMNO" else ft.Icons.BADGE, size=14, color="#2563EB"), ft.Text(tipo, size=12, weight="bold", color="#2563EB")], spacing=5),
                            bgcolor="transparent", border=ft.border.all(1, self.AZUL), padding=ft.padding.symmetric(horizontal=10, vertical=5), border_radius=15
                        )
                    ], spacing=5, expand=True)
                ], expand=True),
                ft.Container(width=1, height=80, bgcolor=self.GRIS_BORDE),
                ft.Column(badges_dinamicos, spacing=10, expand=True)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        if en_curso:
            ui_salida = ft.Container(
                width=160,
                content=ft.Column([
                    ft.Row([
                        ft.Container(content=ft.Icon(ft.Icons.LOGOUT, color=self.ROJO, size=18), bgcolor="transparent", border=ft.border.all(1, self.ROJO), padding=8, border_radius=8),
                        ft.Text("Hora de Salida\n-", size=12, color=self.GRIS_TEXTO)
                    ]),
                    ft.Container(content=ft.Text("Sin salida registrada", color=self.ROJO, size=11, weight="bold"), bgcolor="transparent", border=ft.border.all(1, self.ROJO), padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=10)
                ])
            )
        else:
            ui_salida = self.crear_badge_icono(ft.Icons.LOGOUT, self.ROJO, "transparent", "Hora de Salida", salida)

        seccion_tiempos = ft.Container(
            border=ft.border.all(1, self.GRIS_BORDE), border_radius=15, padding=20,
            content=ft.Row([
                self.crear_badge_icono(ft.Icons.CALENDAR_TODAY, self.AZUL, "transparent", "Fecha", fecha),
                ft.Container(width=1, height=40, bgcolor=self.GRIS_BORDE),
                self.crear_badge_icono(ft.Icons.LOGIN, self.VERDE, "transparent", "Hora de Entrada", entrada),
                ft.Container(width=1, height=40, bgcolor=self.GRIS_BORDE),
                ui_salida
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        seccion_estado = ft.Container(
            bgcolor=bg_estado, border=ft.border.all(1, borde_estado), border_radius=15, padding=20,
            content=ft.Row([
                ft.Row([
                    ft.Icon(icono_estado, color=color_estado, size=30),
                    ft.Column([
                        ft.Text("Estado actual", size=12, color=self.GRIS_TEXTO),
                        ft.Text(texto_estado_h1, size=18, weight="bold", color=color_estado)
                    ], spacing=0)
                ], expand=1),
                ft.Container(width=1, height=40, bgcolor=borde_estado),
                ft.Container(
                    content=ft.Text(texto_estado_h2, size=13, color=self.TEXT),
                    expand=2, padding=ft.padding.only(left=20)
                )
            ])
        )

        def cerrar_dialogo(e):
            dialogo.open = False
            self._page.update()

        dialogo = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=self.CARD,
            title=ft.Row([
                ft.Text("Detalles de Asistencia", weight="bold", size=22, color=self.TEXT),
                ft.IconButton(ft.Icons.CLOSE, on_click=cerrar_dialogo)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Container(
                width=720, # <-- Le damos un poquito más de aire al modal para que quepan todos los detalles perfectos
                content=ft.Column([seccion_perfil, seccion_tiempos, seccion_estado], tight=True, spacing=20)
            ),
            actions=[
                ft.ElevatedButton(
                    "Cerrar", icon=ft.Icons.CHECK,
                    bgcolor="#2563EB", color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=20),
                    on_click=cerrar_dialogo
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=ft.padding.only(right=20, bottom=20)
        )

        self._page.overlay.append(dialogo)
        dialogo.open = True
        self._page.update()
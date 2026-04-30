import flet as ft
from datetime import datetime

class PantallaHistorial(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # Propiedades del Contenedor Principal
        self.expand = True
        self.padding = 30
        self.bgcolor = "#EAF1F7"
        self.border_radius = 30

        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.TEXTO_TITULO = "#111827"
        self.TEXTO_TABLA = "#000000" 
        self.BORDE = "#D1D5DB"

        # ===== CONTROLES DINÁMICOS =====
        self.txt_fecha_inicio = ft.Text("Fecha inicio", color=self.TEXTO_TITULO)
        self.txt_fecha_fin = ft.Text("Fecha fin", color=self.TEXTO_TITULO)

        self.fecha_inicio_picker = ft.DatePicker(on_change=self.seleccionar_inicio)
        self.fecha_fin_picker = ft.DatePicker(on_change=self.seleccionar_fin)
        self._page.overlay.extend([self.fecha_inicio_picker, self.fecha_fin_picker])

        self.input_busqueda = ft.TextField(
            label="Buscar por identificador o nombre...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=12,
            border_color=self.BORDE,
            focused_border_color=self.AZUL,
            bgcolor="white",
            on_change=self.filtrar, # TextField suele aceptar on_change, si falla, muévelo abajo igual que el dropdown
            text_style=ft.TextStyle(color=self.TEXTO_TITULO),
            label_style=ft.TextStyle(color="black"),
        )
        
# DROPDOWN TIPO
        self.combo_tipo = ft.Dropdown(
            expand=True,
            label="Tipo de usuario",
            border_color=self.BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="black",
            color="black",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Alumno"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitante"),
            ],
            value="Todos"
        )
        self.combo_tipo.on_change = self.filtrar

        # DROPDOWN ESTADO
        self.combo_estado = ft.Dropdown(
            expand=True,
            label="Estado",
            border_color=self.BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="black",
            color="black",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Activos"),
                ft.dropdown.Option("Finalizados"),
            ],
            value="Todos"
        )
        self.combo_estado.on_change = self.filtrar


        # BOTÓN EXPORTAR
        self.btn_exportar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, color="#10B981"),
                ft.Text("Exportar a Excel", color="#10B981", weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER),
            border=ft.border.all(1, "#10B981"),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=15),
            height=45,
            expand=True,
        )

        # CARD HOY
        self.card_hoy = ft.Container(
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            bgcolor="white",
            border_radius=20,
            border=ft.border.all(1, self.BORDE),
            expand=True,
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.PEOPLE_ALT_ROUNDED, color="white", size=20),
                    bgcolor="black",
                    padding=8,
                    border_radius=12
                ),
                ft.Column([
                    ft.Text("Usuarios totales hoy", size=10, color="grey"),
                    ft.Text("37", size=18, weight="bold", color="black"),
                    ft.Text("Registrados hoy", size=9, color="grey")
                ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=10)
        )

        self.tabla_container = ft.Column(scroll="auto", expand=True)

        self.build_ui()
        self.filtrar() 

    # ===== LÓGICA =====
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
            height=45,
            border=ft.border.all(1, self.BORDE),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12),
            bgcolor="white",
            on_click=lambda e: self.abrir_picker(e, picker),
            content=ft.Row(
                [ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=self.AZUL), texto_ref],
                spacing=10
            )
        )

    def filtrar(self, e=None):
        # Mantenemos tu lógica de filtrado...
        try:
            from Negocio.Controlador.ControladorHistorial import ControladorHistorial
            control = ControladorHistorial()
            datos = control.obtener_historial()
        except:
            datos = [] 
        
        texto = self.input_busqueda.value.lower() if self.input_busqueda.value else ""
        filas = []

        for d in datos:
            if texto and texto not in str(d.get("identificador","")).lower() and texto not in str(d.get("nombre","")).lower():
                continue
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d.get("identificador","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("nombre","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("fecha","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("entrada","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("salida","")), color=self.TEXTO_TABLA)),
                    ]
                )
            )

        tabla = ft.DataTable(
            expand=True,
            horizontal_lines=ft.border.BorderSide(1, "#F3F4F6"),
            columns=[
                ft.DataColumn(ft.Text("Identificador", weight="bold", color=self.TEXTO_TABLA)),
                ft.DataColumn(ft.Text("Nombre completo", weight="bold", color=self.TEXTO_TABLA)),
                ft.DataColumn(ft.Text("Fecha", weight="bold", color=self.TEXTO_TABLA)),
                ft.DataColumn(ft.Text("Hora entrada", weight="bold", color=self.TEXTO_TABLA)),
                ft.DataColumn(ft.Text("Hora salida", weight="bold", color=self.TEXTO_TABLA)),
            ],
            rows=filas,
        )

        self.tabla_container.controls.clear()
        self.tabla_container.controls.append(ft.Row([tabla], scroll="auto", expand=True))
        if e: self.update()

    def build_ui(self):
        fila_superior = ft.Row([
            ft.Container(self.input_busqueda, expand=2),
            ft.Container(self.build_boton_fecha(self.txt_fecha_inicio, self.fecha_inicio_picker), expand=1),
            ft.Container(self.build_boton_fecha(self.txt_fecha_fin, self.fecha_fin_picker), expand=1),
        ], spacing=10)

        fila_inferior = ft.Row([
            self.combo_tipo,
            self.combo_estado,
            self.btn_exportar,
            self.card_hoy
        ], spacing=10)

        filtros_panel = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column([fila_superior, fila_inferior], spacing=15)
        )

        tabla_panel = ft.Container(
            expand=True,
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=self.tabla_container
        )

        self.content = ft.Column([
            ft.Column([
                ft.Text("Historial de asistencias", size=28, weight="bold", color=self.TEXTO_TITULO),
                ft.Text("Sistema de control digital - Registro de asistencias", color="black", size=13),
            ], spacing=2),
            filtros_panel,
            tabla_panel
        ], spacing=15, expand=True)
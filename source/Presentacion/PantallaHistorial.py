import flet as ft
from datetime import datetime

class PantallaHistorial(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # Propiedades del Contenedor Principal (Fondo de la vista)
        self.expand = True
        self.padding = 30
        self.bgcolor = "#EAF1F7"
        self.border_radius = 30

        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.TEXTO = "#111827"
        self.BORDE = "#E5E7EB"

        # ===== CONTROLES DINÁMICOS =====
        self.txt_fecha_inicio = ft.Text("Fecha inicio", color="#111827")
        self.txt_fecha_fin = ft.Text("Fecha fin", color="#111827")

        self.fecha_inicio_picker = ft.DatePicker(on_change=self.seleccionar_inicio)
        self.fecha_fin_picker = ft.DatePicker(on_change=self.seleccionar_fin)

        # Los DatePickers necesitan aagregarse al overlay de la página principal
        self._page.overlay.extend([self.fecha_inicio_picker, self.fecha_fin_picker])

        self.input_busqueda = ft.TextField(
            hint_text="Buscar por identificador o nombre...",
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            border_radius=12,
            on_change=self.filtrar,

            text_style=ft.TextStyle(color=self.TEXTO),
            hint_style=ft.TextStyle(color="9CA3AF"),
        )

        self.tabla_container = ft.Column(scroll="auto", expand=True)

        # Construir UI y dibujar la tabla vacía inicial
        self.build_ui()
        self.filtrar() 

    # ===== VALIDACIONES Y LÓGICA DE PICKERS =====
    def fecha_valida(self, fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

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

    def abrir_picker(self, picker):
        picker.open = True
        self._page.update()  # Los overlays necesitan que la página completa se actualice

    # ===== WIDGETS REUTILIZABLES =====
    def build_boton_fecha(self, texto_ref, picker):
        return ft.Container(
            width=170,
            height=45,
            border=ft.border.all(1, self.BORDE),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12),
            bgcolor="white",
            on_click=lambda e: self.abrir_picker(picker),
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=self.AZUL),
                    texto_ref
                ],
                spacing=10
            )
        )


    # ===== FILTROS Y TABLA =====
    def filtrar(self, e=None):
        from Negocio.Controlador.ControladorHistorial import ControladorHistorial

        control = ControladorHistorial()
        datos = control.obtener_historial()

        texto = self.input_busqueda.value.lower() if self.input_busqueda.value else ""

        fecha_inicio = self.txt_fecha_inicio.value
        fecha_fin = self.txt_fecha_fin.value

        filas = []

        for d in datos:

            # 🔍 FILTRO TEXTO
            if texto:
                if texto not in d["identificador"].lower() and texto not in d["nombre"].lower():
                    continue

            #  FILTRO FECHAS
            if self.fecha_valida(fecha_inicio) and d["fecha"] < fecha_inicio:
                continue

            if self.fecha_valida(fecha_fin) and d["fecha"] > fecha_fin:
                continue

            # FORMATO HORAS
            
            entrada = d["entrada"] if d["entrada"] else "-"
            salida = d["salida"] if d["salida"] != "-" else "-"

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(d["identificador"], color=self.TEXTO)),
                        ft.DataCell(ft.Text(d["nombre"], color=self.TEXTO)),
                        ft.DataCell(ft.Text(d["fecha"], color=self.TEXTO)),
                        ft.DataCell(ft.Text(entrada, color=self.TEXTO)),
                        ft.DataCell(ft.Text(salida, color=self.TEXTO)),
                    ]
                )
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Identificador", weight="bold", color=self.TEXTO)),
                ft.DataColumn(ft.Text("Nombre completo", weight="bold", color=self.TEXTO)),
                ft.DataColumn(ft.Text("Fecha", weight="bold", color=self.TEXTO)),
                ft.DataColumn(ft.Text("Hora entrada", weight="bold", color=self.TEXTO)),
                ft.DataColumn(ft.Text("Hora salida", weight="bold", color=self.TEXTO)),
            ],
            rows=filas,
            heading_row_color="#F3F4F6",
            data_text_style=ft.TextStyle(color="#000000"),
        )

        self.tabla_container.controls.clear()
        self.tabla_container.controls.append(tabla)

        if e is not None:
            self.update()

    def limpiar(self, e):
        self.input_busqueda.value = ""
        self.txt_fecha_inicio.value = "Fecha inicio"
        self.txt_fecha_fin.value = "Fecha fin"
        self.filtrar()
        self.update()

    def actualizar(self):
        self.filtrar()

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        fecha_inicio_btn = self.build_boton_fecha(self.txt_fecha_inicio, self.fecha_inicio_picker)
        fecha_fin_btn = self.build_boton_fecha(self.txt_fecha_fin, self.fecha_fin_picker)

        filtros = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.input_busqueda,
                    fecha_inicio_btn,
                    fecha_fin_btn,
                    ft.IconButton(
                        icon=ft.Icons.CLEAR,
                        tooltip="Limpiar",
                        on_click=self.limpiar
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
            content=self.tabla_container
        )

        self.content = ft.Column(
            [
                ft.Column(
                    [
                        ft.Text("Historial de asistencias", size=32, weight="bold", color=self.TEXTO),
                        ft.Text("Sistema de control digital - Registro de asistencias", color=self.TEXTO),
                    ],
                    spacing=5
                ),
                filtros,
                tabla_scroll
            ],
            spacing=20,
            expand=True
        )
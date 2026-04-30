import flet as ft
from datetime import datetime
from Negocio.Controlador.ControladorHistorial import ControladorHistorial

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
        self.TEXTO_HEADER = "#111827"
        self.FONDO_HEADER = "#F3F4F6"  

        # ===== CONTROLES DINÁMICOS =====
        self.txt_fecha_inicio = ft.Text("Fecha inicio", color=self.TEXTO_TITULO)
        self.txt_fecha_fin = ft.Text("Fecha fin", color=self.TEXTO_TITULO)

        self.fecha_inicio_picker = ft.DatePicker(on_change=self.seleccionar_inicio)
        self.fecha_fin_picker = ft.DatePicker(on_change=self.seleccionar_fin)
        self._page.overlay.extend([self.fecha_inicio_picker, self.fecha_fin_picker])

        self.btn_limpiar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CLEAR, color="white", size=18),
                ft.Text("Limpiar filtros", color="white", size=12, weight="w500")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            bgcolor="#EF4444",  # rojo suave moderno
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=10,
            on_click=self.limpiar_filtros
        )

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
            value="Todos",
            on_select=self.filtrar
        )

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
            value="Todos",
            on_select=self.filtrar
        )


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

        self.txt_hoy = ft.Text("0", size=18, weight="bold", color="black")
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
                    ft.Text("Usuarios únicos hoy", size=10, color="grey"),
                    self.txt_hoy,
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

    def limpiar_filtros(self, e=None):
        # Reset valores
        self.input_busqueda.value = ""
        self.txt_fecha_inicio.value = "Fecha inicio"
        self.txt_fecha_fin.value = "Fecha fin"
        self.combo_tipo.value = "Todos"
        self.combo_estado.value = "Todos"

        # Refrescar filtros
        self.filtrar()

        if self.page:
            self.update()    


    def filtrar(self, e=None):
        try:
            control = ControladorHistorial()
            datos = control.obtener_historial(
                texto=self.input_busqueda.value or "",
                fecha_inicio=self.txt_fecha_inicio.value if self.txt_fecha_inicio.value != "Fecha inicio" else None,
                fecha_fin=self.txt_fecha_fin.value if self.txt_fecha_fin.value != "Fecha fin" else None,
                tipo=self.combo_tipo.value,
                estado=self.combo_estado.value
            )

            try:
                total_hoy = control.contar_hoy()
                self.txt_hoy.value = str(total_hoy)
            except:
                self.txt_hoy.value = "0"

        except:
            datos = [] 
            self.txt_hoy.value = "0"
        filas = []

        for d in datos:
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(d.get("identificador","")), color=self.TEXTO_TABLA)),
                        # El nombre ahora se adapta, no se impone
                        ft.DataCell(ft.Text(str(d.get("nombre","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("fecha","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("entrada","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(ft.Text(str(d.get("salida","")), color=self.TEXTO_TABLA)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.VISIBILITY_ROUNDED,
                                icon_color=self.AZUL,
                                icon_size=20,
                                on_click=lambda _: print("Ver detalles")
                            )
                        ),
                    ]
                )
            )

        # La clave es 'expand=True' en la tabla y en la columna específica
        tabla = ft.DataTable(
            expand=True, 
            horizontal_lines=ft.border.BorderSide(1, "#E5E7EB"),
            column_spacing=45, # Aumentamos espacio para que respiren las columnas fijas
            heading_row_color=self.FONDO_HEADER,
            heading_row_height=50,
            columns=[
                ft.DataColumn(ft.Text("ID", weight="bold", color=self.TEXTO_HEADER)),
                # Esta columna es la que "empuja" a las demás a los bordes
                ft.DataColumn(
                    ft.Text("Nombre completo", weight="bold", color=self.TEXTO_HEADER),
                    on_sort=lambda e: print("Sort"), # Opcional: ayuda a definir la columna
                ),
                ft.DataColumn(ft.Text("Fecha", weight="bold", color=self.TEXTO_HEADER)),
                ft.DataColumn(ft.Text("Entrada", weight="bold", color=self.TEXTO_HEADER)),
                ft.DataColumn(ft.Text("Salida", weight="bold", color=self.TEXTO_HEADER)),
                ft.DataColumn(ft.Text("Acción", weight="bold", color=self.TEXTO_HEADER)),
            ],
            rows=filas,
        )

        self.tabla_container.controls.clear()
        
        # El contenedor DEBE tener expand=True para que la tabla sepa cuánto espacio hay
        self.tabla_container.controls.append(
            ft.Row(
                controls=[tabla],
                expand=True, # Obliga a la fila a usar todo el ancho del panel blanco
            )
        )
        if e: self.update()
        
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
            self.btn_exportar,
            self.card_hoy
        ], spacing=10)

        # Panel de filtros con ancho completo
        filtros_panel = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=20,
            width=float('inf'), # Forzamos ancho infinito (máximo permitido)
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Column([fila_superior, fila_inferior], spacing=15)
        )

        # Panel de tabla con ancho completo
        tabla_panel = ft.Container(
            expand=True,
            bgcolor="white",
            border_radius=20,
            padding=15,
            width=float('inf'), # Forzamos ancho infinito para que coincida con el de arriba
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=self.tabla_container
        )

        self.content = ft.Column([
            ft.Row(
                [
                    ft.Column([
                        ft.Text("Historial de asistencias", size=28, weight="bold", color=self.TEXTO_TITULO),
                        ft.Text("Sistema de control digital - Registro de asistencias", color="black", size=13),
                    ], spacing=2),
                    
                    self.btn_limpiar
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            filtros_panel,
            tabla_panel
        ], spacing=15, expand=True)
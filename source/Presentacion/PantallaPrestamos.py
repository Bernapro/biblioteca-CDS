import flet as ft
from Presentacion.PantallaNuevoPrestamo import PantallaNuevoPrestamo
from Negocio.Controlador.ControladorPrestamos import ControladorPrestamos

class PantallaPrestamos(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # Instanciamos el controlador
        self.controlador = ControladorPrestamos(self)
        
        # ===== COLORES =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#10B981" 
        self.ROJO = "#EF4444"
        self.NARANJA = "#F59E0B"
        self.FONDO = "transparent" 
        self.GRIS_TEXTO = "onSurfaceVariant"
        self.GRIS_BORDE = "outline"
        self.TEXT = "onSurface"
        self.CARD = "surface"

        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        self.build_ui()

    #TARJETAS
    def build_card_stat(self, titulo, valor, sub_valor, icono, color):
        color_fondo = color.replace("#", "#20")
        return ft.Container(
            expand=True,
            bgcolor=self.CARD,
            padding=20,
            border_radius=15,
            border=ft.border.all(1, self.GRIS_BORDE),
            content=ft.Row([
                # Icono arriba
                ft.Container(
                    content=ft.Icon(icono, color=color, size=28),
                    bgcolor=color_fondo,
                    width=60, height=60,
                    border_radius=30,
                    alignment=ft.Alignment(0, 0)
                ),
                # Textos
                ft.Column([
                    ft.Text(titulo, size=13, color=self.GRIS_TEXTO, weight="w500"),
                    ft.Text(valor, size=26, weight="bold", color=self.TEXT),
                    ft.Text(sub_valor, size=11, color=self.GRIS_TEXTO),
                ], spacing=2)
            ], spacing=15, alignment=ft.MainAxisAlignment.START)
        )

    
    # ===== BADGE DE ESTADO =====
    def build_estado(self, estado):
        #  colores del texto
        color_texto = self.VERDE if estado == "A tiempo" else self.ROJO
        icono = ft.Icons.CHECK_CIRCLE if estado == "A tiempo" else ft.Icons.CANCEL
        
        # DEFINIMOS EL COLOR DE RELLENO (FONDO) AQUÍ
        color_fondo = "#DCFCE7" if estado == "A tiempo" else "#FEE2E2" # Cambia "#FEE2E2" por el color que más te guste

        return ft.Container(
            content=ft.Row([
                ft.Icon(icono, color=color_texto, size=14),
                ft.Text(estado, color=color_texto, weight="bold", size=12)
            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=color_fondo,  # <--- Aquí aplicamos el color de relleno
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border_radius=15,
            width=110
        )

    # ===== BOTONES DE ACCIÓN =====
    def build_btn_accion(self, texto, icono, color):
        return ft.OutlinedButton(
            texto,
            icon=icono,
            style=ft.ButtonStyle(
                color=color,
                shape=ft.RoundedRectangleBorder(radius=8),
                side=ft.BorderSide(1, color),
                padding=ft.padding.symmetric(horizontal=15, vertical=10)
            ),
            height=35
        )

    # FILAS DE LA TABLA 
    def build_row(self, data):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(data["matricula"], color=self.GRIS_TEXTO, size=15)),
                ft.DataCell(
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=20, color=self.AZUL),
                        ft.Text(data["nombre"], color=self.TEXT, size=15)
                    ], spacing=10)
                ),
                ft.DataCell(
                    ft.Row([
                        ft.Icon(ft.Icons.MENU_BOOK, size=20, color=self.AZUL if data["estado"] == "A tiempo" else self.ROJO),
                        ft.Text(data["libro"], color=self.TEXT, size=15)
                    ], spacing=10)
                ),
                ft.DataCell(self.build_estado(data["estado"])),
                ft.DataCell(ft.Text(data["fecha_prestamo"], color=self.GRIS_TEXTO, size=15)),
                ft.DataCell(ft.Text(data["fecha_limite"], color=self.GRIS_TEXTO, size=15)),
                ft.DataCell(
                    ft.Row([
                        self.build_btn_accion("Extender", ft.Icons.CALENDAR_MONTH, self.AZUL),
                        self.build_btn_accion("Devolver", ft.Icons.KEYBOARD_RETURN, self.VERDE),
                        ft.IconButton(icon=ft.Icons.MORE_VERT, icon_color=self.GRIS_TEXTO)
                    ], spacing=10)
                ),
            ]
        )

    # ===== LÓGICA DE NAVEGACIÓN =====
    def ir_a_nuevo_prestamo(self, e):
        self.content = PantallaNuevoPrestamo(self._page, vista_anterior=self)
        self.update()

    def cargar_datos(self, e=None):
        # Obtenemos los datos desde el controlador y llenamos las filas
        datos = self.controlador.obtener_prestamos()
        self.tabla.rows = [self.build_row(data) for data in datos]
        
        # También actualizamos las tarjetas de resumen dinámicamente
        if hasattr(self, 'resumen'):
            stats = self.controlador.obtener_estadisticas()
            self.resumen.controls = [
                self.build_card_stat("Total préstamos", stats["total"], "Registros totales", ft.Icons.MENU_BOOK_ROUNDED, self.AZUL),
                self.build_card_stat("A tiempo", stats["a_tiempo"], "Préstamos vigentes", ft.Icons.CHECK_CIRCLE_OUTLINE, self.VERDE),
                self.build_card_stat("Atrasados", stats["atrasados"], "Préstamos vencidos", ft.Icons.ACCESS_TIME, self.ROJO),
                self.build_card_stat("Por vencer", stats["por_vencer"], "Próximos 3 días", ft.Icons.CALENDAR_MONTH, self.NARANJA),
            ]
            
        if e:
            self.update()

    # Función detectada por PantallaPrincipal para refrescar al entrar a la vista
    def actualizar(self):
        self.cargar_datos()

    # ===== CONSTRUCCIÓN PRINCIPAL =====
    def build_ui(self):
        # 1. Encabezado y botón nuevo préstamo
        encabezado = ft.Row([
            ft.Column([
                ft.Text("Préstamos de libros", size=28, weight="bold", color=self.TEXT),
                ft.Text("Busca y gestiona los préstamos de libros registrados en el sistema.", size=14, color=self.GRIS_TEXTO)
            ], spacing=5),
            ft.ElevatedButton(
                "+ Nuevo préstamo",
                style=ft.ButtonStyle(
                    bgcolor=self.AZUL, color="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=15)
                ),
                height=45,
                on_click=self.ir_a_nuevo_prestamo
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # 2. Filtros (Barra de búsqueda y dropdown estilo píldora)
        filtros = ft.Row([
            ft.Container(
                expand=True,
                content=ft.TextField(
                    hint_text="Buscar por matrícula, nombre o libro...",
                    prefix_icon=ft.Icons.SEARCH, border=ft.InputBorder.NONE, content_padding=15
                ),
                bgcolor=self.CARD, border_radius=10, border=ft.border.all(1, self.GRIS_BORDE)
            ),
            ft.Container(
                width=200,
                content=ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("A tiempo"),
                        ft.dropdown.Option("Atrasado"),
                    ],
                    border=ft.InputBorder.NONE, content_padding=15, hint_text="Estado: Todos"
                ),
                bgcolor=self.CARD, border_radius=10, border=ft.border.all(1, self.GRIS_BORDE)
            ),
            ft.ElevatedButton(
                "Buscar", icon=ft.Icons.SEARCH,
                style=ft.ButtonStyle(bgcolor=self.AZUL, color="white", shape=ft.RoundedRectangleBorder(radius=10)),
                height=50
            )
        ], spacing=15)

        # 3. Tarjetas de Resumen (Se poblarán en cargar_datos)
        self.resumen = ft.Row([], spacing=15)

        # 4. Tabla
       
        self.tabla = ft.DataTable(
            expand=True,
            column_spacing=20,    # <-- Reducido para adaptarse a laptops y pantallas pequeñas
            horizontal_margin=15, # <-- Reducido para aprovechar mejor el espacio
            heading_row_color="surfaceVariant",
            heading_row_height=60,
            data_row_min_height=75, # <-- Filas más altas para la letra grande
            data_row_max_height=75,
            divider_thickness=1,
            columns=[
                ft.DataColumn(ft.Text("Matrícula", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Nombre", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Libro", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Estado", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Fecha préstamo", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Fecha límite", weight="bold", color=self.TEXT, size=15)),
                ft.DataColumn(ft.Text("Acciones", weight="bold", color=self.TEXT, size=15)),
            ],
            rows=[]
        )

        self.cargar_datos() # Poblar la tabla por primera vez

        contenedor_tabla = ft.Container(
            expand=True,
            bgcolor=self.CARD,
            border_radius=15,
            border=ft.border.all(1, self.GRIS_BORDE),
            content=ft.Column([
                ft.Row([self.tabla], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        )

        # 5. Paginación (Pie de tabla)
        paginacion = ft.Row([
            ft.Text("Mostrando 1-4 de 4 préstamos", color=self.GRIS_TEXTO, size=13),
            ft.Row([
                ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, icon_color=self.GRIS_TEXTO),
                ft.Container(content=ft.Text("1", color="white", weight="bold"), bgcolor=self.AZUL, padding=ft.padding.symmetric(horizontal=12, vertical=6), border_radius=6),
                ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, icon_color=self.GRIS_TEXTO),
            ], spacing=5)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Ensamblaje Final
        self.content = ft.Column(
            [encabezado, filtros, self.resumen, contenedor_tabla, paginacion],
            spacing=20,
            expand=True
        )
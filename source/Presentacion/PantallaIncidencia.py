import flet as ft

# IMPORTACIÓN DE LA NUEVA CLASE
# Asegúrate de que el nombre del archivo y la clase coincidan
from Presentacion.PantallaRegistroIncidencia import PantallaRegistroIncidencia

class PantallaIncidencias(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#22C55E"
        self.ROJO = "#EF4444"
        self.NARANJA = "#F59E0B" 
        self.TURQUESA = "#0F766E" 
        self.FONDO = "#EAF1F7"

        # Propiedades del Contenedor Principal
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== CONTROLES DINÁMICOS =====
        self.input_busqueda = ft.TextField(
            expand=True,
            hint_text="Buscar estudiante...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=15),
            text_style=ft.TextStyle(size=15)
        )

        self.dropdown_estado = ft.Dropdown(
            width=140,
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Resuelto"),
            ],
            value="Todos",
            border=ft.InputBorder.NONE,
            color="black",
            content_padding=ft.padding.symmetric(horizontal=10, vertical=15),
            text_style=ft.TextStyle(size=15, weight="w500")
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== BOTONES REUTILIZABLES =====
    def build_btn_resuelto(self):
        return ft.ElevatedButton(
            "Resuelto", height=40, 
            style=ft.ButtonStyle(bgcolor=self.VERDE, color="white", shape=ft.RoundedRectangleBorder(radius=8))
        )

    def build_btn_pendiente(self):
        return ft.ElevatedButton(
            "Pendiente", height=40, 
            style=ft.ButtonStyle(bgcolor=self.ROJO, color="white", shape=ft.RoundedRectangleBorder(radius=8))
        )

    def build_btn_detalles(self):
        return ft.OutlinedButton(
            "Ver detalles", height=40, 
            style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8))
        )

    # ===== CARD INCIDENCIA =====
    def build_card(self, nombre, matricula, razon, lugar, fecha, tipo="PARCIAL", estado="Pendiente"):
        color_borde = self.ROJO if tipo == "DEFINITIVA" else self.NARANJA
        icono_razon = ft.Icons.WARNING_AMBER_ROUNDED
        if "Ruido" in razon: icono_razon = ft.Icons.VOLUME_UP_ROUNDED
        elif "equipo" in razon: icono_razon = ft.Icons.COMPUTER_ROUNDED
        
        return ft.Container(
            bgcolor="white", border_radius=20, shadow=ft.BoxShadow(blur_radius=25, color="black12"), 
            content=ft.Row(
                controls=[
                    ft.Container(width=8, bgcolor=color_borde, border_radius=ft.border_radius.only(top_left=20, bottom_left=20)),
                    ft.Container(
                        expand=True, padding=15, 
                        content=ft.Row([
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, size=45, color=color_borde), 
                                ft.Column([
                                    ft.Text(nombre, weight="bold", size=16, color="black"),
                                    ft.Text(f"Matrícula: {matricula}", size=13, color="#4B5563"),
                                    ft.Text(f"Tipo: {tipo}", size=11, weight="bold", color=color_borde),
                                    ft.Row([ft.Icon(icono_razon, size=15, color="#6B7280"), ft.Text(razon, size=13, color="black")], spacing=5),
                                    ft.Text(f"Lugar: {lugar} | Fecha: {fecha}", size=12, color="#6B7280"),
                                ], spacing=4)
                            ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Row([
                                self.build_btn_resuelto() if estado == "Pendiente" else self.build_btn_pendiente(),
                                self.build_btn_detalles()
                            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
                ], spacing=0
            )
        )

    # ===== LÓGICA DE NAVEGACIÓN (CONEXIÓN) =====
    def ir_a_registro(self, e):
        # 1. Creamos la instancia de la pantalla de registro
        # Pasamos 'self' como vista_anterior para poder regresar
        # 2. Cambiamos el contenido de esta pantalla a la de Registro
        self.content = PantallaRegistroIncidencia(self._page, vista_anterior=self)
        # 3. Actualizamos la vista para mostrar el formulario
        self.update()

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        # --- Botón Nuevo ---
        btn_nueva_incidencia = ft.ElevatedButton(
            "NUEVA INCIDENCIA +",
            bgcolor=self.ROJO,
            color="white",
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(horizontal=25)),
            # CONEXIÓN AQUÍ
            on_click=self.ir_a_registro
        )

        encabezado = ft.Row([
            ft.Column([
                ft.Text("Gestión de Incidencias", size=32, weight="bold", color="black"),
                ft.Text("Busca y gestiona el catálogo de incidencias registradas en el sistema.", color="#4B5563")
            ]),
            btn_nueva_incidencia
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        filtros = ft.Container(
            bgcolor="white", border_radius=35, padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="black12", offset=ft.Offset(0, 4)),
            content=ft.Row([
                self.input_busqueda,
                ft.Container(width=1, height=30, bgcolor="#E5E7EB"),
                self.dropdown_estado,
                ft.ElevatedButton("Buscar", height=45, style=ft.ButtonStyle(bgcolor=self.AZUL, color="white", shape=ft.RoundedRectangleBorder(radius=25), padding=ft.padding.symmetric(horizontal=30)))
            ], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

        lista = ft.Column([
            self.build_card("Carlos Daniel", "100025787", "Ruido excesivo", "Cubículo 1", "24/Marzo/2026", "PARCIAL", "Pendiente"),
            self.build_card("Cruz Castillo", "100025788", "Uso indebido del equipo", "Cubículo 2", "25/Marzo/2026", "DEFINITIVA", "Resuelto"),
            self.build_card("Jose Angel", "ABCDEFGA", "Comportamiento inapropiado", "Cubículo 3", "26/Marzo/2026", "PARCIAL", "Pendiente"),
            self.build_card("Figueroa Sales", "ABCDEFGA", "Páginas arrancadas", "Área de lectura", "27/Marzo/2026", "DEFINITIVA", "Resuelto"),
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

        paginacion = ft.Row([
            ft.Text("1-10 de 100 incidencias", color="black"),
            ft.Row([ft.OutlinedButton("Anterior"), ft.OutlinedButton("Siguiente")], spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.content = ft.Column([encabezado, filtros, lista, paginacion], spacing=20, expand=True)
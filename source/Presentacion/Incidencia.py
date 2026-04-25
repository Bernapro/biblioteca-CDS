import flet as ft

class PantallaIncidencias(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#22C55E"
        self.ROJO = "#EF4444"
        self.FONDO = "#EAF1F7"

        # Propiedades del Contenedor Principal (Fondo de la vista)
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== CONTROLES DINÁMICOS (Para acceder a sus valores después) =====
        self.input_busqueda = ft.TextField(
            width=300,
            hint_text="Buscar por identificador o nombre...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            text_style=ft.TextStyle(color="black"),
        )

        self.dropdown_estado = ft.Dropdown(
            width=180,
            label="Estado",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Resuelto"),
            ],
            color="black",
            text_style=ft.TextStyle(color="black"),
            label_style=ft.TextStyle(color="black"),
            focused_border_color=self.AZUL
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== BOTONES REUTILIZABLES =====
    def build_btn_resuelto(self):
        return ft.ElevatedButton(
            "Resuelto",
            style=ft.ButtonStyle(
                bgcolor=self.VERDE,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    def build_btn_pendiente(self):
        return ft.ElevatedButton(
            "Pendiente",
            style=ft.ButtonStyle(
                bgcolor=self.ROJO,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    def build_btn_detalles(self):
        return ft.OutlinedButton(
            "Ver detalles",
            style=ft.ButtonStyle(
                color=self.AZUL,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

    # ===== CARD INCIDENCIA =====
    def build_card(self, nombre, matricula, razon, lugar, fecha, estado="Pendiente"):
        return ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    # IZQUIERDA (INFO)
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON, size=40, color=self.AZUL),
                            ft.Column(
                                [
                                    ft.Text(nombre, weight="bold", size=16, color="black"),
                                    ft.Text(f"Matrícula: {matricula}", size=12, color="black"),
                                    ft.Container(height=5),
                                    ft.Text(razon, size=13, color="black"),
                                    ft.Text(f"Lugar: {lugar}", size=12, color="black"),
                                    ft.Text(f"Fecha: {fecha}", size=12, color="black"),
                                ],
                                spacing=2
                            )
                        ],
                        spacing=15
                    ),

                    # DERECHA (BOTONES)
                    ft.Row(
                        [
                            # Asigna el botón dependiendo del estado
                            self.build_btn_resuelto() if estado == "Pendiente" else self.build_btn_pendiente(),
                            self.build_btn_detalles()
                        ],
                        spacing=10
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        
        # --- Contenedor de Filtros ---
        filtros = ft.Container(
            bgcolor="white",
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color="black12"),
            content=ft.Row(
                [
                    self.input_busqueda,
                    self.dropdown_estado,
                    ft.ElevatedButton(
                        "Buscar",
                        # on_click=self.buscar_incidencias, # Aquí conectarás tu futura función de BD
                        style=ft.ButtonStyle(
                            bgcolor=self.AZUL,
                            color="white"
                        )
                    )
                ],
                spacing=15
            )
        )

        # --- Lista de Incidencias (Estáticas por ahora) ---
        lista = ft.Column(
            [
                self.build_card("Carlos Daniel", "100025787", "Ruido excesivo", "Cubículo 1", "24/Marzo/2026", "Pendiente"),
                self.build_card("Cruz Castillo", "100025788", "Uso indebido del equipo", "Cubículo 2", "25/Marzo/2026", "Resuelto"),
                self.build_card("Jose Angel", "ABCDEFGA", "Comportamiento inapropiado", "Cubículo 3", "26/Marzo/2026", "Pendiente"),
                self.build_card("Figueroa Sales", "ABCDEFGA", "Ruido excesivo", "Cubículo 1", "27/Marzo/2026", "Resuelto"),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # --- Paginación ---
        paginacion = ft.Row(
            [
                ft.Text("1-10 de 100 incidencias", color="black"),
                ft.Row(
                    [
                        ft.OutlinedButton("Anterior"),
                        ft.OutlinedButton("Siguiente"),
                    ],
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # --- Ensamblaje Final ---
        self.content = ft.Column(
            [
                ft.Text("Incidencias", size=32, weight="bold", color="black"),
                ft.Text(
                    "Busca y gestiona el catalogo de incidencias registrados en el sistema",
                    color="black"
                ),
                filtros,
                lista,
                paginacion
            ],
            spacing=20,
            expand=True
        )
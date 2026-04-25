import flet as ft

class MenuLateral(ft.Container):
    def __init__(self, app_layout):
        super().__init__()
        self.app_layout = app_layout # Referencia a la app principal para cambiar vistas
        
        # Propiedades del Container (Sidebar)
        self.width = 250
        self.margin = ft.margin.only(left=20, top=20, bottom=20)
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = "white"
        self.shadow = ft.BoxShadow(
            blur_radius=25,
            color="black12",
            offset=ft.Offset(0, 10)
        )
        
        # Opciones del menú
        self.opciones = [
            {"icon": ft.Icons.HOME, "texto": "Principal"},
            {"icon": ft.Icons.QR_CODE, "texto": "Asistencia"},
            {"icon": ft.Icons.HISTORY, "texto": "Historial"},
            {"icon": ft.Icons.BAR_CHART, "texto": "Reportes"},
            {"icon": ft.Icons.MENU_BOOK, "texto": "Libros"},
            {"icon": ft.Icons.SWAP_HORIZ, "texto": "Préstamos"},
            {"icon": ft.Icons.WARNING, "texto": "Incidencias"},
        ]
        
        # Contenedor dinámico para los items del menú
        self.menu_items = ft.Column(spacing=10)
        
        # Contenido del Sidebar
        self.content = ft.Column([
            ft.Text("UNACH", size=22, weight="bold", color="#111827"),
            ft.Divider(height=20, color="transparent"),
            self.menu_items
        ])

    # Método que se llama cuando Flet construye el control
    def build(self):
        self.actualizar_menu()

    def actualizar_menu(self):
        self.menu_items.controls.clear()
        for index, opcion in enumerate(self.opciones):
            self.menu_items.controls.append(
                self.crear_item(opcion["icon"], opcion["texto"], index)
            )
        self.update() # Actualiza solo el sidebar

    def crear_item(self, icon, texto, index):
        activo = self.app_layout.index_actual == index

        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=5,
                        height=40,
                        bgcolor="#3B82F6" if activo else "transparent",
                        border_radius=5
                    ),
                    ft.Icon(
                        icon,
                        size=22,
                        color="#3B82F6" if activo else "#6B7280"
                    ),
                    ft.Text(
                        texto,
                        size=15,
                        weight="bold" if activo else "normal",
                        color="#111827" if activo else "#374151"
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=12,
            border_radius=12,
            bgcolor="#EFF6FF" if activo else "transparent",
            on_click=lambda e, idx=index: self.app_layout.cambiar_vista(idx)
        )
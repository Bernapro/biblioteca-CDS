import flet as ft

class MenuLateral(ft.Container):
    def __init__(self, on_menu_click, active_index=0, on_logout=None):
        super().__init__()
        self.on_menu_click = on_menu_click
        self.active_index = active_index
        self.on_logout = on_logout
        self.es_oscuro = False

        # Paleta por defecto (Modo Claro)
        self.CARD = "#FFFFFF"
        self.BORDER = "#E2E8F0"
        self.TEXT = "#0F172A"
        self.TEXT_SECONDARY = "#475569"
        self.ACTIVE_BG = "#DBEAFE"
        self.ACTIVE_COLOR = "#2563EB"
        
        # Estilos del Sidebar
        self.width = 250
        self.margin = ft.margin.only(left=20, top=20, bottom=20)
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = self.CARD
        self.border = ft.border.all(1, self.BORDER)
        self.shadow = ft.BoxShadow(blur_radius=25, color="black12", offset=ft.Offset(0, 10))

        # Opciones del menú
        self.opciones = [
            (ft.Icons.HOME, "Principal"),
            (ft.Icons.QR_CODE, "Asistencia"),
            (ft.Icons.HISTORY, "Historial"),
            (ft.Icons.BAR_CHART, "Reportes"),
            (ft.Icons.MENU_BOOK, "Libros"),
            (ft.Icons.SWAP_HORIZ, "Préstamos"),
            (ft.Icons.WARNING, "Incidencias"),
        ]

        # Botón Cerrar Sesión
        self.btn_logout = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.LOGOUT, size=22, color="#EF4444"),
                ft.Text("Cerrar sesión", size=15, weight="bold", color="#EF4444"),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=12,
            ink=True,
            on_click=self.cerrar_sesion
        )

        self.titulo_sidebar = ft.Text("UNACH", size=22, weight="bold", color=self.TEXT)

        # Menú dinámico
        self.menu_items = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        self.content = ft.Column(
            controls=[
                self.titulo_sidebar,
                ft.Divider(height=20, color="transparent"),
                self.menu_items,
                ft.Divider(height=10, color="transparent"),
                self.btn_logout
            ],
            expand=True
        )
        
        self.build_menu()

    def aplicar_tema(self, es_oscuro: bool):
        self.es_oscuro = es_oscuro
        if es_oscuro:
            self.CARD = "#1E222A"
            self.BORDER = "#2E3440"
            self.TEXT = "#F8F9FA"
            self.TEXT_SECONDARY = "#E2E8F0"
            self.ACTIVE_BG = "#242832"
            self.ACTIVE_COLOR = "#60A5FA"
        else:
            self.CARD = "#FFFFFF"
            self.BORDER = "#E2E8F0"
            self.TEXT = "#0F172A"
            self.TEXT_SECONDARY = "#475569"
            self.ACTIVE_BG = "#DBEAFE"
            self.ACTIVE_COLOR = "#2563EB"

        self.bgcolor = self.CARD
        self.border = ft.border.all(1, self.BORDER)
        self.titulo_sidebar.color = self.TEXT
        self.build_menu()
        try:
            if self.page is not None:
                self.update()
        except Exception:
            pass

    def build_menu(self):
        self.menu_items.controls.clear()
        
        for index, (icon, texto) in enumerate(self.opciones):
            activo = (self.active_index == index)
            
            item = ft.Container(
                content=ft.Row([
                    ft.Container(width=5, height=40, bgcolor=self.ACTIVE_COLOR if activo else "transparent", border_radius=5),
                    ft.Icon(icon, size=22, color=self.ACTIVE_COLOR if activo else self.TEXT_SECONDARY),
                    ft.Text(texto, size=15, weight="bold" if activo else "normal", color=self.ACTIVE_COLOR if activo else self.TEXT_SECONDARY),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=12,
                border_radius=12,
                bgcolor=self.ACTIVE_BG if activo else "transparent",
                on_click=lambda e, idx=index: self.cambiar_seleccion(idx)
            )
            self.menu_items.controls.append(item)

    def cambiar_seleccion(self, index):
        self.active_index = index
        self.build_menu()
        self.update()
        self.on_menu_click(index)

    def cerrar_sesion(self, e):
        if self.on_logout:
            try:
                self.on_logout()
            except Exception:
                pass
        from Presentacion.PantallaLogin import PantallaLogin
        e.page.theme_mode = ft.ThemeMode.LIGHT
        e.page.bgcolor = "#9ec9ff"
        e.page.controls.clear()
        login_app = PantallaLogin(e.page)
        e.page.add(login_app.construir_vista())
        e.page.update()
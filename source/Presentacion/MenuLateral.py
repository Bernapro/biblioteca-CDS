import flet as ft

class MenuLateral(ft.Container):
    def __init__(self, on_menu_click, active_index=0):
        super().__init__()
        self.on_menu_click = on_menu_click
        self.active_index = active_index
        
        # Estilos del Sidebar
        self.width = 250
        self.margin = ft.margin.only(left=20, top=20, bottom=20)
        self.padding = 20
        self.border_radius = 20
        self.bgcolor = "white"
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

        # Menú dinámico
        self.menu_items = ft.Column(spacing=10)
        self.content = ft.Column([
            ft.Text("UNACH", size=22, weight="bold", color="#111827"),
            ft.Divider(height=20, color="transparent"),
            self.menu_items
        ])
        
        # Dibuja el menú por primera vez
        self.build_menu()

    def build_menu(self):
        self.menu_items.controls.clear()
        
        for index, (icon, texto) in enumerate(self.opciones):
            # Comprobamos si este botón es el que está seleccionado actualmente
            activo = (self.active_index == index)
            
            item = ft.Container(
                content=ft.Row([
                    # Barrita lateral azul
                    ft.Container(width=5, height=40, bgcolor="#3B82F6" if activo else "transparent", border_radius=5),
                    # Icono
                    ft.Icon(icon, size=22, color="#3B82F6" if activo else "#6B7280"),
                    # Texto
                    ft.Text(texto, size=15, weight="bold" if activo else "normal", color="#111827" if activo else "#374151"),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=12,
                border_radius=12,
                bgcolor="#EFF6FF" if activo else "transparent",
                # Al hacer clic, ejecuta cambiar_seleccion pasando el índice de este botón
                on_click=lambda e, idx=index: self.cambiar_seleccion(idx)
            )
            self.menu_items.controls.append(item)

    def cambiar_seleccion(self, index):
        # 1. Actualizamos el índice de la pestaña seleccionada
        self.active_index = index
        
        # 2. Volvemos a construir los botones para que apliquen los colores al nuevo índice
        self.build_menu()
        
        # 3. Actualizamos solo la interfaz del Sidebar
        self.update()
        
        # 4. Le avisamos a la aplicación principal que cambie la vista
        self.on_menu_click(index)
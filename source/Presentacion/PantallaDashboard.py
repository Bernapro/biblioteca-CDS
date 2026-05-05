import flet as ft

class PantallaDashboard(ft.Container):
    def __init__(self, page: ft.Page):
        self._page = page
        
        # Colores (¡Excelente uso de los tokens dinámicos de Material 3!)
        self.CARD = "surface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.PRIMARY = "primary"
        self.TEXT_MAIN = "onSurface"

        # 1. ARMAMOS EL LAYOUT PRINCIPAL
        layout_principal = ft.Column(
            expand=True,
            spacing=25,
            scroll=ft.ScrollMode.AUTO, 
            controls=[
                # HEADER
                ft.Column(
                    [
                        ft.Row([ft.Text("Hola, Toileteros", size=28, weight="bold", color=self.TEXT_MAIN), ft.Text("👋", size=24)]),
                        ft.Text("Aquí tienes un resumen del sistema hoy.", size=14, color=self.TEXT_SECONDARY),
                    ],
                    spacing=2
                ),

                # TARJETAS SUPERIORES
                ft.Row(
                    [
                        self.build_card("Sesiones", 67, ft.Icons.PEOPLE_OUTLINED, self.PRIMARY, "12.5"),
                        self.build_card("Préstamos", 19, ft.Icons.BOOK_OUTLINED, "#10B981", "8.3"),
                        self.build_card("Vencidos", 28, ft.Icons.EVENT_BUSY_OUTLINED, "error", "15.7"),
                    ],
                    spacing=15
                ),

                # SECCIÓN INFERIOR ASIMÉTRICA
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=15,
                    controls=[
                        # Columna Izquierda
                        ft.Column(
                            controls=[
                                self.build_donut_chart(), 
                                self.build_boton() 
                            ],
                            expand=3, spacing=15
                        ),

                        # Columna Central
                        ft.Column(
                            controls=[
                                self.build_resumen_general()
                            ],
                            expand=3, spacing=15
                        ),

                        # Columna Derecha
                        ft.Column(
                            controls=[
                                self.build_bar_chart()
                            ],
                            expand=4, spacing=15
                        ),
                    ]
                )
            ]
        )

        super().__init__(
            expand=True,
            padding=ft.padding.only(left=20, top=10, right=20, bottom=20),
            bgcolor="transparent",
            content=layout_principal
        )

    # ===== COMPONENTES =====
    def build_card(self, title, value, icon_name, color_hex, percentage):
        return ft.Container(
            expand=True,
            height=120, 
            padding=20,
            bgcolor=self.CARD,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column([
                ft.Row([
                    ft.Container(content=ft.Icon(icon_name, color=color_hex, size=22), padding=10),
                    ft.Column([ft.Text(title, size=12, color=self.TEXT_SECONDARY, weight="w500"), ft.Text(str(value), size=24, weight="bold", color=self.TEXT_MAIN)], spacing=0, horizontal_alignment="end")
                ], alignment="spaceBetween"),
                ft.Row([ft.Icon(ft.Icons.ARROW_UPWARD, color="#10B981", size=14), ft.Text(f"{percentage}%", size=11, color="#10B981", weight="bold"), ft.Text("vs. sem. pasada", size=11, color=self.TEXT_SECONDARY)], spacing=5)
            ], alignment="spaceBetween")
        )

    def build_donut_chart(self):
        def detalle_turno(icono, titulo, valor, color_icono="primary", color_valor="onSurface"):
            return ft.Row(
                spacing=12,
                controls=[
                    ft.Container(content=ft.Icon(icono, size=14, color=color_icono), padding=8),
                    ft.Column(
                        spacing=0, 
                        controls=[
                            ft.Text(titulo, size=10, color=self.TEXT_SECONDARY),
                            ft.Text(valor, size=12, weight="bold", color=color_valor)
                        ]
                    )
                ]
            )

        return ft.Container(
            height=415, 
            bgcolor=self.CARD, border_radius=20, 
            padding=25, 
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                spacing=12,
                controls=[
                    # 1. HEADER 
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Row([ft.Icon(ft.Icons.AV_TIMER, size=16, color=self.TEXT_MAIN), ft.Text("Cambio de turno", size=14, weight="bold", color=self.TEXT_MAIN)], spacing=5),
                            ft.Container(
                                content=ft.Row([ft.Container(width=6, height=6, border_radius=3, bgcolor="#10B981"), ft.Text("Turno actual", size=10, color=self.TEXT_MAIN)], spacing=5), 
                                bgcolor="surfaceVariant", padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=10
                            )
                        ]
                    ),
                    
                    # 2. CUERPO 
                    ft.Container(
                        expand=True, 
                        content=ft.Row(
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Column(
                                    expand=1,
                                    horizontal_alignment="center",
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                    controls=[
                                        ft.Stack(
                                            alignment=ft.Alignment(0, 0),
                                            controls=[
                                                # 🔥 AQUÍ ESTÁ LA MAGIA: Un solo anillo con bgcolor hace todo el trabajo
                                                ft.ProgressRing(
                                                    value=0.68, 
                                                    stroke_width=14, 
                                                    width=140, 
                                                    height=140, 
                                                    color=self.PRIMARY,          # Color de la barra llena
                                                    bgcolor="surfaceVariant"     # Color del hueco vacío
                                                ),
                                                ft.Column([ft.Text("01:25:32", size=15, weight="bold", color=self.TEXT_MAIN), ft.Text("restante", size=10, color=self.TEXT_SECONDARY)], alignment="center", horizontal_alignment="center", spacing=0)
                                            ]
                                        ),
                                        ft.Column([ft.Text("68%", size=15, weight="bold", color=self.TEXT_MAIN), ft.Text("del turno restante", size=10, color=self.TEXT_SECONDARY)], horizontal_alignment="center", spacing=0)
                                    ]
                                ),
                                
                                ft.Column(
                                    expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                    controls=[
                                        detalle_turno(ft.Icons.PLAY_ARROW_OUTLINED, "Inicio de turno", "08:00 AM"),
                                        detalle_turno(ft.Icons.FLAG_OUTLINED, "Fin de turno", "04:00 PM"),
                                        detalle_turno(ft.Icons.ACCESS_TIME, "Duración total", "8 horas"),
                                        detalle_turno(ft.Icons.HOURGLASS_BOTTOM, "Tiempo transcurrido", "06:34:28", self.PRIMARY, self.PRIMARY),
                                    ]
                                )
                            ]
                        )
                    ),
                    
                    # 3. FOOTER 
                    ft.Container(
                        bgcolor="primaryContainer", padding=10, border_radius=10,
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO, size=14, color="onPrimaryContainer"),
                            ft.Text("El cambio de turno está programado para las 04:00 PM", size=10, color="onPrimaryContainer", weight="bold")
                        ], spacing=8)
                    )
                ]
            )
        )

    def build_resumen_general(self):
        def item_lista(icono, color, titulo, valor):
            return ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Row([
                        ft.Container(content=ft.Icon(icono, size=18, color=color), padding=8),
                        ft.Column([
                            ft.Text(titulo, size=12, color=self.TEXT_SECONDARY),
                            ft.Text(valor, size=16, weight="bold", color=self.TEXT_MAIN)
                        ], spacing=0)
                    ])
                ]
            )

        return ft.Container(
            height=480, 
            bgcolor=self.CARD, border_radius=20, 
            padding=25, 
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                spacing=40, 
                controls=[
                    ft.Text("Resumen general", size=16, weight="bold", color=self.TEXT_MAIN),
                    item_lista(ft.Icons.VISIBILITY_OUTLINED, self.PRIMARY, "Visitas totales", "1,248"),
                    item_lista(ft.Icons.PERSON_OUTLINE, "#10B981", "Usuarios registrados", "342"),
                    item_lista(ft.Icons.BOOK_OUTLINED, "#8B5CF6", "Libros disponibles", "1,876"),
                    item_lista(ft.Icons.WARNING_AMBER_ROUNDED, "error", "Incidencias abiertas", "6"),
                ]
            )
        )

    def build_bar_chart(self):
        def barra(alto, label, valor):
            return ft.Column(
                horizontal_alignment="center",
                spacing=5,
                controls=[
                    ft.Text(str(valor), size=11, color=self.TEXT_SECONDARY, weight="bold"),
                    ft.Container(width=35, height=alto, border_radius=4, bgcolor=self.PRIMARY), 
                    ft.Text(label, size=12, color=self.TEXT_SECONDARY)
                ]
            )

        return ft.Container(
            height=480, 
            bgcolor=self.CARD, border_radius=20, 
            padding=25, 
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                controls=[
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text("Gráfica de la semana", size=16, weight="bold", color=self.TEXT_MAIN),
                            ft.Container(
                                content=ft.Row([ft.Text("Esta semana", size=11, color=self.TEXT_MAIN), ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=14, color=self.TEXT_MAIN)], spacing=5), 
                                border=ft.border.all(1, "outlineVariant"), padding=ft.padding.symmetric(horizontal=8, vertical=4), border_radius=8
                            )
                        ]
                    ),
                    ft.Row(
                        alignment="spaceEvenly", 
                        vertical_alignment="end",
                        controls=[
                            barra(220, "Lun", 65),
                            barra(300, "Mar", 88),
                            barra(240, "Mié", 72),
                            barra(180, "Jue", 56),
                            barra(260, "Vie", 78),
                            barra(140, "Sáb", 48),
                            barra(200, "Dom", 62),
                        ]
                    )
                ]
            )
        )

    def build_boton(self):
        return ft.Container(
            height=50, 
            width=float("inf"), alignment=ft.Alignment(0, 0), border_radius=12, bgcolor=self.PRIMARY,
            shadow=ft.BoxShadow(blur_radius=10, color="black12"),
            content=ft.Row([ft.Icon(ft.Icons.PICTURE_AS_PDF_OUTLINED, color="onPrimary", size=20), ft.Text("Generar Reporte PDF", size=14, color="onPrimary", weight="bold")], alignment="center", spacing=10)
        )
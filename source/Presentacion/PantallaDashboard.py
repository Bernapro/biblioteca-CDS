import flet as ft

from Negocio.Controlador.ControladorDashboard import ControladorDashboard


class PantallaDashboard(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.controlador = ControladorDashboard()

        self.CARD = "surface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.PRIMARY = "primary"
        self.TEXT_MAIN = "onSurface"

        self.label_sesiones = ft.Text("0", size=28, weight="bold", color=self.TEXT_MAIN)
        self.label_prestamos = ft.Text("N/D", size=28, weight="bold", color=self.TEXT_MAIN)
        self.label_vencidos = ft.Text("N/D", size=28, weight="bold", color=self.TEXT_MAIN)

        self.label_visitas_totales = ft.Text("0", size=16, weight="bold", color=self.TEXT_MAIN)
        self.label_usuarios_registrados = ft.Text("0", size=16, weight="bold", color=self.TEXT_MAIN)
        self.label_libros_disponibles = ft.Text("N/D", size=16, weight="bold", color=self.TEXT_MAIN)
        self.label_incidencias_abiertas = ft.Text("0", size=16, weight="bold", color=self.TEXT_MAIN)

        self.turno_estado = ft.Text("Matutino", size=24, weight="bold", color=self.TEXT_MAIN)
        self.turno_inicio = ft.Text("08:00 AM", size=14, color=self.TEXT_MAIN)
        self.turno_fin = ft.Text("02:00 PM", size=14, color=self.TEXT_MAIN)
        self.turno_restante = ft.Text("00:00:00", size=14, color=self.TEXT_MAIN)
        self.turno_duracion = ft.Text("6 horas", size=14, color=self.TEXT_MAIN)

        self.bar_labels = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        self.bar_value_labels = []
        self.bar_containers = []

        self.btn_actualizar = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.REFRESH, size=18),
                ft.Text("Actualizar", size=14)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            on_click=self.cargar_datos,
            style=ft.ButtonStyle(
                bgcolor=self.PRIMARY,
                color="onPrimary",
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(horizontal=22, vertical=16)
            )
        )

        self.layout_principal = ft.Column(
            expand=True,
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Row([ft.Text("Hola, Toileteros", size=28, weight="bold", color=self.TEXT_MAIN), ft.Text("👋", size=24)]),
                            ft.Text("Aquí tienes un resumen del sistema hoy.", size=14, color=self.TEXT_SECONDARY),
                        ], spacing=4),
                        self.btn_actualizar
                    ]
                ),
                ft.Row(
                    spacing=15,
                    controls=[
                        self.build_card("Sesiones activas hoy", self.label_sesiones, ft.Icons.PEOPLE_OUTLINED, self.PRIMARY),
                        self.build_card("Préstamos activos", self.label_prestamos, ft.Icons.BOOK_OUTLINED, "#10B981"),
                        self.build_card("Vencidos", self.label_vencidos, ft.Icons.EVENT_BUSY_OUTLINED, "error"),
                    ]
                ),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=15,
                    controls=[
                        ft.Column(
                            expand=3,
                            spacing=15,
                            controls=[
                                self.build_turno_card(),
                                self.build_boton()
                            ]
                        ),
                        ft.Column(
                            expand=3,
                            spacing=15,
                            controls=[
                                self.build_resumen_general()
                            ]
                        ),
                        ft.Column(
                            expand=4,
                            spacing=15,
                            controls=[
                                self.build_bar_chart()
                            ]
                        )
                    ]
                )
            ]
        )

        self.content = self.layout_principal
        self.cargar_datos()

    def did_mount(self):
        self.cargar_datos()

    def build_card(self, title, value, icon_name, color_hex):
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
                    ft.Column([
                        ft.Text(title, size=12, color=self.TEXT_SECONDARY, weight="w500"),
                        value
                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.END)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def build_turno_card(self):
        def detalle_turno(icono, titulo, valor):
            return ft.Row(
                spacing=12,
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, size=16, color=self.PRIMARY),
                        padding=8
                    ),
                    ft.Column([
                        ft.Text(titulo, size=12, color=self.TEXT_SECONDARY),
                        valor
                    ], spacing=0)
                ]
            )

        return ft.Container(
            height=415,
            bgcolor=self.CARD,
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text("Turno actual", size=16, weight="bold", color=self.TEXT_MAIN),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=self.PRIMARY, size=20),
                            self.turno_estado
                        ], spacing=10),
                        padding=ft.padding.symmetric(horizontal=16, vertical=14),
                        border_radius=14,
                        bgcolor="surfaceVariant"
                    ),
                    detalle_turno(ft.Icons.PLAY_ARROW_OUTLINED, "Inicio", self.turno_inicio),
                    detalle_turno(ft.Icons.FLAG_OUTLINED, "Fin", self.turno_fin),
                    detalle_turno(ft.Icons.ACCESS_TIME, "Duración", self.turno_duracion),
                    detalle_turno(ft.Icons.HOURGLASS_BOTTOM, "Tiempo restante", self.turno_restante),
                    ft.Container(
                        bgcolor="primaryContainer",
                        border_radius=12,
                        padding=ft.padding.all(12),
                        content=ft.Text("Actualiza los datos manualmente con el botón.", size=12, color="onPrimaryContainer")
                    )
                ]
            )
        )

    def build_resumen_general(self):
        def item_lista(icono, color, titulo, valor):
            return ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row([
                        ft.Container(content=ft.Icon(icono, size=18, color=color), padding=8),
                        ft.Column([
                            ft.Text(titulo, size=12, color=self.TEXT_SECONDARY),
                            valor
                        ], spacing=0)
                    ])
                ]
            )

        return ft.Container(
            height=480,
            bgcolor=self.CARD,
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                spacing=30,
                controls=[
                    ft.Text("Resumen general", size=16, weight="bold", color=self.TEXT_MAIN),
                    item_lista(ft.Icons.VISIBILITY_OUTLINED, self.PRIMARY, "Visitas totales", self.label_visitas_totales),
                    item_lista(ft.Icons.PERSON_OUTLINE, "#10B981", "Usuarios registrados", self.label_usuarios_registrados),
                    item_lista(ft.Icons.BOOK_OUTLINED, "#8B5CF6", "Libros disponibles", self.label_libros_disponibles),
                    item_lista(ft.Icons.WARNING_AMBER_ROUNDED, "error", "Incidencias abiertas", self.label_incidencias_abiertas),
                ]
            )
        )

    def build_bar_chart(self):
        barras = []
        for label in self.bar_labels:
            valor_label = ft.Text("0", size=11, color=self.TEXT_SECONDARY, weight="bold")
            barra_container = ft.Container(width=35, height=70, border_radius=4, bgcolor=self.PRIMARY)
            self.bar_value_labels.append(valor_label)
            self.bar_containers.append(barra_container)
            barras.append(
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                        valor_label,
                        barra_container,
                        ft.Text(label, size=12, color=self.TEXT_SECONDARY)
                    ]
                )
            )

        self.bar_chart_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.END,
            controls=barras
        )

        return ft.Container(
            height=480,
            bgcolor=self.CARD,
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=15, color="#0000000D"),
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Gráfica de la semana", size=16, weight="bold", color=self.TEXT_MAIN),
                        ]
                    ),
                    self.bar_chart_row
                ]
            )
        )

    def build_boton(self):
        return ft.Container(
            height=50,
            width=float("inf"),
            alignment=ft.Alignment(0, 0),
            border_radius=12,
            bgcolor=self.PRIMARY,
            shadow=ft.BoxShadow(blur_radius=10, color="black12"),
            content=ft.Row([
                ft.Icon(ft.Icons.PICTURE_AS_PDF_OUTLINED, color="onPrimary", size=20),
                ft.Text("Generar Reporte PDF", size=14, color="onPrimary", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        )

    def actualizar_barras(self, datos_semana):
        valores = [datos_semana.get(i, 0) for i in range(1, 8)]
        max_valor = max(valores) if valores else 1

        for idx, cantidad in enumerate(valores):
            self.bar_value_labels[idx].value = str(cantidad)
            self.bar_containers[idx].height = 70 + int((cantidad / max_valor) * 180) if max_valor else 70

    def safe_update(self):
        try:
            self.update()
        except Exception:
            pass

    def cargar_datos(self, e=None):
        datos = self.controlador.obtener_datos_dashboard()

        self.label_sesiones.value = str(datos["sesiones_activas_hoy"])
        self.label_prestamos.value = str(datos["prestamos"])
        self.label_vencidos.value = str(datos["vencidos"])

        self.label_visitas_totales.value = str(datos["visitas_semana_totales"])
        self.label_usuarios_registrados.value = str(datos["usuarios_registrados"])
        self.label_libros_disponibles.value = "N/D"
        self.label_incidencias_abiertas.value = str(datos["incidencias_abiertas"])

        turno = datos.get("turno", {})
        self.turno_estado.value = turno.get("turno", "Matutino")
        self.turno_inicio.value = turno.get("inicio", "08:00 AM")
        self.turno_fin.value = turno.get("fin", "02:00 PM")
        self.turno_duracion.value = turno.get("duracion_horas", "6 horas")
        self.turno_restante.value = turno.get("restante_formateado", "00:00:00")

        self.actualizar_barras(datos.get("visitas_semana", {}))
        self.safe_update()

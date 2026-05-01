import flet as ft

from Negocio.Controlador.ControladorAsistencia import ControladorAsistencia
from Presentacion.PantallaRegistroUsuario import PantallaRegistroUsuario


class PantallaAsistencia(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

        self.control = ControladorAsistencia(self)

        self.expand = True
        self.padding = 30
        self.bgcolor = "#EAF1F7"
        self.border_radius = 30
        
        self.AZUL = "#3B82F6"
        self.CARD = "white"
        self.TEXT = "#111827"
        self.TEXT_SECONDARY = "#6B7280"

        self.mensaje_final = ft.Column(
            [],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.input_qr = ft.TextField(
            hint_text="Ingresa código QR",
            width=240,
            autofocus=True,
            text_style=ft.TextStyle(color=self.TEXT),
            hint_style=ft.TextStyle(color=self.TEXT),
            border_radius=12,
            border_color="#D1D5DB",
            prefix_icon=ft.Icons.PERSON,
            on_submit=self.procesar_qr,
            on_change=lambda e: self.limpiar_mensaje()
        )

        self.build_ui()

    # =========================
    # MENSAJE DINÁMICO
    # =========================
    def mostrar_resultado(self, estado, nombre, tipo_usuario):

        # ===== COLORES POR TIPO =====
        colores = {
            "ALUMNO": "#3B82F6",
            "PERSONAL": "#10B981",
            "VISITANTE": "#F59E0B"
        }

        color_tipo = colores.get(tipo_usuario, "#6B7280")

        # ===== TEXTO TIPO =====
        texto_tipo = tipo_usuario.capitalize() if tipo_usuario else ""

        badge = ft.Container(
            content=ft.Text(
                f"[ {texto_tipo} ]",
                color=color_tipo,
                weight="bold",
                size=14
            ),
            padding=ft.padding.symmetric(horizontal=8, vertical=2),
            border_radius=8,
            border=ft.border.all(1, color_tipo),
            bgcolor={
                "ALUMNO": "#DBEAFE",
                "PERSONAL": "#D1FAE5",
                "VISITANTE": "#FEF3C7"
            }.get(tipo_usuario, "#F3F4F6")
        )

        # ===== MENSAJE PRINCIPAL =====
        if estado == "ENTRADA":
            mensaje = ft.Text(
                "✅ Entrada registrada correctamente",
                color="#16A34A",
                weight="bold"
            )

        elif estado == "SALIDA":
            mensaje = ft.Text(
                "👋 Salida registrada correctamente",
                color="#2563EB",
                weight="bold"
            )

        elif estado == "NO_ENCONTRADO":
            self.mensaje_final.controls = [
                ft.Text("❌ Usuario no encontrado", color="#DC2626", weight="bold")
            ]
            self.update()
            return

        elif estado == "INVALIDO":
            self.mensaje_final.controls = [
                ft.Text("⚠️ Ingresa un código válido", color="#D97706", weight="bold")
            ]
            self.update()
            return

        else:
            self.mensaje_final.controls = []
            self.update()
            return

        # ===== RESULTADO FINAL =====
        self.mensaje_final.controls = [
            mensaje,
            ft.Text(nombre, size=16, weight="bold", color="#000000"),
            badge
        ]

        self.update()

    def limpiar_mensaje(self):
        self.mensaje_final.value = ""
        self.update()
    # =========================
    # PROCESAR QR (CORREGIDO)
    # =========================
    def procesar_qr(self, e):
        e.control.data = "btn_qr"

        respuesta = self.control.procesar_qr(e)

        if not respuesta:
            return

        estado = respuesta.get("estado")
        nombre = respuesta.get("nombre")
        tipo_usuario = respuesta.get("tipo")

        self.mostrar_resultado(estado, nombre, tipo_usuario)

    def ir_a_registro(self, e):
        self.content = PantallaRegistroUsuario(self._page, vista_anterior=self)
        self.update()

    def build_ui(self):
        
        panel_qr = ft.Container(
            expand=1,
            height=260,
            bgcolor="#F3F4F6",
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.QR_CODE_SCANNER, size=140, color=self.AZUL),
                    ft.Text("Esperando escaneo...", size=14, color=self.TEXT_SECONDARY),
                    ft.Container(width=10, height=10, bgcolor="#22C55E", border_radius=10)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )

        panel_input = ft.Container(
            expand=1,
            height=260,
            bgcolor="#F3F4F6",
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=120, color=self.AZUL),
                    self.input_qr,
                    ft.ElevatedButton(
                        "Confirmar",
                        on_click=self.procesar_qr,
                        data="btn_qr",
                        style=ft.ButtonStyle(
                            bgcolor="#111827",
                            color="white"
                        )
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )

        card = ft.Container(
            width=720,
            height=600,
            border_radius=40,
            padding=30,
            gradient=ft.LinearGradient(
                colors=["#cfe8ff", "#9ec9ff"],
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1)
            ),
            content=ft.Container(
                expand=True,
                bgcolor=self.CARD,
                border_radius=30,
                padding=30,
                shadow=ft.BoxShadow(blur_radius=25, color="black26"),
                content=ft.Column(
                    [
                        ft.Text("Registro de asistencia", size=30, weight="bold", color=self.TEXT),
                        ft.Text("Escanea tu código QR para ingresar", size=16, color=self.TEXT_SECONDARY),

                        ft.Row(
                            [
                                panel_qr,
                                ft.Container(
                                    width=40,
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Text("O", size=28, weight="bold", color=self.TEXT)
                                ),
                                panel_input
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),

                        ft.OutlinedButton(
                            "Registrar nuevo usuario",
                            icon=ft.Icons.PERSON_ADD,
                            style=ft.ButtonStyle(
                                color=self.AZUL,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=self.ir_a_registro
                        ),

                        self.mensaje_final

                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                )
            )
        )

        self.content = ft.Column(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
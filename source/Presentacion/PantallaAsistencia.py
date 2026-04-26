import flet as ft

# IMPORTACIÓN DE SERVICIO (Se mantiene igual)
from Negocio.asistencia_service import registrar_qr

# Importar la nueva pantalla de registro
from Presentacion.PantallaRegistroUsuario import PantallaRegistroUsuario


class PantallaAsistencia(ft.Container):
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
        self.CARD = "white"
        self.TEXT = "#111827"
        self.TEXT_SECONDARY = "#6B7280"

        # ===== CONTROLES DINÁMICOS =====
        # Declaramos los controles que van a cambiar de valor/color como atributos
        self.resultado = ft.Text("", size=14, color=self.TEXT)

        self.input_qr = ft.TextField(
            hint_text="Ingresa código QR",
            width=240,
            text_style=ft.TextStyle(color=self.TEXT),
            hint_style=ft.TextStyle(color=self.TEXT),
            border_radius=12,
            border_color="#D1D5DB",
            prefix_icon=ft.Icons.PERSON,
            on_submit=self.procesar_qr  # Al dar Enter, llama a la función
        )

        # Construir y ensamblar toda la UI
        self.build_ui()

    # ===== LOGICA =====
    def procesar_qr(self, e):
        qr = self.input_qr.value.strip() if self.input_qr.value else ""

        if not qr:
            self.resultado.value = "⚠️ Ingresa un código QR"
            self.resultado.color = "red"
            self.input_qr.border_color = "red"
            self.update()  # Actualizamos solo esta vista
            return

        if len(qr) < 3:
            self.resultado.value = "⚠️ Código QR inválido"
            self.resultado.color = "red"
            self.input_qr.border_color = "red"
            self.update()
            return

        self.input_qr.border_color = "#D1D5DB"

        # Llamada al servicio
        mensaje = registrar_qr(qr)

        if "Entrada" in mensaje or "Salida" in mensaje:
            self.resultado.color = "green"
            self.input_qr.value = ""
        else:
            self.resultado.color = "red"

        self.resultado.value = mensaje
        self.update() # Actualizamos la vista con el resultado final

    def ir_a_registro(self, e):
        # Cambiamos el contenido de esta pantalla a la de Registro
        self.content = PantallaRegistroUsuario(self._page, vista_anterior=self)
        self.update()

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
    def build_ui(self):
        
        # --- Panel QR ---
        panel_qr = ft.Container(
            expand=1,  # CLAVE
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

        # --- Panel Input ---
        panel_input = ft.Container(
            expand=1,  # CLAVE
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
                        on_click=self.procesar_qr, # Botón conectado a la función
                        style=ft.ButtonStyle(
                            bgcolor="#111827",
                            color="white"
                        )
                    ),
                    self.resultado
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )

        # --- Card Principal ---
        card = ft.Container(
            width=720,
            height=540,
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
                        ft.Text("Registro de usuario", size=30, weight="bold", color=self.TEXT),
                        ft.Text("Escanea tu código QR para ingresar", size=16, color=self.TEXT_SECONDARY),

                        # 🔥 CONTENEDOR QUE LIMITA TODO
                        ft.Container(
                            width=float("inf"),
                            content=ft.Row(
                                [
                                    panel_qr,
                                    
                                    ft.Container(
                                        width=40,
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Text(
                                            "O",
                                            size=28,
                                            weight="bold",
                                            color=self.TEXT
                                        )
                                    ),
                                    
                                    panel_input
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20
                            )
                        ),

                        # --- Botón Registrar Usuario ---
                        ft.OutlinedButton(
                            "Registrar nuevo usuario",
                            icon=ft.Icons.PERSON_ADD,
                            style=ft.ButtonStyle(
                                color=self.AZUL,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=self.ir_a_registro
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                )
            )
        )

        # Asignamos el diseño centrado al contenido del contenedor principal
        self.content = ft.Column(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
import flet as ft
from servicios.asistencia_service import registrar_qr


def asistencia_view(page):

    AZUL = "#3B82F6"
    BG = "#EAF1F7"
    CARD = "white"
    TEXT = "#111827"
    TEXT_SECONDARY = "#6B7280"

    resultado = ft.Text("", size=14, color=TEXT)

    input_qr = ft.TextField(
        hint_text="Ingresa código QR",
        width=240,
        text_style=ft.TextStyle(color=TEXT),
        hint_style=ft.TextStyle(color=TEXT),
        border_radius=12,
        border_color="#D1D5DB",
        prefix_icon=ft.Icons.PERSON
    )

    # ===== LOGICA =====
    def procesar_qr(e):

        qr = input_qr.value.strip() if input_qr.value else ""

        if not qr:
            resultado.value = "⚠️ Ingresa un código QR"
            resultado.color = "red"
            input_qr.border_color = "red"
            page.update()
            return

        if len(qr) < 3:
            resultado.value = "⚠️ Código QR inválido"
            resultado.color = "red"
            input_qr.border_color = "red"
            page.update()
            return

        input_qr.border_color = "#D1D5DB"

        mensaje = registrar_qr(qr)

        if "Entrada" in mensaje or "Salida" in mensaje:
            resultado.color = "green"
            input_qr.value = ""
        else:
            resultado.color = "red"

        resultado.value = mensaje
        page.update()

    input_qr.on_submit = procesar_qr

    # ===== PANEL QR =====
    panel_qr = ft.Container(
        expand=1,  # 🔥 CLAVE
        height=320,
        bgcolor="#F3F4F6",
        border_radius=20,
        padding=20,
        content=ft.Column(
            [
                ft.Icon(ft.Icons.QR_CODE_SCANNER, size=140, color=AZUL),
                ft.Text("Esperando escaneo...", size=14, color=TEXT_SECONDARY),
                ft.Container(width=10, height=10, bgcolor="#22C55E", border_radius=10)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    # ===== PANEL INPUT =====
    panel_input = ft.Container(
        expand=1,  # 🔥 CLAVE
        height=320,
        bgcolor="#F3F4F6",
        border_radius=20,
        padding=20,
        content=ft.Column(
            [
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=120, color=AZUL),
                input_qr,
                ft.ElevatedButton(
                    "Confirmar",
                    on_click=procesar_qr,
                    style=ft.ButtonStyle(
                        bgcolor="#111827",
                        color="white"
                    )
                ),
                resultado
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

    # ===== CARD PRINCIPAL =====
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
            bgcolor=CARD,
            border_radius=30,
            padding=30,
            shadow=ft.BoxShadow(blur_radius=25, color="black26"),
            content=ft.Column(
                [
                    ft.Text("Registro de usuario", size=30, weight="bold", color=TEXT),
                    ft.Text("Escanea tu código QR para ingresar", size=16, color=TEXT_SECONDARY),

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
                                        color=TEXT
                                    )
                                ),

                                panel_input
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25
            )
        )
    )

    return ft.Container(
        expand=True,
        padding=30,
        bgcolor=BG,
        border_radius=30,
        content=ft.Column(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
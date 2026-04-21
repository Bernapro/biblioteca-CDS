import flet as ft
from servicios.asistencia_service import registrar_qr


def asistencia_view(page):

    resultado = ft.Text("", size=14, color="black")

    input_qr = ft.TextField(
        hint_text="Ingresa código QR",
        width=250,
        text_style=ft.TextStyle(color="black"),
        border_color="black"
    )

    # Función para procesar el código QR
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

        # reset visual
        input_qr.border_color = "black"

        # procesar QR
        mensaje = registrar_qr(qr)

        
        if "Entrada" in mensaje or "Salida" in mensaje:
            resultado.color = "green"
            input_qr.value = ""  # limpiar input
        else:
            resultado.color = "red"

        resultado.value = mensaje

        page.update()

    # ENTER TAMBIÉN ENVÍA
    input_qr.on_submit = procesar_qr

    return ft.Container(
        expand=True,
        content=ft.Column(
            [
                ft.Container(
                    width=600,
                    height=500,
                    bgcolor="white",
                    border_radius=40,
                    padding=30,
                    shadow=ft.BoxShadow(blur_radius=25, color="black26"),

                    content=ft.Column(
                        [
                            ft.Text("Registro de usuario", size=28, weight="bold", color="black"),
                            ft.Text("Escanea tu código QR para ingresar", color="black"),

                            ft.Icon(ft.Icons.PERSON, size=80, color="#3B82F6"),

                            ft.Container(
                                padding=20,
                                border_radius=20,
                                bgcolor="#F3F4F6",
                                content=ft.Column(
                                    [
                                        ft.Container(
                                            width=220,
                                            height=50,
                                            alignment=ft.alignment.Alignment(0, 0),
                                            gradient=ft.LinearGradient(
                                                colors=["#3B82F6", "#2563EB"]
                                            ),
                                            border_radius=15,
                                            content=ft.Text("Ingresar QR", color="white")
                                        ),

                                        input_qr,

                                        ft.ElevatedButton(
                                            "Confirmar",
                                            on_click=procesar_qr
                                        ),

                                        resultado
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
import flet as ft
from Presentacion.PantallaPrincipal import PantallaPrincipal
# Importamos el controlador que hace el trabajo sucio en la BD
from Negocio.Controlador.ControladorLogin import ControladorLogin

class PantallaLogin:
    def __init__(self, page: ft.Page):
        self.page = page
        
        # --- COLORES EXACTOS AL DISEÑO ---
        self.azul_unach = "#1a56db"
        self.fondo_izquierdo = "#e8f0fe" 
        self.texto_gris = "#6b7280"
        
        # --- INPUTS DEL FORMULARIO ---
        self.usuario_input = ft.TextField(
            label="Usuario",
            hint_text="Ingresa tu usuario",
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            text_size=14,
            label_style=ft.TextStyle(color=self.azul_unach),
            border_color="#d1d5db",
            focused_border_color=self.azul_unach,
            height=55,
            width=550
        )
        
        self.pass_input = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            text_size=14,
            label_style=ft.TextStyle(color=self.azul_unach),
            border_color="#d1d5db",
            focused_border_color=self.azul_unach,
            height=55,
            width=550
        )

    def mostrar_alerta(self, mensaje, es_error=True):
        alerta = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE, weight="bold"),
            bgcolor=ft.Colors.ERROR if es_error else ft.Colors.GREEN_400,
            # 💡 Quitamos action_color para evitar el crash
            action="Entendido", 
        )
        self.page.overlay.append(alerta)
        alerta.open = True
        self.page.update()

    def intentar_login(self, e):
        usuario_ingresado = self.usuario_input.value
        pass_ingresada = self.pass_input.value

        if not usuario_ingresado or not pass_ingresada:
            self.mostrar_alerta("Por favor, llena todos los campos.")
            return

        boton = e.control
        texto_boton = boton.content.controls[0] 
        texto_original = texto_boton.value
        
        texto_boton.value = "Verificando..."
        boton.disabled = True
        self.page.update()

        try:
            acceso_valido = ControladorLogin.validar_credenciales(usuario_ingresado, pass_ingresada)
        except Exception as ex:
            texto_boton.value = texto_original
            boton.disabled = False
            self.mostrar_alerta(f"Error de conexión: {ex}")
            return

        if acceso_valido:
            self.page.controls.clear()
            self.page.update()
            try:
                app_principal = PantallaPrincipal(self.page)
                self.page.add(app_principal)
                self.page.update()
            except Exception as ex:
                self.mostrar_alerta(f"Error al cargar menú principal: {ex}")
        else:
            texto_boton.value = texto_original
            boton.disabled = False
            self.pass_input.value = ""
            self.mostrar_alerta("Usuario o contraseña incorrectos.")

    def construir_vista(self):
        panel_izquierdo = ft.Container(
            expand=4, 
            bgcolor=self.fondo_izquierdo,
            border_radius=ft.border_radius.only(top_right=80, bottom_right=80),
            padding=ft.padding.all(30),
            # CORRECCIÓN: Usamos Alignment(0,0) para evitar AttributeError
            alignment=ft.alignment.Alignment(0, 0), 
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src="logo.png", width=160, fit="contain"),
                    ft.Container(height=10),
                    ft.Text("Sistema de Gestión de Biblioteca", size=14, color=ft.Colors.BLACK87),
                    ft.Container(height=50),
                    ft.Image(src="Ilustracion.png", width=280, fit="contain"),
                    ft.Container(height=50),
                    ft.Text(
                        "“ La lectura es la llave\nque abre puertas al conocimiento ”",
                        italic=True,
                        text_align=ft.TextAlign.CENTER,
                        color=self.texto_gris,
                        size=13
                    )
                ]
            )
        )

        formulario = ft.Container(
            width=650, 
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.only(left=50, right=50, top=60, bottom=40),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1, 
                blur_radius=25, 
                color=ft.Colors.BLACK12, 
                offset=ft.Offset(0, 10)
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                controls=[
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("¡Bienvenido!", size=32, weight=ft.FontWeight.W_900, color=ft.Colors.BLACK), 
                                ft.Text("Inicia sesión para continuar", size=14, color=self.texto_gris),
                            ]
                        ),
                        # CORRECCIÓN: Usamos Alignment(0,0)
                        alignment=ft.alignment.Alignment(0, 0),
                        margin=ft.margin.only(bottom=40) 
                    ),
                    self.usuario_input,
                    ft.Container(height=15),
                    self.pass_input,
                    ft.Container(height=15),
                    ft.Row(
                        width=550,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                           
                           
                        ]
                    ),
                    ft.Container(height=30),
                    ft.ElevatedButton(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Iniciar sesión", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE), 
                            ]
                        ),
                        bgcolor=self.azul_unach,
                        height=50,
                        width=550,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        on_click=self.intentar_login
                    ),
                    ft.Container(height=40),
                    ft.Container(
                        content=ft.Text("Sistema de Gestión de Biblioteca", size=11, color="#d1d5db"),
                        # CORRECCIÓN: Usamos Alignment(0,0)
                        alignment=ft.alignment.Alignment(0, 0) 
                    )
                ]
            )
        )

        panel_derecho = ft.Container(
            expand=6, 
            # CORRECCIÓN: Usamos Alignment(0,0)
            alignment=ft.alignment.Alignment(0, 0), 
            content=formulario
        )

        return ft.Container(
            expand=True,
            bgcolor="#f4f7fc", 
            content=ft.Row(
                expand=True,
                spacing=0, 
                controls=[panel_izquierdo, panel_derecho]
            )
        )
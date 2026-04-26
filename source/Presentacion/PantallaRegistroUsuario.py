import flet as ft

class PantallaRegistroUsuario(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        
        # ===== ESTILOS Y COLORES =====
        self.AZUL = "#3B82F6"
        self.TEXT = "#111827"
        self.CARD = "white"

        # ==========================================
        # 1. CAMPOS GENERALES (Tabla: Usuario)
        # ==========================================
        self.nombre = self._crear_input("Nombre(s)", width=350)
        
        # Apellidos en una sola fila para ahorrar espacio
        self.ap_paterno = self._crear_input("Apellido Paterno", width=165)
        self.ap_materno = self._crear_input("Apellido Materno", width=165)
        self.row_apellidos = ft.Row([self.ap_paterno, self.ap_materno], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        
        # Fecha e Identificador en una sola fila
        self.fecha_nacimiento = self._crear_input("Fecha Nacimiento (YYYY-MM-DD)", width=165)
        self.identificador = self._crear_input("Identificador Único", width=165)
        self.row_datos_extra = ft.Row([self.fecha_nacimiento, self.identificador], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        # ==========================================
        # 2. SELECTOR DE TIPO (El detonador)
        # ==========================================
        self.tipo_usuario = ft.Dropdown(
            label="Tipo de Usuario",
            width=350,
            border_radius=12,
            focused_border_color=self.AZUL,
            options=[
                ft.dropdown.Option("Alumno"),
                ft.dropdown.Option("Personal"),
                ft.dropdown.Option("Visitante"),
            ],
            on_change=self.cambiar_campos
        )

        # ==========================================
        # 3. CAMPOS ESPECÍFICOS (Subtablas)
        # ==========================================
        
        # Campos de Alumno
        self.matricula = self._crear_input("Matrícula", width=165)
        self.grupo = self._crear_input("Grado y Grupo", width=165)
        self.row_alumno = ft.Row([self.matricula, self.grupo], spacing=20, alignment=ft.MainAxisAlignment.CENTER, visible=False)
        
        # Campos de Personal
        self.n_plaza = self._crear_input("Número de plaza (n_plaza)", width=350, visible=False)
        
        # Campos de Visitante (La imagen se corta, asumo que no hay más campos)
        self.mensaje_visitante = ft.Text("✓ El visitante no requiere datos adicionales", color="green", visible=False)

        # Contenedor dinámico que refrescaremos
        self.contenedor_dinamico = ft.Column(
            controls=[self.row_alumno, self.n_plaza, self.mensaje_visitante],
            spacing=15, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.build_ui()

    # Herramienta para crear inputs rápido
    def _crear_input(self, label, width, visible=True): # <--- Agregamos visible=True aquí
        return ft.TextField(
            label=label, 
            width=width, 
            visible=visible, # <--- Y se lo pasamos al TextField aquí
            border_color="#D1D5DB", 
            border_radius=12,
            focused_border_color=self.AZUL, 
            text_style=ft.TextStyle(color=self.TEXT)
        )

    # Lógica para mostrar campos según la selección
    def cambiar_campos(self, e):
        tipo = self.tipo_usuario.value
        
        # Apagamos todo primero
        self.row_alumno.visible = False
        self.n_plaza.visible = False
        self.mensaje_visitante.visible = False
        
        # Prendemos lo que toca
        if tipo == "Alumno":
            self.row_alumno.visible = True
        elif tipo == "Personal":
            self.n_plaza.visible = True
        elif tipo == "Visitante":
            self.mensaje_visitante.visible = True
            
        # Actualizamos la vista
        self.contenedor_dinamico.update()
        self._page.update()

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def build_ui(self):
        # Ensamblado de todo el formulario
        formulario = ft.Column(
            [
                self.nombre,
                self.row_apellidos,
                self.row_datos_extra,
                ft.Divider(height=10, color="transparent"),
                self.tipo_usuario,
                self.contenedor_dinamico
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        card = ft.Container(
            bgcolor=self.CARD,
            padding=40,
            border_radius=30,
            width=700, # Un poco más ancho para que quepan bien las dos columnas
            shadow=ft.BoxShadow(blur_radius=20, color="black26"),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_1, size=50, color=self.AZUL),
                    ft.Text("Registro de usuario", size=26, weight="bold", color=self.TEXT),
                    ft.Text("Completa los datos base y selecciona el rol", size=14, color="gray"),
                    ft.Divider(height=15, color="transparent"),
                    
                    formulario,
                    
                    ft.Divider(height=15, color="transparent"),
                    ft.Row(
                        [
                            ft.OutlinedButton("Cancelar", on_click=self.cancelar, style=ft.ButtonStyle(color="red")),
                            ft.ElevatedButton("Guardar", bgcolor=self.AZUL, color="white", width=150)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER, spacing=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.content = ft.Row([card], alignment=ft.MainAxisAlignment.CENTER)

# Zona de pruebas solitaria
if __name__ == "__main__":
    def main(page: ft.Page):
        page.bgcolor = "#F0F4F8"
        page.scroll = "auto"
        page.add(PantallaRegistroUsuario(page))
    ft.app(target=main)
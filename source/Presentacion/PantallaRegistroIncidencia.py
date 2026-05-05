import flet as ft
import datetime
from Negocio.Utilidades.Validador import Validador
from Negocio.Utilidades.Herramientas import Herramientas
from Negocio.Controlador.ControladorRegistroIncidencia import ControladorRegistroIncidencia

class PantallaRegistroIncidencia(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)

        self.AZUL = "#3B82F6"
        self.GRIS_BORDE = "outline"          
        self.GRIS_TEXTO = "onSurfaceVariant" 
        self.TEXT = "onSurface"             
        self.CARD = "surface"  

        self.controlador = ControladorRegistroIncidencia(self)
        self.id_usuario_actual = None

        self._iniciar_controles()
        self.build_ui()

    def _iniciar_controles(self):
        self.txt_nombre = ft.TextField(
            label="Usuario encontrado", width=350, read_only=True,
            border_color="transparent", bgcolor="surfaceVariant",    
            color=self.TEXT, text_style=ft.TextStyle(weight="bold")
        )

        self.text_identificador = self._crear_input("Identificador (Matrícula/Plaza/Visitante)", 350)
        self.text_identificador.on_change = self.buscar_usuario_handler 

        self.drop_tipo = ft.Dropdown(
            value="PARCIAL", label="Tipo de incidencia",
            width=350, border_radius=12, border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            options=[ft.dropdown.Option("PARCIAL"), ft.dropdown.Option("DEFINITIVA")]
        )

        self.txt_desc = ft.TextField(
            label="Descripción", width=350, border_radius=12, 
            border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            multiline=True, min_lines=3, hint_text="Describe lo sucedido..."
        )

        self.drop_cat = ft.Dropdown(
            label="Categoría", width=165, border_radius=12, border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL, value="Libros", 
            options=[
                ft.dropdown.Option("Ruido"), ft.dropdown.Option("Equipo"),
                ft.dropdown.Option("Comportamiento"), ft.dropdown.Option("Libros")
            ],
            on_select=self.actualizar_vista_previa
        )

        self.icono_previa = ft.Icon(ft.Icons.WARNING, color=self.AZUL, size=30)
        self.txt_previa = ft.Text("Libros", size=13, weight="bold")
        
        self.container_previa = ft.Container(
            content=ft.Row([self.icono_previa, self.txt_previa], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            width=165, height=60, bgcolor="surfaceVariant", border_radius=12, padding=10
        )

        self.row_cat_previa = ft.Row([self.drop_cat, self.container_previa], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        self.txt_lugar = self._crear_input("Lugar (Ej. Cubículo 1)", width=350)
        self.txt_mensaje = ft.Text("", size=15, weight="w500", text_align=ft.TextAlign.CENTER)

    def _crear_input(self, label, width):
        return ft.TextField(
            label=label, width=width, border_color=self.GRIS_BORDE,
            border_radius=12, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT)
        )

    #acciones
    def buscar_usuario_handler(self, e):
        identificador = self.text_identificador.value.strip()
        
        if not identificador:
            self.limpiar_usuario_encontrado()
            return
            
        usuario = self.controlador.buscar_usuario(identificador)
        
        if usuario:
            self.txt_nombre.value = f"{usuario['nombre']} {usuario['ap_paterno']} {usuario['ap_materno']}"
            self.id_usuario_actual = usuario["id_usuario"]
            self.mostrar_mensaje("", "") # Limpia errores previos
        else:
            self.txt_nombre.value = "Usuario no encontrado"
            self.id_usuario_actual = None
            self.mostrar_mensaje("❌ Identificador no válido", "red")
            
        self.update()

    def guardar_handler(self, e):
        campos = [
            (self.text_identificador, "Ingresa un identificador"),
            (self.drop_tipo, "Selecciona el tipo"),
            (self.drop_cat, "Selecciona la categoría"),
            (self.txt_desc, "Ingresa una descripción"),
            (self.txt_lugar, "Ingresa el lugar")
        ]
        
        valido, mensaje = Validador.validar(campos)
        if not valido:
            self.mostrar_mensaje(f"❌ {mensaje}", "orange")
            return
            
        if not self.id_usuario_actual:
            self.mostrar_mensaje("❌ Debes buscar un usuario válido primero", "orange")
            return

        datos_incidencia = {
            "id_usuario": self.id_usuario_actual,
            "tipo": self.drop_tipo.value.upper().strip(),
            "motivo": self.drop_cat.value,
            "descripcion": self.txt_desc.value.strip(),
            "lugar": self.txt_lugar.value.strip()
        }

        exito, respuesta = self.controlador.guardar_incidencia(datos_incidencia)
        
        if exito:
            fecha_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            self.mostrar_mensaje(f"✅ Incidencia para {self.txt_nombre.value} guardada\n🕒 {fecha_str}", "green")
            self.limpiar_form()
        else:
            self.mostrar_mensaje(f"❌ {respuesta}", "red")

    # UTILIDADES VISUALES INTERNAS
    def limpiar_usuario_encontrado(self):
        self.txt_nombre.value = ""
        self.id_usuario_actual = None
        self.txt_mensaje.value = ""
        self.update()

    def actualizar_vista_previa(self, e):
        cat = self.drop_cat.value
        if not cat: return
        
        iconos = {
            "Ruido": ft.Icons.VOLUME_UP,
            "Equipo": ft.Icons.COMPUTER,
            "Comportamiento": ft.Icons.PERSON_OFF,
            "Libros": ft.Icons.WARNING
        }
        
        self.txt_previa.value = cat
        self.icono_previa.icon = iconos.get(cat, ft.Icons.WARNING)
        self.update()

    def mostrar_mensaje(self, texto, color):
        self.txt_mensaje.value = texto
        self.txt_mensaje.color = color if texto else "transparent"
        self.update()

    def limpiar_form(self):
        Herramientas.limpiar_controles([
            self.text_identificador, self.txt_nombre, self.txt_desc, self.txt_lugar
        ])
        Herramientas.reset_dropdowns([self.drop_tipo, self.drop_cat])
        
        self.drop_tipo.value = "PARCIAL"
        self.drop_cat.value = "Libros"
        self.id_usuario_actual = None
        self.actualizar_vista_previa(None)
        self.update()

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def build_ui(self):
        formulario = ft.Column([
            self.txt_nombre, self.text_identificador, self.drop_tipo,
            self.txt_desc, self.row_cat_previa, self.txt_lugar  
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        inner_card = ft.Container(
            bgcolor=self.CARD, padding=40, border_radius=30,
            shadow=ft.BoxShadow(blur_radius=20, color="black26"),
            content=ft.Column([
                ft.Icon(ft.Icons.ADD_ALERT_ROUNDED, size=50, color=self.AZUL),
                ft.Text("Registro de Incidencia", size=26, weight="bold", color=self.TEXT),
                ft.Text("Reporte detallado de irregularidades", size=14, color=self.GRIS_TEXTO),
                ft.Divider(height=15, color="transparent"),
                formulario,
                ft.Divider(height=15, color="transparent"),
                ft.Row([
                    ft.OutlinedButton("Cancelar", on_click=self.cancelar, style=ft.ButtonStyle(color="red")),
                    ft.ElevatedButton(
                        "Guardar Reporte", bgcolor=self.AZUL, color="white", width=180,
                        on_click=self.guardar_handler
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                self.txt_mensaje
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        self.content = ft.Column([
            ft.Container(
                width=660, border_radius=40, padding=30,
                gradient=ft.LinearGradient(
                    colors=["#cfe8ff", "#9ec9ff"], begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1)
                ),
                content=inner_card
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           scroll=ft.ScrollMode.AUTO, expand=True)
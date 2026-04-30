import flet as ft
import datetime
from Negocio.Modelo.Alumno import Alumno
from Negocio.Modelo.Personal import Personal
from Negocio.Modelo.Visitante import Visitante

from Persistencia.Postgres.CatalogoRepository import CatalogoRepository

from Negocio.Controlador.ControladorRegistroUsuario import ControladorPantallaRegistroUsuario


class PantallaRegistroUsuario(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self.control = ControladorPantallaRegistroUsuario(self)
        self.catalogo_repo = CatalogoRepository()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True


        self.mensaje = ft.Container(
            visible=False,
            padding=10,
            border_radius=10,
            alignment=ft.Alignment(0, 0)        )

        self.usuarios = {
            "Alumno": Alumno(),
            "Personal": Personal(),
            "Visitante": Visitante()
        }

        self.AZUL = "#3B82F6"
        self.TEXT = "#111827"
        self.CARD = "white"

        self.nombre = self._crear_input("Nombre(s)", width=350)

        self.ap_paterno = self._crear_input("Apellido Paterno", width=165)
        self.ap_materno = self._crear_input("Apellido Materno", width=165)

        self.row_apellidos = ft.Row(
            [self.ap_paterno, self.ap_materno],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.calendario = ft.DatePicker(
            on_change=self.seleccionar_fecha,
            first_date=datetime.datetime(1950, 1, 1),
            last_date=datetime.datetime.now(),
        )
        self._page.overlay.append(self.calendario)

        self.fecha_nacimiento = ft.TextField(
            label="Fecha Nacimiento",
            width=350,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.abrir_calendario
        )

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
            on_select=self.cambiar_campos
        )

        self.matricula = self._crear_input("Matrícula", width=350, visible=False)

        self.licenciatura = ft.Dropdown(
            label="Licenciatura",
            width=350,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[],
            visible=False,
            on_select=self.on_carrera_change
        )

        self.semestre = ft.Dropdown(
            label="Semestre",
            width=165,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[],
            on_select=self.on_semestre_change
        )

        self.grupo = ft.Dropdown(
            label="Grupo",
            width=165,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[]
        )

        self.row_semestre_grupo = ft.Row(
            [self.semestre, self.grupo],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

        self.n_plaza = self._crear_input("Número de plaza", width=350, visible=False)

        self.institucion = ft.Dropdown(
            label="Institución",
            width=350,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[],
            visible=False
        )

        self.identificador_preview = ft.TextField(
            label="Identificador",
            width=350,
            read_only=True,
            visible=False,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
        )

        self.contenedor_dinamico = ft.Column(
            controls=[self.matricula, self.licenciatura, self.row_semestre_grupo, self.n_plaza, self.institucion, self.identificador_preview],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.build_ui()

    def did_mount(self):
        self.cargar_catalogos()

    def cargar_catalogos(self):

        carreras = self.catalogo_repo.obtener_carreras()
        self.licenciatura.options = [
            ft.dropdown.Option(str(c["id_carrera"]), text=c["nombre_carrera"])
            for c in carreras
        ]

        semestres = self.catalogo_repo.obtener_semestres()
        self.semestre.options = [
            ft.dropdown.Option(str(s["id_semestre"]), text=s["semestre"])
            for s in semestres
        ]

        instituciones = self.catalogo_repo.obtener_instituciones()
        self.institucion.options = [
            ft.dropdown.Option(str(i["id_institucion"]), text=i["nombre_institucion"])
            for i in instituciones
        ]

        self.update()

    def on_carrera_change(self, e):
        self.actualizar_grupos()

    def on_semestre_change(self, e):
        self.actualizar_grupos()

    def actualizar_grupos(self):
        if not self.semestre.value or not self.licenciatura.value:
            return

        grupos = self.catalogo_repo.obtener_grupos(
            self.licenciatura.value,
            self.semestre.value
        )

        self.grupo.options = [
            ft.dropdown.Option(str(g["id_grupo"]), text=g["grupo"])
            for g in grupos
        ]

        self.grupo.value = None
        self.update()

    def preparar_identificador(self):
        tipo = self.tipo_usuario.value

        if tipo == "Alumno":
            pass
        elif tipo == "Personal":
            self.matricula.value = self.n_plaza.value
        elif tipo == "Visitante":
            self.matricula.value = self.institucion.value

    def guardar_con_preparacion(self, e):

        # 🔹 Validación
        if not self.validar_campos():
            self.mostrar_mensaje("Completa todos los campos obligatorios", "orange")
            return

        try:
            self.preparar_identificador()

            resultado = self.control.guardar_usuario(e)

            if resultado:
                identificador = resultado["identificador"]

                if identificador:
                    self.identificador_preview.value = identificador   # 🔥 CLAVE
                    self.identificador_preview.visible = True
                    mensaje = f"Usuario registrado: {identificador}"
                else:
                    mensaje = "Usuario registrado correctamente"

                self.mostrar_mensaje(mensaje, "green")
                self.update()

                self.limpiar_campos()

        except Exception as ex:

            if "usuario_identificador_key" in str(ex):
                self.mostrar_mensaje("El usuario ya está registrado", "red")
            else:
                self.mostrar_mensaje("Error al guardar el usuario", "red")

            print("ERROR:", ex)

    def _crear_input(self, label, width, visible=True):
        return ft.TextField(
            label=label,
            width=width,
            visible=visible,
            border_color="#D1D5DB",
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            value=""
        )

    def seleccionar_fecha(self, e):
        if self.calendario.value:
            self.fecha_nacimiento.value = self.calendario.value.strftime("%Y-%m-%d")
            self.fecha_nacimiento.update()

    def abrir_calendario(self, e):
        self.calendario.open = True
        self._page.update()

    def cambiar_campos(self, e):
        tipo = self.tipo_usuario.value

        self.tipo_usuario.text_style = ft.TextStyle(color=self.TEXT)
        self.tipo_usuario.label_style = ft.TextStyle(color=self.TEXT)

        self.matricula.visible = False
        self.licenciatura.visible = False
        self.row_semestre_grupo.visible = False
        self.n_plaza.visible = False
        self.institucion.visible = False

        if tipo == "Alumno":
            self.matricula.visible = True
            self.licenciatura.visible = True
            self.row_semestre_grupo.visible = True
        elif tipo == "Personal":
            self.n_plaza.visible = True
        elif tipo == "Visitante":
            self.institucion.visible = True

            siguiente = self.control.obtener_siguiente_vis()
            self.identificador_preview.value = siguiente
            self.identificador_preview.visible = True
        self.update()

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def mostrar_mensaje(self, texto, color):
        icono = ft.Icons.CHECK_CIRCLE if color == "green" else ft.Icons.ERROR

        bg = "#DCFCE7" if color == "green" else "#FEE2E2" if color == "red" else "#FEF9C3"

        self.mensaje.bgcolor = bg

        self.mensaje.content = ft.Row(
            [
                ft.Icon(icono, color=color),
                ft.Text(texto, color="black", size=14)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.mensaje.visible = True
        self.update()
        
    def validar_campos(self):
        if not self.nombre.value or not self.ap_paterno.value:
            return False

        if not self.tipo_usuario.value:
            return False

        tipo = self.tipo_usuario.value

        if tipo == "Alumno":
            if not self.matricula.value or not self.grupo.value:
                return False

        elif tipo == "Personal":
            if not self.n_plaza.value:
                return False

        elif tipo == "Visitante":
            if not self.institucion.value:
                return False

        return True
        
    def limpiar_campos(self):
        self.nombre.value = ""
        self.ap_paterno.value = ""
        self.ap_materno.value = ""
        self.fecha_nacimiento.value = ""

        self.tipo_usuario.value = None

        self.matricula.value = ""
        self.n_plaza.value = ""
        self.institucion.value = None

        self.semestre.value = None
        self.grupo.value = None
        self.licenciatura.value = None


        self.update()

    def build_ui(self):
        formulario = ft.Column(
            [
                self.nombre,
                self.row_apellidos,
                self.fecha_nacimiento,
                ft.Divider(height=10, color="transparent"),
                self.tipo_usuario,
                self.contenedor_dinamico
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        inner_card = ft.Container(
            bgcolor=self.CARD,
            padding=40,
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=20, color="black26"),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_1, size=50, color=self.AZUL),
                    ft.Text("Registro de usuario", size=26, weight="bold", color=self.TEXT),
                    ft.Text("Completa los datos base y selecciona el rol", size=14, color="black"),
                    ft.Divider(height=15, color="transparent"),

                    formulario,

                    ft.Divider(height=15, color="transparent"),
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                "Cancelar",
                                on_click=self.cancelar,
                                style=ft.ButtonStyle(color="red")
                            ),
                            ft.ElevatedButton(
                                "Guardar",
                                bgcolor=self.AZUL,
                                color="white",
                                width=150,
                                data="btn_guardar",
                                on_click=self.guardar_con_preparacion 
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),
                    self.mensaje,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        card = ft.Container(
            width=660,
            border_radius=40,
            padding=30,
            gradient=ft.LinearGradient(
                colors=["#cfe8ff", "#9ec9ff"],
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1)
            ),
            content=inner_card
        )

        self.content = ft.Column(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
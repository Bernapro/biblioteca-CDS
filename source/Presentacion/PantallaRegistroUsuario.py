import flet as ft
import datetime
from Negocio.Modelo.Alumno import Alumno

from Negocio.catalogos_service import (
    obtener_carreras,
    obtener_semestres,
    obtener_grupos_por_semestre,
    obtener_instituciones,
    obtener_grupos_filtrados  # 🔥 NUEVO
)

from Negocio.Controlador.ControladorRegistroUsuario import ControladorPantallaRegistroUsuario


class PantallaRegistroUsuario(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self.control = ControladorPantallaRegistroUsuario(self)
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True

        self.usuarios= {"Alumno": Alumno(), "Personal": None, "Visitante": None}
        
        self.AZUL = "#3B82F6"
        self.TEXT = "#111827"
        self.CARD = "white"

        self.nombre = self._crear_input("Nombre(s)", width=350)

        self.ap_paterno = self._crear_input("Apellido Paterno", width=165)
        self.ap_materno = self._crear_input("Apellido Materno", width=165)

        self.row_apellidos = ft.Row([self.ap_paterno, self.ap_materno], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
        
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
            on_select=self.on_carrera_change  # 🔥 NUEVO
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
        
        self.row_semestre_grupo = ft.Row([self.semestre, self.grupo], spacing=20, alignment=ft.MainAxisAlignment.CENTER, visible=False)
        
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

        self.contenedor_dinamico = ft.Column(
            controls=[self.matricula, self.licenciatura, self.row_semestre_grupo, self.n_plaza, self.institucion],
            spacing=15, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.build_ui()

    def did_mount(self):
        self.cargar_catalogos()

    def cargar_catalogos(self):

        self.licenciatura.options = [
            ft.dropdown.Option(str(c[0]), text=c[1])
            for c in obtener_carreras()
        ]

        self.semestre.options = [
            ft.dropdown.Option(str(s[0]), text=s[1])
            for s in obtener_semestres()
        ]

        self.institucion.options = [
            ft.dropdown.Option(str(i[0]), text=i[1])
            for i in obtener_instituciones()
        ]

        self.update()

    # 🔥 NUEVO
    def on_carrera_change(self, e):
        self.actualizar_grupos()

    #CORREGIDO
    def on_semestre_change(self, e):
        self.actualizar_grupos()

    # NUEVO CORE
    def actualizar_grupos(self):
        if not self.semestre.value or not self.licenciatura.value:
            return

        grupos = obtener_grupos_filtrados(
            self.licenciatura.value,
            self.semestre.value
        )

        self.grupo.options = [
            ft.dropdown.Option(str(g[0]), text=g[1])
            for g in grupos
        ]

        self.grupo.value = None
        self.update()

    def _crear_input(self, label, width, visible=True):
        return ft.TextField(
            label=label, 
            width=width, 
            visible=visible,
            border_color="#D1D5DB", 
            border_radius=12,
            focused_border_color=self.AZUL, 
            text_style=ft.TextStyle(color=self.TEXT),
            value= ""
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
            
        self.update()

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

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
                                on_click=self.control.guardar_usuario
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
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
import flet as ft
import datetime
import threading 
from Negocio.Utilidades.Validador import Validador
from Negocio.Utilidades.Herramientas import Herramientas
from Negocio.Controlador.ControladorRegistroUsuario import ControladorPantallaRegistroUsuario

class PantallaRegistroUsuario(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self.controlador = ControladorPantallaRegistroUsuario(self)
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)
        
        self.mensaje = ft.Container(
            visible=False,
            padding=10,
            border_radius=10,
            alignment=ft.Alignment(0, 0)        
        )

        self.AZUL = "#3B82F6"
        self.TEXT = "onSurface"
        self.TEXT_SECONDARY = "onSurfaceVariant"
        self.CARD = "surface"
        self.GRIS_BORDE = "outline"

        self.nombre = self._crear_input("Nombre(s)", width=350)
        self.nombre.on_submit = self._ignorar_escaneo

        self.ap_paterno = self._crear_input("Apellido Paterno", width=165)

        self.ap_paterno.on_submit = self._ignorar_escaneo

        self.ap_materno = self._crear_input("Apellido Materno", width=165)
        self.ap_materno.on_submit = self._ignorar_escaneo

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
            border_color=self.GRIS_BORDE,
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
        self.matricula.on_submit = self._procesar_escaneo_matricula

        self.licenciatura = ft.Dropdown(
            label="Licenciatura",
            width=350,
            border_color=self.GRIS_BORDE,
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[],
            visible=False,
            on_select=self.on_carrera_o_semestre_change 
        )

        self.semestre = ft.Dropdown(
            label="Semestre",
            width=165,
            border_color=self.GRIS_BORDE,
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            options=[],
            on_select=self.on_carrera_o_semestre_change 
        )

        self.grupo = ft.Dropdown(
            label="Grupo",
            width=165,
            border_color=self.GRIS_BORDE,
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
        self.n_plaza.on_submit = self._procesar_escaneo_plaza

        self.institucion = ft.Dropdown(
            label="Institución",
            width=350,
            border_color=self.GRIS_BORDE,
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

            border_color="transparent",
            bgcolor="surfaceVariant",

            color=self.TEXT,

            text_style=ft.TextStyle(
                weight="bold"
            )
        )

        self.contenedor_dinamico = ft.Column(
            controls=[self.matricula, self.licenciatura, self.row_semestre_grupo, self.n_plaza, self.institucion, self.identificador_preview],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.build_ui()

    def did_mount(self):
        carreras, semestres, instituciones = self.controlador.cargar_datos_iniciales()
        self.poblar_catalogos(carreras, semestres, instituciones)

    def poblar_catalogos(self, carreras, semestres, instituciones):
        self.licenciatura.options = [ft.dropdown.Option(str(c["id_carrera"]), text=c["nombre_carrera"]) for c in carreras]
        self.semestre.options = [ft.dropdown.Option(str(s["id_semestre"]), text=s["semestre"]) for s in semestres]
        self.institucion.options = [ft.dropdown.Option(str(i["id_institucion"]), text=i["nombre_institucion"]) for i in instituciones]
        self.update()

    def poblar_grupos(self, grupos):
        self.grupo.options = [ft.dropdown.Option(str(g["id_grupo"]), text=g["grupo"]) for g in grupos]
        self.grupo.value = None
        self.update()

    def on_carrera_o_semestre_change(self, e):
        grupos = self.controlador.actualizar_grupos(
            self.licenciatura.value,
            self.semestre.value
        )
        self.poblar_grupos(grupos)

    def _obtener_identificador_final(self, tipo):
        if tipo == "Alumno": return self.matricula.value
        if tipo == "Personal": return self.n_plaza.value
        if tipo == "Visitante": return self.institucion.value
        return None
    
    def _ignorar_escaneo(self, e):
        self.mostrar_mensaje("Usa el escáner solo para Matrícula o N. de Plaza.", "orange")
        e.control.value = "" 
        e.control.update()

    def _procesar_escaneo_matricula(self, e):
        valor = e.control.value.strip()
        if valor: 
            e.control.border_color = "#22C55E" 
            e.control.update()
            self.mostrar_mensaje(f"Matrícula {valor} escaneada con éxito", "green")
            self.page.set_focus(self.licenciatura)
            self.licenciatura.update()
            self.update()

    def _procesar_escaneo_plaza(self, e):
        valor = e.control.value.strip()
        if valor:
            e.control.border_color = "#22C55E" 
            e.control.update()
            self.mostrar_mensaje(f"Plaza {valor} escaneada con éxito", "green")
            self.update()

    def guardar_con_preparacion(self, e):
        campos = [
            (self.nombre, None),
            (self.ap_paterno, None),
            (self.ap_materno, None),
            (self.fecha_nacimiento, None),
            (self.tipo_usuario, None),
        ]

        tipo = self.tipo_usuario.value

        if tipo == "Alumno":
            campos.extend([
                (self.matricula, None),
                (self.licenciatura, None),
                (self.semestre, None),
                (self.grupo, None),
            ])
        elif tipo == "Personal":
            campos.append((self.n_plaza, None))
        elif tipo == "Visitante":
            campos.append((self.institucion, None))

        valido, mensaje = Validador.validar(campos)

        if not valido:
            self.mostrar_mensaje(mensaje, "orange")
            return

        datos_usuario = {
            "nombre": self.nombre.value,
            "ap_paterno": self.ap_paterno.value,
            "ap_materno": self.ap_materno.value,
            "fecha_nacimiento": self.fecha_nacimiento.value,
            "tipo_usuario": tipo.upper() if tipo else None,
            "identificador": self._obtener_identificador_final(tipo),
            "semestre": self.semestre.value,
            "grupo": self.grupo.value,
            "institucion": self.institucion.value,
            "licenciatura": self.licenciatura.value
        }

        try:
            exito, identificador = self.controlador.guardar_usuario(datos_usuario)

            if exito:
                if identificador:
                    self.identificador_preview.value = identificador
                    self.identificador_preview.visible = True
                    mensaje = f"Usuario registrado: {identificador}"
                else:
                    mensaje = "Usuario registrado correctamente"

                self.mostrar_mensaje(mensaje, "green")
                self.update()
                self.limpiar_campos()

        except ValueError as ve:
            self.mostrar_mensaje(str(ve), "red")
        except Exception as ex:
            self.mostrar_mensaje("Error al guardar el usuario", "red")
            print("ERROR:", ex)

    def _crear_input(self, label, width, visible=True):
        return ft.TextField(
            label=label,
            width=width,
            visible=visible,
            border_color=self.GRIS_BORDE,
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

        Herramientas.reset_dropdowns([
            self.institucion,
            self.grupo,
            self.semestre,
            self.licenciatura
        ])

        Herramientas.ocultar([
            self.matricula,
            self.licenciatura,
            self.row_semestre_grupo,
            self.n_plaza,
            self.institucion,
            self.identificador_preview
        ])

        if tipo == "Alumno":
            Herramientas.mostrar([
                self.matricula,
                self.licenciatura,
                self.row_semestre_grupo
            ])
        elif tipo == "Personal":
            Herramientas.mostrar([self.n_plaza])
        elif tipo == "Visitante":
            Herramientas.mostrar([self.institucion])
            self.identificador_preview.value = self.controlador.obtener_siguiente_vis()
            self.identificador_preview.visible = True
        self.update()

        #  asíncrono 
        def forzar_foco():
            import time
            time.sleep(0.2) 
            if tipo == "Alumno":
                self.matricula.focus()
                self.matricula.update()
            elif tipo == "Personal":
                self.n_plaza.focus()
                self.n_plaza.update()

        
        threading.Thread(target=forzar_foco, daemon=True).start()

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def mostrar_mensaje(self, texto, color):
        es_exito = (color == "green")
        color_real = "#22C55E" if es_exito else "error" if color == "red" else "#F59E0B"
        icono = ft.Icons.CHECK_CIRCLE if es_exito else ft.Icons.ERROR

        self.mensaje.bgcolor = "transparent"
        self.mensaje.border = ft.border.all(1, color_real)
        self.mensaje.content = ft.Row(
            [
                ft.Icon(icono, color=color_real),
                ft.Text(texto, color=self.TEXT, size=14)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.mensaje.visible = True
        self.update()
        
    def limpiar_campos(self):
            Herramientas.limpiar_controles([
                self.nombre,
                self.row_apellidos,
                self.fecha_nacimiento,
                self.contenedor_dinamico
            ])
            
            Herramientas.reset_dropdown(self.tipo_usuario)
            
            Herramientas.reset_dropdowns([
                self.institucion,
                self.grupo,
                self.semestre,
                self.licenciatura
            ])
            
            self.cambiar_campos(None)
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
                    ft.Text("Completa los datos base y selecciona el rol", size=14, color=self.TEXT_SECONDARY),
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
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
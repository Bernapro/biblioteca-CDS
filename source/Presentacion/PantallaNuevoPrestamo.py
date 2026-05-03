import flet as ft
import datetime

class PantallaNuevoPrestamo(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)

        # ===== COLORES ADAPTABLES AL MODO OSCURO (Flet 0.84.0) =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#22C55E"
        self.GRIS_BORDE = "outline"          
        self.GRIS_TEXTO = "onSurfaceVariant" 
        self.TEXT = "onSurface"              
        self.CARD = "surface"                

        # === CONTROLES DEL FORMULARIO ===
        
        # 1. Alumno
        self.txt_matricula = ft.TextField(
            hint_text="Ej. 100025787",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            expand=True, height=50, content_padding=10
        )
        self.btn_buscar_alumno = ft.OutlinedButton("Buscar", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)), on_click=self.buscar_alumno)
        
        # Tarjeta de resultado del alumno
        self.card_alumno = ft.Container(
        )

        # 2. Libro
        self.txt_adquisicion = ft.TextField(
            hint_text="Ej. ADQ-001245",
            prefix_icon=ft.Icons.MENU_BOOK,
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            expand=True, height=50, content_padding=10
        )
        self.btn_buscar_libro = ft.OutlinedButton("Buscar", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)))

        # === CONTENEDOR CON SCROLL PARA LOS LIBROS ===
        self.lista_libros = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
        self.radio_group_libros = ft.RadioGroup(content=self.lista_libros)

        self.contenedor_resultados = ft.Container(
            content=self.radio_group_libros,
            height=250, # Altura fija para forzar el scroll si hay muchos
            border=ft.border.all(1, self.GRIS_BORDE),
            border_radius=12,
            padding=10,
            bgcolor="surface"
        )

        # 3. Calendarios
        self.picker_fecha_prestamo = ft.DatePicker(
            on_change=self.seleccionar_fecha_prestamo,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31)
        )
        self.picker_fecha_limite = ft.DatePicker(
            on_change=self.seleccionar_fecha_limite,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31)
        )
        self._page.overlay.extend([self.picker_fecha_prestamo, self.picker_fecha_limite])

        # Campos de texto de fechas
        self.txt_fecha_prestamo = ft.TextField(
            label="Fecha de préstamo",
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT), prefix_icon=ft.Icons.CALENDAR_TODAY,
            expand=True, height=55, read_only=True, value=datetime.datetime.now().strftime("%d/%b/%Y"),
            on_click=self.abrir_picker_prestamo
        )
        self.txt_fecha_limite = ft.TextField(
            label="Fecha límite (7 días)",
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT), prefix_icon=ft.Icons.CALENDAR_MONTH,
            expand=True, height=55, read_only=True, value=(datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d/%b/%Y"),
            on_click=self.abrir_picker_limite
        )

        # Poblar libros de prueba
        self.cargar_libros_prueba()
        self.build_ui()

    def buscar_alumno(self, e):
        matricula_buscar = self.txt_matricula.value
        
        # =========================================================
        # AQUÍ TU AMIGO CONECTARÁ LA API O LA BASE DE DATOS
        # respuesta = api.buscar_alumno(matricula_buscar)
        # =========================================================
        
        # Simulamos que la API devuelve un resultado exitoso:
        if matricula_buscar:
            nombre = "Carlos Daniel" # Reemplazar con: respuesta["nombre"]
            carrera_semestre = "Ingeniería en Sistemas | 2°A" # Reemplazar con: respuesta["carrera"] + " | " + respuesta["semestre"]
            
            # Actualizamos la tarjeta dinámicamente con los datos reales
            self.card_alumno.bgcolor = "surfaceVariant"
            self.card_alumno.border_radius = 12
            self.card_alumno.padding = 15
            self.card_alumno.content = ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=self.AZUL),
                ft.Column([
                    ft.Text(nombre, weight="bold", size=16, color=self.TEXT),
                    ft.Text(carrera_semestre, size=13, color=self.GRIS_TEXTO)
                ], expand=True, spacing=2),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, size=14, color=self.VERDE), ft.Text("Alumno encontrado", size=12, color=self.VERDE, weight="bold")], spacing=4),
                    bgcolor="#D1FAE5", 
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    border_radius=15
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
        else:
            # Lógica en caso de que no se encuentre el alumno o el campo esté vacío
            self.card_alumno.content = ft.Text("Por favor, ingresa una matrícula válida.", color="red")
            
        self.update()

    def seleccionar_fecha_prestamo(self, e):
        if self.picker_fecha_prestamo.value:
            self.txt_fecha_prestamo.value = self.picker_fecha_prestamo.value.strftime("%d/%b/%Y")
            self.txt_fecha_prestamo.update()

    def seleccionar_fecha_limite(self, e):
        if self.picker_fecha_limite.value:
            self.txt_fecha_limite.value = self.picker_fecha_limite.value.strftime("%d/%b/%Y")
            self.txt_fecha_limite.update()

    def abrir_picker_prestamo(self, e):
        self.picker_fecha_prestamo.open = True
        self._page.update()

    def abrir_picker_limite(self, e):
        self.picker_fecha_limite.open = True
        self._page.update()

    def cargar_libros_prueba(self):
        # Datos simulados basados en tu diseño
        libros = [
            ("El principito", "Antoine de Saint-Exupéry", "ADQ-001245"),
            ("1984", "George Orwell", "ADQ-001246"),
            ("Cien años de soledad", "Gabriel García Márquez", "ADQ-001247"),
            ("El alquimista", "Paulo Coelho", "ADQ-001248"),
            ("Rayuela", "Julio Cortázar", "ADQ-001249")
        ]
        colores = ["#3B82F6", "#EF4444", "#F59E0B", "#10B981", "#8B5CF6"]

        for i, (titulo, autor, adq) in enumerate(libros):
            self.lista_libros.controls.append(
                ft.Container(
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, self.GRIS_BORDE),
                    content=ft.Row([
                        ft.Container(content=ft.Icon(ft.Icons.MENU_BOOK, color=colores[i%len(colores)], size=25), bgcolor="surfaceVariant", padding=10, border_radius=8),
                        ft.Column([
                            ft.Text(titulo, weight="bold", color=self.TEXT),
                            ft.Text(f"Autor: {autor} \nNo. Adquisición: {adq}", size=11, color=self.GRIS_TEXTO),
                        ], expand=True, spacing=1),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.VERDE, size=14),
                            ft.Text("Disponible", color=self.VERDE, size=12, weight="bold")
                        ], spacing=4),
                        ft.Radio(value=adq, active_color=self.AZUL)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            )

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def build_ui(self):
        formulario = ft.Column(
            [
                # SECCIÓN 1
                ft.Text("1. Matrícula del alumno", weight="bold", color=self.TEXT),
                ft.Row([self.txt_matricula, self.btn_buscar_alumno], spacing=10),
                self.card_alumno,
                
                ft.Divider(height=15, color="transparent"),
                
                # SECCIÓN 2
                ft.Text("2. Número de adquisición del ejemplar", weight="bold", color=self.TEXT),
                ft.Row([self.txt_adquisicion, self.btn_buscar_libro], spacing=10),
                ft.Text("Selecciona el libro (Ejemplares disponibles):", size=12, color=self.GRIS_TEXTO),
                self.contenedor_resultados,

                ft.Divider(height=15, color="transparent"),

                # SECCIÓN 3
                ft.Row([self.txt_fecha_prestamo, self.txt_fecha_limite], spacing=20)
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )

        inner_card = ft.Container(
            bgcolor=self.CARD,
            padding=40,
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=20, color="black26"),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MENU_BOOK, size=50, color=self.AZUL),
                    ft.Text("Nuevo préstamo", size=26, weight="bold", color=self.TEXT),
                    ft.Text("Registra un préstamo de libro", size=14, color=self.GRIS_TEXTO),
                    ft.Divider(height=20, color="transparent"),
                    
                    formulario, # Insertamos el formulario completo
                    
                    ft.Divider(height=20, color="transparent"),
                    ft.Row(
                        [
                            ft.OutlinedButton("Cancelar", on_click=self.cancelar, style=ft.ButtonStyle(color="onSurface")),
                            ft.ElevatedButton(
                                "Registrar préstamo",
                                bgcolor=self.AZUL, color="white", width=200,
                                on_click=lambda _: print("Préstamo registrado")
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        self.content = ft.Column(
            [
                # Contenedor exterior idéntico al de Incidencias
                ft.Container(
                    width=700, border_radius=40, padding=30,
                    bgcolor="transparent", # Hereda el modo oscuro de la pantalla principal
                    content=inner_card
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
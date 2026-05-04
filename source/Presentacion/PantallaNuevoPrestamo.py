import flet as ft
import datetime
from Negocio.Controlador.ControladorNuevoPrestamo import ControladorNuevoPrestamo

class PantallaNuevoPrestamo(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)

        # Instanciamos el controlador
        self.controlador = ControladorNuevoPrestamo(self)
        self.libros_seleccionados = {}   # {adq: (titulo, autor, adq)}
        self.libros_cache = []
        
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
        self.btn_buscar_alumno = ft.OutlinedButton("Buscar", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)), on_click=self.controlador.buscar_alumno)
        
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

        self.btn_buscar_libro = ft.OutlinedButton(
            "Buscar",
            icon=ft.Icons.SEARCH,
            style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=self.buscar_libros
        )

        # === CONTENEDOR CON SCROLL PARA LOS LIBROS ===
        self.lista_libros = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

        self.contenedor_resultados = ft.Container(
            content=self.lista_libros,
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
        )
        self.txt_fecha_limite = ft.TextField(
            label="Fecha límite (7 días)",
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT), prefix_icon=ft.Icons.CALENDAR_MONTH,
            expand=True, height=55, read_only=True, value=(datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d/%b/%Y"),
            on_click=self.abrir_picker_limite
        )
##variable proxima si van a usar la fecha inicio para algo
        self.fecha_prestamo = datetime.datetime.now()
        self.txt_fecha_prestamo.value = self.fecha_prestamo.strftime("%d/%b/%Y")
        
        # Poblar libros de prueba
        self.build_ui()


    def crear_item_libro(self, titulo, autor, adq):
        return ft.Container(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, self.GRIS_BORDE),
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.MENU_BOOK, color=self.AZUL, size=25),
                    bgcolor="surfaceVariant",
                    padding=10,
                    border_radius=8
                ),
                ft.Column([
                    ft.Text(titulo, weight="bold", color=self.TEXT),
                    ft.Text(f"Autor: {autor} \nNo. Adquisición: {adq}", size=11, color=self.GRIS_TEXTO),
                ], expand=True, spacing=1),
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.VERDE, size=14),
                    ft.Text("Disponible", color=self.VERDE, size=12, weight="bold")
                ], spacing=4),
                ft.Checkbox(
                    value=adq in self.libros_seleccionados,
                    on_change=lambda e, l=(titulo, autor, adq): self.toggle_libro(l, e.control.value)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def actualizar_lista(self):
        self.lista_libros.controls.clear()

        usados = set()

        # 🔹 Seleccionados primero
        for adq, libro in self.libros_seleccionados.items():
            self.lista_libros.controls.append(
                self.crear_item_libro(*libro)
            )
            usados.add(adq)

        # 🔹 Resultados de búsqueda
        for libro in self.libros_cache:
            if libro[2] not in usados:
                self.lista_libros.controls.append(
                    self.crear_item_libro(*libro)
                )

        if self.page:
            self.update()

    def buscar_libros(self, e):
        filtro = self.txt_adquisicion.value.lower()
        libros = self.controlador.obtener_libros_prueba()

        if filtro:
            libros = [l for l in libros if filtro in l[2].lower()]

        self.libros_cache = libros
        self.actualizar_lista()

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

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def toggle_libro(self, libro, checked):
        adq = libro[2]

        if checked:
            self.libros_seleccionados[adq] = libro
        else:
            self.libros_seleccionados.pop(adq, None)

        self.actualizar_lista()  

    def did_mount(self):
        self.buscar_libros(None)

    def build_ui(self):
        formulario = ft.Column(
            [
                # SECCIÓN 1
                ft.Text("Matrícula del alumno", weight="bold", color=self.TEXT),
                ft.Row([self.txt_matricula, self.btn_buscar_alumno], spacing=10),
                self.card_alumno,
                
                ft.Divider(height=15, color="transparent"),
                
                # SECCIÓN 2
                ft.Text("Número de adquisición del ejemplar", weight="bold", color=self.TEXT),
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
                                on_click=self.controlador.registrar_prestamo
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
                    gradient=ft.LinearGradient(
                        colors=["#cfe8ff", "#9ec9ff"],
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1)
                    ),
                    content=inner_card
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
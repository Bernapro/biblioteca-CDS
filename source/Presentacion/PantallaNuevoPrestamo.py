import flet as ft
import datetime
from Negocio.Controlador.ControladorNuevoPrestamo import ControladorNuevoPrestamo
from Infraestructura.API.BibliotecaEjemplares import BibliotecaEjemplares
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp

class PantallaNuevoPrestamo(ft.Container):
    # Inicializa la vista y variables
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        self.alignment = ft.alignment.Alignment(0, 0)
        numDias = 4
        fechaHoy = datetime.datetime.now()
        fechaEstimada = fechaHoy + datetime.timedelta(days=numDias)
        fechaEstimadaDomingo = fechaEstimada + datetime.timedelta(days=1)
        fechaEstimadaSabado = fechaEstimada - datetime.timedelta(days=1)
        diaFechaEstimada = fechaEstimada.weekday()
        fechaLimite = fechaEstimada if diaFechaEstimada < 5 else (fechaEstimadaDomingo if diaFechaEstimada == 6 else fechaEstimadaSabado)
        numDias = (fechaLimite - fechaHoy).days

        self.controlador = ControladorNuevoPrestamo(self, BibliotecaEjemplares(), repositorio= RepositorioImpl(crud=CRUDimp()), endPrestamo=BibliotecaPrestamos())
        self.libros_seleccionados = {}
        self.libros_cache = []
        
        self.AZUL = "#3B82F6"
        self.VERDE = "#22C55E"
        self.GRIS_BORDE = "outline"          
        self.GRIS_TEXTO = "onSurfaceVariant" 
        self.TEXT = "onSurface"              
        self.CARD = "surface" 
        self.ROJO = "#E53A2E"
        self.AMBER = ft.Colors.AMBER

        self.txt_matricula = ft.TextField(
            hint_text="Ej. 100025787",
            prefix_icon=ft.Icons.PERSON,
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            expand=True, height=50, content_padding=10,
            on_submit=self.controlador.buscar_alumno,
            on_change=self.limpiar_error_borde # Limpia el color rojo al escribir
        )
        self.btn_buscar_alumno = ft.OutlinedButton("Buscar", icon=ft.Icons.SEARCH, style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)), on_click=self.controlador.buscar_alumno)
        
        self.card_alumno = ft.Container()

        self.txt_adquisicion = ft.TextField(
            hint_text="Ej. ADQ-001245",
            prefix_icon=ft.Icons.MENU_BOOK,
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            expand=True, height=50, content_padding=10,
            on_change=self.limpiar_error_borde # Limpia el color rojo al escribir
        )

        self.btn_buscar_libro = ft.OutlinedButton(
            "Buscar",
            icon=ft.Icons.SEARCH,
            style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)),
            data="btn_buscar",
            on_click=self.controlador.listener
        )

        self.lista_libros = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

        self.contenedor_resultados = ft.Container(
            content=self.lista_libros,
            height=250,
            border=ft.border.all(1, self.GRIS_BORDE),
            border_radius=12,
            padding=10,
            bgcolor="surface"
        )

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

        self.txt_fecha_prestamo = ft.TextField(
            label="Fecha de préstamo",
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT), prefix_icon=ft.Icons.CALENDAR_TODAY,
            expand=True, height=55, read_only=True, value= fechaHoy.strftime("%d/%b/%Y"),
            on_click=self.abrir_picker_prestamo
        )
        self.txt_fecha_limite = ft.TextField(
            label=f"Fecha límite ({numDias} dias)",
            border_radius=12, border_color=self.GRIS_BORDE, focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT), prefix_icon=ft.Icons.CALENDAR_MONTH,
            expand=True, height=55, read_only=True, value=fechaLimite.strftime("%d/%b/%Y"),
            on_click=self.abrir_picker_limite
        )

        self.txt_mensaje_alerta = ft.Text("", color=self.TEXT, size=14, weight="bold")
        self.icon_mensaje_alerta = ft.Icon(ft.Icons.WARNING, color=self.AMBER, size=20)
        
        self.contenedor_mensaje = ft.Container(
            content=ft.Row([self.icon_mensaje_alerta, self.txt_mensaje_alerta], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            border=ft.border.all(2, self.AMBER),
            border_radius=10,
            padding=10,
            visible=False,
            margin=ft.margin.only(top=20)
        )

        self.build_ui()

    # Pinta el borde de un campo en rojo
    def marcar_error_borde(self, campo):
        campo.border_color = self.ROJO
        campo.update()

    # Restaura el color gris del borde al escribir
    def limpiar_error_borde(self, e):
        e.control.border_color = self.GRIS_BORDE
        e.control.update()

    # Muestra la alerta inferior
    def mostrar_alerta(self, mensaje, es_error=True):
        self.txt_mensaje_alerta.value = mensaje
        self.contenedor_mensaje.visible = True
        self.update()

    # Oculta la alerta inferior
    def ocultar_alerta(self):
        self.contenedor_mensaje.visible = False
        self.update()

    # Crea item de libro para la lista
    def crear_item_libro(self, id, titulo, autor, adq, disponible):
        disponibilidad = "Disponible" if disponible else "No disponible"
        color = self.VERDE if disponible else ft.Colors.RED_200
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
                    ft.Text(f"Autores: {autor} \nNo. Adquisición: {adq}", size=11, color=self.GRIS_TEXTO),
                ], expand=True, spacing=1),
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=color, size=14),
                    ft.Text(disponibilidad, color=color, size=12, weight="bold")
                ], spacing=4),
                ft.Checkbox(
                    value=adq in self.libros_seleccionados,
                    disabled = not disponible,
                    on_change=lambda e, l=(id, titulo, autor, adq, disponible): self.toggle_libro(l, e.control.value)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    # Actualiza lista de libros
    def actualizar_lista(self):
        self.lista_libros.controls.clear()
        usados = set()

        for adq, libro in self.libros_seleccionados.items():
            self.lista_libros.controls.append(self.crear_item_libro(*libro))
            usados.add(libro[1])

        for libro in self.libros_cache:
            if libro[1] not in usados:
                self.lista_libros.controls.append(self.crear_item_libro(*libro))

        if self.page:
            self.update()

    # Asigna fecha de prestamo
    def seleccionar_fecha_prestamo(self, e):
        if self.picker_fecha_prestamo.value:
            self.txt_fecha_prestamo.value = self.picker_fecha_prestamo.value.strftime("%d/%b/%Y")
            self.txt_fecha_prestamo.update()

    # Asigna fecha limite
    def seleccionar_fecha_limite(self, e):
        fecha = self.picker_fecha_limite.value
        if fecha:
            if fecha.weekday() >= 5:
                self.picker_fecha_limite.value = None
            else:
                self.txt_fecha_limite.value = self.picker_fecha_limite.value.strftime("%d/%b/%Y")
                self.txt_fecha_limite.update()

    # Abre calendario prestamo
    def abrir_picker_prestamo(self, e):
        self.picker_fecha_prestamo.open = True
        self._page.update()

    # Abre calendario limite
    def abrir_picker_limite(self, e):
        self.picker_fecha_limite.open = True
        self._page.update()

    # Regresa a vista anterior
    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    # Agrega o quita libro seleccionado
    def toggle_libro(self, libro, checked):
        adq = libro[3]
        if checked:
            self.libros_seleccionados[adq] = libro
        else:
            self.libros_seleccionados.pop(adq, None)
        self.actualizar_lista()  

    # Construye la interfaz
    def build_ui(self):
        formulario = ft.Column(
            [
                ft.Text("Matrícula del alumno", weight="bold", color=self.TEXT),
                ft.Row([self.txt_matricula, self.btn_buscar_alumno], spacing=10),
                self.card_alumno,
                ft.Divider(height=15, color="transparent"),
                
                ft.Text("Número de adquisición del ejemplar", weight="bold", color=self.TEXT),
                ft.Row([self.txt_adquisicion, self.btn_buscar_libro], spacing=10),
                ft.Text("Selecciona el libro (Ejemplares disponibles):", size=12, color=self.GRIS_TEXTO),
                self.contenedor_resultados,
                ft.Divider(height=15, color="transparent"),

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
                    formulario, 
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
                    ),
                    self.contenedor_mensaje 
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        self.content = ft.Column(
            [
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

    # Limpia campos y resetea variables
    def limpiar_pantalla(self, e=None):
        self.txt_matricula.value = ""
        self.txt_matricula.border_color = self.GRIS_BORDE
        self.txt_adquisicion.value = ""
        self.txt_adquisicion.border_color = self.GRIS_BORDE
        
        self.card_alumno.content = None
        self.card_alumno.bgcolor = ft.Colors.TRANSPARENT

        self.libros_seleccionados.clear()
        self.libros_cache.clear()
        self.lista_libros.controls.clear()

        fecha_actual = datetime.datetime.now()
        fecha_limite_default = fecha_actual + datetime.timedelta(days=7)
        self.fecha_prestamo = fecha_actual 
        
        self.txt_fecha_prestamo.value = fecha_actual.strftime("%d/%b/%Y")
        self.txt_fecha_limite.value = fecha_limite_default.strftime("%d/%b/%Y")
        
        self.picker_fecha_prestamo.value = None
        self.picker_fecha_limite.value = None

        self.ocultar_alerta() 
        self.update()
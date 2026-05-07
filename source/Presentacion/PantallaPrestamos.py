import flet as ft
from Presentacion.PantallaNuevoPrestamo import PantallaNuevoPrestamo
from Negocio.Controlador.ControladorPrestamos import ControladorPrestamos
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp


class PantallaPrestamos(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        self.texto_pagina = ft.Text("1", color="white", weight="bold")
        # Instanciamos el controlador
        self.controlador = ControladorPrestamos(self, endPrestamos=BibliotecaPrestamos(), repo=RepositorioImpl(crud=CRUDimp()))
        # ===== COLORES =====
        self.AZUL = "#3B82F6"
        self.VERDE = "#10B981" 
        self.ROJO = "#EF4444"
        self.NARANJA = "#F59E0B"
        self.FONDO = "transparent" 
        self.GRIS_TEXTO = "onSurfaceVariant"
        self.GRIS_BORDE = "outline"
        self.TEXT = "onSurface"
        self.CARD = "surface"
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30
        self.colores = {"A tiempo": self.VERDE, "Atrasado": self.ROJO, "Por vencer": self.NARANJA}
        self.iconos = {"A tiempo": ft.Icons.CHECK_CIRCLE, "Atrasado": ft.Icons.CANCEL, "Por vencer": ft.Icons.CALENDAR_MONTH}
        self.pagina_actual = 1
        self.registros_por_pagina = 10
        self.total_registros = 0
        self.footer_tabla = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        # [Añadir esto al final de tu __init__]
        
        # ===== CONTROLES DEL MODAL REUTILIZABLE =====
       # 1. Controles de la Tarjeta de Usuario
        self.modal_avatar_icon = ft.Icon(ft.Icons.PERSON, size=80, color=self.AZUL)
        self.modal_nombre = ft.Text("", size=18, weight="bold", color=self.TEXT)
        self.modal_matricula = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_carrera = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_semestre = ft.Text("", color=self.GRIS_TEXTO, size=13, weight="bold")
        self.modal_qr_placeholder = ft.Container(width=80, height=80, bgcolor=self.GRIS_BORDE, border_radius=5)
        
        # 2. Controles Dinámicos
        self.modal_titulo = ft.Text("", size=18, weight="bold", color=self.TEXT)
        self.modal_contenido_dinamico = ft.Column(spacing=15)
        
        # --- NUEVO: CONTROLES DE ACCIÓN PERSONALIZADOS ---
        self.mensaje = ft.Container(
            visible=False,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            expand=True # Para que empuje el botón a la derecha
        )
        # Aquí guardaremos el botón que cambia ("Devolver", "Extender")
        self.modal_boton_dinamico = ft.Container() 

        # Fila que reemplaza al 'actions' nativo
        self.fila_acciones = ft.Row(
            [self.mensaje, self.modal_boton_dinamico],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=470
        )
        
        # 3. Definición del AlertDialog Maestro
        self.dialogo_accion = ft.AlertDialog(
            modal=True,
            bgcolor="surface",
            shape=ft.RoundedRectangleBorder(radius=15),
            title=ft.Row([
                self.modal_titulo,
                ft.IconButton(ft.Icons.CLOSE, icon_color="onSurface", on_click=self.cerrar_dialogo)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # TODO EL DISEÑO VIVE AQUÍ AHORA
            content=ft.Container(
                width=500,
                content=ft.Column([
                    # Tarjeta Fija
                    ft.Container(
                        padding=15, border=ft.border.all(1, self.GRIS_BORDE), border_radius=10,
                        content=ft.Row([
                            self.modal_avatar_icon,
                            ft.Column([self.modal_nombre, self.modal_matricula, self.modal_carrera, self.modal_semestre], spacing=2, expand=True),
                            self.modal_qr_placeholder
                        ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    ),
                    ft.Divider(height=10, color="transparent"),
                    
                    # Área Dinámica (Los libros)
                    self.modal_contenido_dinamico,
                    
                    ft.Divider(height=10, color="transparent"),
                    
                    # Área de Acciones (Mensaje y Botón)
                    self.fila_acciones
                    
                ], tight=True, spacing=8)
            ),
            # ¡Dejamos actions vacío para evitar los bugs de renderizado!
            actions=[], 
        )
        
        self.build_ui()

    #TARJETAS
    def build_card_stat(self, titulo, valor, sub_valor, icono, color):
        color_fondo = color.replace("#", "#20")
        return ft.Container(
            expand=True,
            bgcolor=self.CARD,
            padding=20,
            border_radius=15,
            border=ft.border.all(1, self.GRIS_BORDE),
            content=ft.Row([
                # Icono arriba
                ft.Container(
                    content=ft.Icon(icono, color=color, size=28),
                    bgcolor=color_fondo,
                    width=60, height=60,
                    border_radius=30,
                    alignment=ft.Alignment(0, 0)
                ),
                # Textos
                ft.Column([
                    ft.Text(titulo, size=13, color=self.GRIS_TEXTO, weight="w500"),
                    ft.Text(valor, size=26, weight="bold", color=self.TEXT),
                    ft.Text(sub_valor, size=11, color=self.GRIS_TEXTO),
                ], spacing=2)
            ], spacing=15, alignment=ft.MainAxisAlignment.START)
        )

    
    # ===== BADGE DE ESTADO =====
    def build_estado(self, estado):
        #  colores del texto
        color_texto = self.colores[estado] if estado in self.colores else self.GRIS_TEXTO
        
        icono = self.iconos[estado] if estado in self.iconos else ft.Icons.CIRCLE
        
        # DEFINIMOS EL COLOR DE RELLENO (FONDO) AQUÍ
        color_fondo = "#DCFCE7" if estado == "A tiempo" else "#FEE2E2" # Cambia "#FEE2E2" por el color que más te guste

        return ft.Container(
            content=ft.Row([
                ft.Icon(icono, color=color_texto, size=14),
                ft.Text(estado, color=color_texto, weight="bold", size=12)
            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=color_fondo,  # <--- Aquí aplicamos el color de relleno
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border_radius=15,
            width=110
        )

    # ===== BOTONES DE ACCIÓN =====
    def build_btn_accion(self, texto, icono, color, on_click_action=None, data="", estado = ""):
        return ft.OutlinedButton(
            texto,
            icon=icono,
            style=ft.ButtonStyle(
                color=color,
                shape=ft.RoundedRectangleBorder(radius=8),
                side=ft.BorderSide(1, color),
                padding=ft.padding.symmetric(horizontal=10, vertical=5)
            ),
            height=35,
            on_click=on_click_action,
            data= data,
            visible= estado != "Devuelto"
        )

    # FILAS DE LA TABLA 
    def build_row(self, data):
        print(data["prestamo"])
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(data["identificador"], color=self.GRIS_TEXTO, size=14)),
                ft.DataCell(
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=18, color=self.AZUL),
                        ft.Text(data["nombre"], color=self.TEXT, size=14)
                    ], spacing=8)
                ),
                ft.DataCell(
                    ft.Row([
                        ft.Icon(ft.Icons.FORMAT_LIST_NUMBERED, size=18, color=self.colores[data["estado"]] if data["estado"] in self.colores else self.GRIS_TEXTO),
                        ft.Text(str(data["cantidad"]), color=self.TEXT, size=14)
                    ], spacing=8)
                ),
                ft.DataCell(self.build_estado(data["estado"])),
                ft.DataCell(ft.Text(data["fecha_prestamo"], color=self.GRIS_TEXTO, size=14)),
                ft.DataCell(ft.Text(data["fecha_limite"], color=self.GRIS_TEXTO, size=14)),
                ft.DataCell(
                    ft.Row([
                        self.build_btn_accion(
                            "Extender", 
                            ft.Icons.CALENDAR_MONTH, 
                            self.AZUL,
                            on_click_action=lambda e, d=data: self.abrir_dialogo_prestamo(e, d, "extender"),
                            data= data["prestamo"],
                            estado = data["estado"]
                        ),
                        self.build_btn_accion(
                            "Devolver", 
                            ft.Icons.KEYBOARD_RETURN, 
                            self.VERDE,
                            on_click_action=lambda e, d=data: self.abrir_dialogo_prestamo(e, d, "devolver"),
                            data= data["prestamo"],
                            estado = data["estado"]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.MORE_VERT, 
                            icon_color=self.GRIS_TEXTO,
                            on_click=lambda e, d=data: self.abrir_dialogo_prestamo(e, d, "detalle")
                        )
                    ], spacing=5)
                ),
            ]
        )
        return row


    # ===== LÓGICA DE NAVEGACIÓN =====
    def ir_a_nuevo_prestamo(self, e):
        self.content = PantallaNuevoPrestamo(self._page, vista_anterior=self)
        self.update()

    def cargar_datos(self, e=None):
        # Obtenemos los datos desde el controlador y llenamos las filas
        datos = self.controlador.obtener_prestamos()
        print("datos",datos)
        inicio = (self.pagina_actual - 1) * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        datos_paginados = datos
        print("datos_paginados",datos_paginados)

        self.tabla.rows = [self.build_row(data) for data in datos_paginados]
        #print(data.key for data in self.tabla.rows)

        # También actualizamos las tarjetas de resumen dinámicamente
        if hasattr(self, 'resumen'):
            stats = self.controlador.obtener_estadisticas()
            self.resumen.controls = [
                self.build_card_stat("Total préstamos", stats["totales"], "Registros totales", ft.Icons.MENU_BOOK_ROUNDED, self.AZUL),
                self.build_card_stat("A tiempo", stats["vigentes"], "Préstamos vigentes", ft.Icons.CHECK_CIRCLE_OUTLINE, self.VERDE),
                self.build_card_stat("Atrasados", stats["vencidos"], "Préstamos vencidos", ft.Icons.ACCESS_TIME, self.ROJO),
                self.build_card_stat("Por vencer", stats["proximosAVencer"], "Próximos 3 días", ft.Icons.CALENDAR_MONTH, self.NARANJA),
            ]
            
        texto_resultados = ft.Text(
            f"Mostrando {len(datos_paginados)} de {self.total_registros} préstamos",
            size=14,
            color=self.GRIS_TEXTO
        )
        
        self.footer_tabla.controls = [
            texto_resultados,
            self.construir_paginacion()
        ]

        if e:
            # 1. Forzamos a que la tabla repinte sus filas
            self.tabla.update()
            
            # 2. Forzamos a que el pie de página repinte los botones
            self.footer_tabla.update()
            
            # 3. Refrescamos el contenedor global por si acaso
            self.update()

    # Función detectada por PantallaPrincipal para refrescar al entrar a la vista
    def actualizar(self):
        self.cargar_datos()
        
    def _input_focus(self, e):
        e.control.value = ""
        e.control.color = self.TEXT
        self.update()

    def _input_blur(self, e):
        if not e.control.value:
            e.control.value = str(self.pagina_actual)
            e.control.color = self.GRIS_TEXTO
        self.update()

    def construir_paginacion(self):
        total_paginas = max(1, (self.total_registros // self.registros_por_pagina) + (1 if self.total_registros % self.registros_por_pagina else 0))

        def cambiar_pagina(nueva):
            if 1 <= nueva <= total_paginas:
                self.pagina_actual = nueva
                self.cargar_datos(e=True)

        input_pagina = ft.TextField(
            width=60, height=35, text_align=ft.TextAlign.CENTER,
            value=str(self.pagina_actual), border_radius=8, color=self.GRIS_TEXTO,
            content_padding=5, 
            on_focus=lambda e: self._input_focus(e),
            on_blur=lambda e: self._input_blur(e),
            on_submit=lambda e: cambiar_pagina(int(e.control.value) if e.control.value.isdigit() else self.pagina_actual)
        )

        botones = [
            ft.IconButton(ft.Icons.FIRST_PAGE, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(1)),
            ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(self.pagina_actual - 1))
        ]

        rango = 2
        paginas = []
        if total_paginas <= 7:
            paginas = list(range(1, total_paginas + 1))
        else:
            paginas = [1]
            if self.pagina_actual > 3: paginas.append("...")
            for i in range(max(2, self.pagina_actual - rango), min(total_paginas - 1, self.pagina_actual + rango) + 1):
                paginas.append(i)
            if self.pagina_actual < total_paginas - 2: paginas.append("...")
            paginas.append(total_paginas)

        for p in paginas:
            if p == "...":
                botones.append(ft.Text("...", color=self.TEXT))
            else:
                botones.append(ft.TextButton(
                    content=ft.Text(str(p)), on_click=lambda e, p=p: cambiar_pagina(p),
                    style=ft.ButtonStyle(bgcolor=self.AZUL if p == self.pagina_actual else "transparent", color="white" if p == self.pagina_actual else self.TEXT)
                ))

        botones.extend([
            ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(self.pagina_actual + 1)),
            ft.IconButton(ft.Icons.LAST_PAGE, icon_color=self.TEXT, on_click=lambda e: cambiar_pagina(total_paginas)),
            input_pagina
        ])

        return ft.Row(botones, spacing=5)

    # ===== CONSTRUCCIÓN PRINCIPAL =====
    def build_ui(self):
        # 1. Encabezado y botón nuevo préstamo
        encabezado = ft.Row([
            ft.Column([
                ft.Text("Préstamos de libros", size=28, weight="bold", color=self.TEXT),
                ft.Text("Busca y gestiona los préstamos de libros registrados en el sistema.", size=14, color=self.GRIS_TEXTO)
            ], spacing=5),
            ft.ElevatedButton(
                "+ Nuevo préstamo",
                style=ft.ButtonStyle(
                    bgcolor=self.AZUL, color="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=15)
                ),
                height=45,
                on_click=self.ir_a_nuevo_prestamo
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # 2. Filtros (Barra de búsqueda y dropdown estilo píldora)
        filtros = ft.Row([
            ft.Container(
                expand=True,
                content=ft.TextField(
                    hint_text="Buscar por matrícula, nombre o cantidad...",
                    prefix_icon=ft.Icons.SEARCH, border=ft.InputBorder.NONE, content_padding=15
                ),
                bgcolor=self.CARD, border_radius=10, border=ft.border.all(1, self.GRIS_BORDE)
            ),
            ft.Container(
                width=200,
                content=ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Todos"),
                        ft.dropdown.Option("A tiempo"),
                        ft.dropdown.Option("Atrasado"),
                    ],
                    border=ft.InputBorder.NONE, content_padding=15, hint_text="Estado: Todos"
                ),
                bgcolor=self.CARD, border_radius=10, border=ft.border.all(1, self.GRIS_BORDE)
            ),
            ft.ElevatedButton(
                "Buscar", icon=ft.Icons.SEARCH,
                style=ft.ButtonStyle(bgcolor=self.AZUL, color="white", shape=ft.RoundedRectangleBorder(radius=10)),
                height=50
            )
        ], spacing=15)

        # 3. Tarjetas de Resumen (Se poblarán en cargar_datos)
        self.resumen = ft.Row([], spacing=15)

        # 4. Tabla
       
        self.tabla = ft.DataTable(
            expand=True,
            column_spacing=38,    
            horizontal_margin=25, 
            heading_row_color="surfaceVariant",
            heading_row_height=60,
            data_row_min_height=70, 
            data_row_max_height=70,
            divider_thickness=1,
            columns=[
                ft.DataColumn(ft.Text("Id", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Nombre", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Cantidad", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Estado", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Préstamo", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Límite", weight="bold", color=self.TEXT, size=14)),
                ft.DataColumn(ft.Text("Acciones", weight="bold", color=self.TEXT, size=14)),
            ],
            rows=[]
        )

        self.cargar_datos() # Poblar la tabla por primera vez

        contenedor_tabla = ft.Container(
            expand=True,
            width=float("inf"),
            bgcolor=self.CARD,
            border_radius=15,
            border=ft.border.all(1, self.GRIS_BORDE),            alignment=ft.alignment.Alignment(0, -1),
            content=ft.Column([
                self.tabla
            ], scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )


        # Ensamblaje Final
        self.content = ft.Column(
            [encabezado, filtros, self.resumen, contenedor_tabla, self.footer_tabla],
            spacing=20,
            expand=True
        )
        # ===== CREADOR DE TARJETAS DE LIBRO PARA EL MODAL =====
# ===== CREADOR DE TARJETAS DE LIBRO PARA EL MODAL (SOLO LECTURA) =====
    def crear_item_libro_modal(self, titulo, autor, adq):
        # Usamos colores directos ya que en esta vista sabemos que el libro está prestado
        color_icono = self.AZUL
        
        return ft.Container(
            padding=10,
            border_radius=8,
            border=ft.border.all(1, self.GRIS_BORDE),
            content=ft.Row([
                # Icono izquierdo
                ft.Container(
                    content=ft.Icon(ft.Icons.MENU_BOOK, color=color_icono, size=25),
                    bgcolor="surfaceVariant",
                    padding=10,
                    border_radius=8
                ),
                # Datos del libro (expand=True toma el espacio disponible hasta el final)
                ft.Column([
                    ft.Text(titulo, weight="bold", color=self.TEXT),
                    ft.Text(f"Autores: {autor} \nNo. Adquisición: {adq}", size=11, color=self.GRIS_TEXTO),
                ], expand=True, spacing=1)
                
            ], alignment=ft.MainAxisAlignment.START)
        )
    def mostrar_mensaje(self, texto, color):
        es_exito = (color == "green")
        color_real = self.VERDE if es_exito else self.ROJO if color == "red" else self.NARANJA
        icono = ft.Icons.CHECK_CIRCLE if es_exito else ft.Icons.ERROR if color == "red" else ft.Icons.WARNING

        self.mensaje.bgcolor = "transparent"
        self.mensaje.border = ft.border.all(1, color_real)
        self.mensaje.content = ft.Row(
            [
                ft.Icon(icono, color=color_real, size=20),
                ft.Text(texto, color=self.TEXT, size=13, weight="w500")
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=8
        )
        self.mensaje.visible = True
        # Usamos _page.update() para que el overlay completo se entere del cambio
        self._page.update() 

    def abrir_dialogo_prestamo(self, e, d, accion):
        # 1. Resetear el estado visual instantáneamente
        args = (d["prestamo"],d["estado"])
        print(args)
        self.mensaje.visible = False
        self.modal_boton_dinamico.content = None
        self.modal_contenido_dinamico.controls.clear()

        self.modal_nombre.value = d["nombre"]
        self.modal_matricula.value = f"ID: {d['identificador']}"

        # 3. Simular lista de libros prestados
        libros= self.controlador.obtenerLibros(args[0])
        print(libros)
        lista_tarjetas_libros = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)
        for libro in libros:
            lista_tarjetas_libros.controls.append(self.crear_item_libro_modal(libro["titulo"], libro["autor"], libro["adq"]))

        contenedor_libros_scroll = ft.Container(
            content=lista_tarjetas_libros, height=180, border=ft.border.all(1, self.GRIS_BORDE),
            border_radius=12, padding=10, bgcolor="surface"
        )

        # 4. Configurar según la acción
        if accion == "devolver":
            self.modal_titulo.value = "Devolución de Material"
            self.modal_contenido_dinamico.controls.extend([
                ft.Text("Ejemplares a devolver:", size=13, weight="bold", color=self.TEXT),
                contenedor_libros_scroll
            ])
            self.modal_boton_dinamico.content = ft.ElevatedButton(
                "Confirmar Devolución", bgcolor=self.VERDE, color="white", 
                data="btn_devolver",
                on_click=lambda e, p = args: self.controlador.finalizarPrestamo(e, p)
            )

        elif accion == "extender":
            self.modal_titulo.value = "Extender Préstamo"
            self.modal_contenido_dinamico.controls.extend([
                ft.Text("Ejemplares para extensión:", size=13, weight="bold", color=self.TEXT),
                contenedor_libros_scroll,
                ft.TextField(label="Nueva fecha límite", read_only=True, prefix_icon=ft.Icons.CALENDAR_MONTH, border_radius=8)
            ])
            self.modal_boton_dinamico.content = ft.ElevatedButton(
                "Guardar Extensión", bgcolor=self.AZUL, color="white", 
                on_click=lambda e: self.mostrar_mensaje("El alumno tiene multas pendientes.", "red")
            )

        elif accion == "detalle":
            self.modal_titulo.value = "Detalles del Préstamo"
            self.modal_contenido_dinamico.controls.extend([
                ft.Text("Ejemplares prestados:", size=13, weight="bold", color=self.TEXT),
                contenedor_libros_scroll
            ])

        # 5. LÓGICA DE INYECCIÓN SEGURA (La corrección principal)
        # Verificamos si ya está en el overlay, si no, lo inyectamos
        if self.dialogo_accion not in self._page.overlay:
            self._page.overlay.append(self.dialogo_accion)
            
        self.dialogo_accion.open = True
        
        # Le ordenamos a la página completa que se dibuje. 
        # Esto soluciona el RuntimeError porque Flet asocia el control al árbol.
        self._page.update()

    def cerrar_dialogo(self, e):
        self.dialogo_accion.open = False
        self._page.update()
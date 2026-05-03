import flet as ft
from Presentacion.PantallaRegistroIncidencia import PantallaRegistroIncidencia
from Negocio.Controlador.ControladorIncidencia import ControladorIncidencia

class PantallaIncidencias(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.controlador = ControladorIncidencia(self) # Instanciamos el controlador
        
        # ===== COLORES CONSTANTES (Actualizados y nuevos) =====
        self.AZUL = "#3B82F6"      # Botones principales
        self.VERDE = "#22C55E"     # Estado Resuelto
        self.ROJO = "#EF4444"      # Botón Nueva / Estado Pendiente
        self.NARANJA = "#F59E0B"   # Icono Usuario / Texto Parcial
        self.TURQUESA = "#0F766E" 
        self.FONDO = "transparent"
        
        # Nuevos colores específicos para el modal
        self.GRIS_TEXTO = "onSurfaceVariant"
        self.GRIS_BORDE = "outline"

        # Propiedades del Contenedor Principal
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30
        
        # ===== VARIABLES DE PAGINACIÓN =====
        self.pagina_actual = 1
        self.registros_por_pagina = 10
        self.total_registros = 0
        self.footer_tabla = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        # ===== CONTROLES DINÁMICOS DE BÚSQUEDA =====
        self.input_busqueda = ft.TextField(
            expand=True,
            hint_text="Buscar por nombre o identificador...",
            prefix_icon=ft.Icons.SEARCH,
            color="onSurface",
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=15),
            text_style=ft.TextStyle(size=15),

            on_change=self.cargar_datos
        )

        self.dropdown_tipo = ft.Dropdown(
            width=180,
            label="Tipo de usuario",
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="surface",
            color="onSurface",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("ALUMNO"),
                ft.dropdown.Option("PERSONAL"),
                ft.dropdown.Option("VISITANTE"),
            ],
            value="Todos",
            on_select=self.cargar_datos
        )

        self.dropdown_estado = ft.Dropdown(
            width=160,
            label="Estado",
            border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            border_radius=12,
            bgcolor="surface",
            color="onSurface",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Resuelto"),
            ],
            value="Todos",
            on_select=self.cargar_datos
        )

        self.estado_actual_modal = None
        self.modal_cat_icon = ft.Icon(ft.Icons.WARNING, size=16)

        self.btn_resuelto = ft.ElevatedButton(
            "Resuelto",
            width=150,
            height=40,
            on_click=lambda e: self.cambiar_estado_ui("RESUELTA")
        )

        self.btn_pendiente = ft.ElevatedButton(
            "Pendiente",
            width=150,
            height=40,
            on_click=lambda e: self.cambiar_estado_ui("PENDIENTE")
        )
            
        
        # 1. Controles referenciables dentro del modal (para actualizar su contenido)
        self.modal_avatar_icon = ft.Icon(ft.Icons.PERSON, size=80, color=self.NARANJA)
        self.modal_nombre = ft.Text("", size=18, weight="bold", color="black")
        self.modal_matricula = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_carrera = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_semestre = ft.Text("", color=self.GRIS_TEXTO, size=13, weight="bold")
        
        # espacio para QR 
        self.modal_qr_placeholder = ft.Container(width=80, height=80, bgcolor=self.GRIS_BORDE, border_radius=5)

        self.modal_tipo = ft.Text("", color=self.NARANJA, weight="bold")
        self.modal_categoria = ft.Text("", color="onSurface")
        self.modal_descripcion = ft.Text("", color="onSurface")
        self.modal_lugar = ft.Text("", color="onSurface")
        self.modal_fecha = ft.Text("", color="onSurface")
        
        self.modal_estado_icono = ft.Icon(ft.Icons.CIRCLE, size=12, color=self.VERDE)
        self.modal_estado_texto = ft.Text("", color=self.VERDE, weight="w500")

        self.modal_comentario = ft.TextField(
            multiline=True, 
            min_lines=3, 
            max_lines=5,
            hint_text="Escribe un comentario sobre el seguimiento...",
            border_color=self.GRIS_BORDE,
            border_radius=10,
            text_style=ft.TextStyle(color="onSurface", size=13)
        )

        # Definición del AlertDialog rediseñado
        self.dialogo_detalles = ft.AlertDialog(
            modal=True,
            bgcolor="surface", 
            shape=ft.RoundedRectangleBorder(radius=15),
            
            # TÍTULO: Fila con Texto y Botón Cerrar
            title=ft.Row([
                ft.Text("Detalle de Incidencia", size=18, weight="bold", color="onSurface"),
                ft.IconButton(ft.Icons.CLOSE, icon_color="onSurface", on_click=self.cerrar_dialogo)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            



            # CONTENIDO PRINCIPAL
            content=ft.Container(
                width=500, # Ancho similar a la imagen 1
                content=ft.Column([
                    
                    # SECCIÓN 1: Tarjeta de Datos Personales (Borde gris)
                    ft.Container(
                        padding=15,
                        border=ft.border.all(1, self.GRIS_BORDE),
                        border_radius=10,
                        content=ft.Row([
                            self.modal_avatar_icon,
                            ft.Column([
                                self.modal_nombre,
                                self.modal_matricula,
                                self.modal_carrera,
                                self.modal_semestre
                            ], spacing=2, expand=True),
                            self.modal_qr_placeholder # Espacio para el QR
                        ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    ),
                    
                    ft.Divider(height=20, color="transparent"),
                    
                    # SECCIÓN 2: Detalles de la Incidencia (Filas alineadas)
                    # Usamos anchos fijos en las etiquetas para alinear los dos puntos
                    ft.Row([ft.Text("Tipo de Incidencia:", width=130, color=self.GRIS_TEXTO), self.modal_tipo]),
                    ft.Row([
                        ft.Text("Categoría:", width=130, color=self.GRIS_TEXTO),
                        ft.Row([self.modal_cat_icon, self.modal_categoria], spacing=5)
                    ]),

                    ft.Row([
                        ft.Text("Descripción:", width=130, color=self.GRIS_TEXTO),
                        self.modal_descripcion
                    ]),
                    ft.Row([ft.Text("Lugar:", width=130, color=self.GRIS_TEXTO), self.modal_lugar]),
                    ft.Row([ft.Text("Fecha:", width=130, color=self.GRIS_TEXTO), self.modal_fecha]),
                    ft.Row([ft.Text("Estado Actual:", width=130, color=self.GRIS_TEXTO), ft.Row([self.modal_estado_icono, self.modal_estado_texto], spacing=5)]),
                    
                    ft.Divider(height=25),
                    
                    # SECCIÓN 3: Cambiar Estado (Selector visual)
                    ft.Row([
                        ft.Text("Cambiar Estado:", width=130, color=self.GRIS_TEXTO, weight="bold"),
                        ft.Row([
                            self.btn_resuelto,
                            ft.Icon(ft.Icons.SWAP_HORIZ, color=self.GRIS_TEXTO),
                            self.btn_pendiente
                        ])
                    ]),
                    ft.Text("Cambia el estado de la incidencia", color=self.GRIS_TEXTO, size=11, italic=True),
                    
                    ft.Divider(height=15, color="transparent"),
                    
                    # SECCIÓN 4: Comentario
                    ft.Text("Comentario:", weight="bold", color="onSurface"),
                    self.modal_comentario,
                    
                ], tight=True, spacing=8)
            ),
            
            # ACCIONES: Solo botón guardar a la derecha
            actions=[
                ft.ElevatedButton(
                    "Guardar cambios", 
                    bgcolor=self.AZUL, 
                    color="white", 
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=self.controlador.guardar_dialogo # Delegado al controlador
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== LÓGICA DEL DIÁLOGO ACTUALIZADA =====
    # Ahora acepta el evento 'e' y los datos de la incidencia
    def abrir_dialogo(self, e, d):        
        nuevo_icono = self.obtener_icono_tipo(d["tipo_usuario"])

        self.modal_avatar_icon.icon = nuevo_icono.icon
        self.modal_avatar_icon.color = nuevo_icono.color
        self.controlador.seleccionar_incidencia(d["id"])

        self.modal_nombre.value = d["nombre"]

        label_id = {
            "ALUMNO": "Matrícula",
            "PERSONAL": "No. Plaza",
            "VISITANTE": "ID"
        }.get(d["tipo_usuario"], "ID")

        self.modal_matricula.value = f"{label_id}: {d['identificador']}"

        tipo = d["tipo_usuario"]

        if tipo == "ALUMNO":
            self.modal_carrera.value = f"Carrera: {d['carrera']}"
            self.modal_semestre.value = f"Semestre: {d['semestre']}"

        elif tipo == "PERSONAL":
            self.modal_carrera.value = ""
            self.modal_semestre.value = ""

        elif tipo == "VISITANTE":
            self.modal_carrera.value = f"Institución: {d.get('institucion', '-')}"
            self.modal_semestre.value = ""

        self.modal_tipo.value = d["tipo"]

        # 🔥 DESCRIPCIÓN REAL
        self.modal_descripcion.value = d["descripcion"]

        self.modal_lugar.value = d["lugar"]
        self.modal_fecha.value = d["fecha"]

        # 🔥 ESTADO
        self.modal_estado_texto.value = d["estado"]
        self.modal_estado_texto.color = self.VERDE if d["estado"] == "RESUELTA" else self.ROJO
        self.modal_estado_icono.color = self.modal_estado_texto.color
        self.modal_estado_icono.icon = ft.Icons.CIRCLE
        
        # 🔥 COMENTARIO
        self.modal_comentario.value = d["comentario"]

        self.modal_categoria.value = d["categoria"]

        if "Ruido" in d["categoria"]:
            self.modal_cat_icon.icon = ft.Icons.VOLUME_UP
        elif "Equipo" in d["categoria"]:
            self.modal_cat_icon.icon = ft.Icons.COMPUTER
        elif "Comportamiento" in d["categoria"]:
            self.modal_cat_icon.icon = ft.Icons.PERSON_OFF
        else:
            self.modal_cat_icon.icon = ft.Icons.WARNING

        self.estado_actual_modal = d["estado"]
        self.actualizar_botones_estado()

   

        # 2. Abrir el diálogo
        if self.dialogo_detalles not in self._page.overlay:
            self._page.overlay.append(self.dialogo_detalles)
        self.dialogo_detalles.open = True
        self._page.update()

    def cerrar_dialogo(self, e):
        self.dialogo_detalles.open = False
        self._page.update()


    def cambiar_estado_ui(self, nuevo_estado):
        id_actual = self.controlador._ControladorIncidencia__id_actual
        self.controlador.cambiar_estado(id_actual, nuevo_estado)
        self.estado_actual_modal = nuevo_estado
        color = self.VERDE if nuevo_estado == "RESUELTA" else self.ROJO
        self.modal_estado_texto.value = nuevo_estado
        self.modal_estado_texto.color = color
        self.modal_estado_icono.color = color
        self.modal_estado_icono.icon = ft.Icons.CIRCLE
        self.actualizar_botones_estado()
        self.actualizar()
        self._page.update()

    def actualizar_botones_estado(self):
        estado = self.estado_actual_modal

        self.btn_resuelto.style = ft.ButtonStyle(
            bgcolor=self.VERDE if estado == "RESUELTA" else None,  
            color="white" if estado == "RESUELTA" else self.VERDE,
            side=ft.BorderSide(1, self.VERDE),
            shape=ft.RoundedRectangleBorder(radius=8)
        )

        self.btn_pendiente.style = ft.ButtonStyle(
            bgcolor=self.ROJO if estado == "PENDIENTE" else None,  
            color="white" if estado == "PENDIENTE" else self.ROJO,
            side=ft.BorderSide(1, self.ROJO),
            shape=ft.RoundedRectangleBorder(radius=8)
        )

        self.update()

    # ===== BOTONES REUTILIZABLES =====
    def build_btn_resuelto(self, id_incidencia):
        return ft.ElevatedButton(
            "Resuelto",
            height=40,
            width=140,  
            style=ft.ButtonStyle(
                bgcolor=self.VERDE,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=(lambda e: self.controlador.cambiar_estado(id_incidencia, "RESUELTA"))
        )
    
    def build_btn_pendiente(self, id_incidencia):
        return ft.ElevatedButton(
            "Pendiente",
            height=40,
            width=140,
            style=ft.ButtonStyle(
                bgcolor=self.ROJO,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=(lambda e: self.controlador.cambiar_estado(id_incidencia, "PENDIENTE"))
        )

    # MODIFICADO: Ahora build_btn_detalles acepta una función lambda con los datos
    def build_btn_detalles(self, on_click_action):
        return ft.OutlinedButton(
            "Ver detalles", height=40, 
            style=ft.ButtonStyle(color=self.AZUL, shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=on_click_action  
        )

    # ===== CARD INCIDENCIA ACTUALIZADA =====
    # Agregamos carrera y semestre como parámetros requeridos

    def build_card(self, d):
        tipo_usuario = d["tipo_usuario"]

        label_id = {
            "ALUMNO": "Matrícula",
            "PERSONAL": "No. Plaza",
            "VISITANTE": "ID"
        }.get(tipo_usuario, "ID")

        identificador = d["identificador"]

        color_borde = self.ROJO if d["tipo"] == "DEFINITIVA" else self.NARANJA

        categoria = d["categoria"]

        # Icono por categoría
        icono = ft.Icons.WARNING
        if "Ruido" in categoria:
            icono = ft.Icons.VOLUME_UP
        elif "Equipo" in categoria:
            icono = ft.Icons.COMPUTER
        elif "Comportamiento" in categoria:
            icono = ft.Icons.PERSON_OFF

        # Estado visual
        color_estado = self.VERDE if d["estado"] == "RESUELTA" else self.ROJO
        icono_estado = ft.Icons.CHECK_CIRCLE if d["estado"] == "RESUELTA" else ft.Icons.CANCEL

        return ft.Container(
            bgcolor="surface",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=25, color="black12"),
            content=ft.Row(
                controls=[
                    # BARRA IZQUIERDA DE COLOR
                    ft.Container(width=8, bgcolor=color_borde),

                    ft.Container(
                        expand=True,
                        padding=15,
                        content=ft.Row(
                            [
                                #IZQUIERDA (DATOS)
                                ft.Row([
                                    self.obtener_icono_tipo(tipo_usuario),
                                        ft.Container(  
                                            padding=ft.padding.only(left=10),
                                            content=ft.Column([
                                                ft.Text(d["nombre"], weight="bold", size=18),  

                                                ft.Text(
                                                    f"{label_id}: {identificador}",
                                                    size=14,
                                                    color=self.GRIS_TEXTO
                                                ),

                                                ft.Text(
                                                    f"Tipo: {d['tipo']}",
                                                    size=12,
                                                    color=color_borde,
                                                    weight="w500"
                                                ),

                                                ft.Row([
                                                    ft.Icon(icono, size=18),  
                                                    ft.Text(d["categoria"], size=14)
                                                ], spacing=6),

                                                ft.Text(
                                                    f"{d['lugar']} | {d['fecha']}",
                                                    size=13
                                                )

                                            ], spacing=6)
                                        )

                    

                                ], spacing=15),

                                #CENTRO (DESCRIPCIÓN)
                                ft.Container(
                                    expand=True,
                                    padding=10,
                                    border_radius=10,
                                    bgcolor="surfaceVariant",
                                    content=ft.Text(
                                        d["descripcion"] or "Sin descripción",
                                        size=13,
                                        color=self.GRIS_TEXTO,
                                        max_lines=3,
                                        weight="w400",
                                        overflow=ft.TextOverflow.ELLIPSIS
                                    )
                                ),

                                # DERECHA 
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(icono_estado, color=color_estado, size=18),
                                        ft.Text(d["estado"], color=color_estado, weight="bold")
                                    ], spacing=5),

                                    self.build_btn_detalles(
                                        lambda e, d=d: self.abrir_dialogo(e, d)
                                    )
                                ], spacing=15)

                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                ]
            )
        )
                

    #  LÓGICA DE NAVEGACIÓN 
    def ir_a_registro(self, e):
        self.content = PantallaRegistroIncidencia(self._page, vista_anterior=self)
        self.update()

    #  CONSTRUCCIÓN DE LA INTERFAZ 
    def build_ui(self):
        # --- Botón Nuevo ---
        btn_nueva_incidencia = ft.ElevatedButton(
            "NUEVA INCIDENCIA +",
            bgcolor=self.ROJO,
            color="white",
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=ft.padding.symmetric(horizontal=25)),
            on_click=self.ir_a_registro
        )

        encabezado = ft.Row([
            ft.Column([
                ft.Text("Gestión de Incidencias", size=32, weight="bold", color="onSurface"),
                ft.Text("Busca y gestiona el catálogo de incidencias registradas en el sistema.", color=self.GRIS_TEXTO)
            ]),
            btn_nueva_incidencia
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        filtros = ft.Container(
            bgcolor="surface", border_radius=35, padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="black12", offset=ft.Offset(0, 4)),
            content=ft.Row([
                self.input_busqueda,
                ft.Container(width=1, height=30, bgcolor=self.GRIS_BORDE),
                self.dropdown_tipo,
                self.dropdown_estado,

            ], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # Contenedor dinámico para la lista
        self.lista_incidencias = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        self.cargar_datos() # Se llama para popular la lista

        self.content = ft.Column([encabezado, filtros, self.lista_incidencias, self.footer_tabla], spacing=20, expand=True)

    # Función detectada automáticamente por PantallaPrincipal para refrescar al entrar a la vista
    def actualizar(self):
        self.cargar_datos()

    def cargar_datos(self, e=None):

        if e and hasattr(e, "control"):
            if e.control in [self.input_busqueda, self.dropdown_tipo, self.dropdown_estado]:
                self.pagina_actual = 1

        texto = (self.input_busqueda.value or "").lower()
        tipo = self.dropdown_tipo.value
        estado = self.dropdown_estado.value
        self.lista_incidencias.controls.clear()
        datos = self.controlador.obtener_incidencias()
        

        datos_filtrados = []

        for d in datos:

            if texto:
                if texto not in d["nombre"].lower() and texto not in d["identificador"].lower():
                    continue

            if tipo != "Todos" and d["tipo_usuario"] != tipo:
                continue

            if estado != "Todos":
                if estado == "Pendiente" and d["estado"] != "PENDIENTE":
                    continue
                if estado == "Resuelto" and d["estado"] != "RESUELTA":
                    continue

            datos_filtrados.append(d)

        # ===== PAGINACIÓN DESPUÉS DEL FILTRO =====
        self.total_registros = len(datos_filtrados)

        inicio = (self.pagina_actual - 1) * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina

        datos_paginados = datos_filtrados[inicio:fin]
            
        for d in datos_paginados:
            self.lista_incidencias.controls.append(self.build_card(d))


        texto_resultados = ft.Text(
            f"Mostrando {len(datos_paginados)} de {self.total_registros} incidencias",
            size=14,
            color="onSurfaceVariant"
        )
        
        self.footer_tabla.controls = [
            texto_resultados,
            self.construir_paginacion()
        ]
        if e:
            self.update()

    def _input_focus(self, e):
        e.control.value = ""
        e.control.color = "onSurface"
        self.update()

    def _input_blur(self, e):
        if not e.control.value:
            e.control.value = str(self.pagina_actual)
            e.control.color = "onSurfaceVariant"
        self.update()

    def obtener_icono_tipo(self, tipo):
            if tipo == "ALUMNO":
                return ft.Icon(ft.Icons.SCHOOL, color=self.AZUL,size=100)
            elif tipo == "PERSONAL":
                return ft.Icon(ft.Icons.BADGE, color=self.VERDE,size=100)
            elif tipo == "VISITANTE":
                return ft.Icon(ft.Icons.PERSON, color=self.NARANJA,size=100)
            else:
                return ft.Icon(ft.Icons.HELP)    

    def construir_paginacion(self):
        total_paginas = max(1, (self.total_registros // self.registros_por_pagina) + (1 if self.total_registros % self.registros_por_pagina else 0))

        def cambiar_pagina(nueva):
            if 1 <= nueva <= total_paginas:
                self.pagina_actual = nueva
                self.cargar_datos(e=True) # Pasamos 'e' para forzar la actualización visual

        input_pagina = ft.TextField(
            width=60, height=35, text_align=ft.TextAlign.CENTER,
            value=str(self.pagina_actual), border_radius=8, color="onSurfaceVariant",
            content_padding=5, 
            on_focus=lambda e: self._input_focus(e),
            on_blur=lambda e: self._input_blur(e),
            on_submit=lambda e: cambiar_pagina(int(e.control.value) if e.control.value.isdigit() else self.pagina_actual)
        )



        botones = [
            ft.IconButton(ft.Icons.FIRST_PAGE, icon_color="onSurface", on_click=lambda e: cambiar_pagina(1)),
            ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color="onSurface", on_click=lambda e: cambiar_pagina(self.pagina_actual - 1))
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
                botones.append(ft.Text("...", color="onSurface"))
            else:
                botones.append(ft.TextButton(
                    content=ft.Text(str(p)), on_click=lambda e, p=p: cambiar_pagina(p),
                    style=ft.ButtonStyle(bgcolor=self.AZUL if p == self.pagina_actual else None, color="white" if p == self.pagina_actual else "black")
                ))

        botones.extend([
            ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color="onSurface", on_click=lambda e: cambiar_pagina(self.pagina_actual + 1)),
            ft.IconButton(ft.Icons.LAST_PAGE, icon_color="onSurface", on_click=lambda e: cambiar_pagina(total_paginas)),
            input_pagina
        ])

        return ft.Row(botones, spacing=5)
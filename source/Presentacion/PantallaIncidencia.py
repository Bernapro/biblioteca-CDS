import flet as ft

# IMPORTACIÓN DE LA NUEVA CLASE (Se mantiene igual)
from Presentacion.PantallaRegistroIncidencia import PantallaRegistroIncidencia

class PantallaIncidencias(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        
        # ===== COLORES CONSTANTES (Actualizados y nuevos) =====
        self.AZUL = "#3B82F6"      # Botones principales
        self.VERDE = "#22C55E"     # Estado Resuelto
        self.ROJO = "#EF4444"      # Botón Nueva / Estado Pendiente
        self.NARANJA = "#F59E0B"   # Icono Usuario / Texto Parcial
        self.TURQUESA = "#0F766E" 
        self.FONDO = "#EAF1F7"
        
        # Nuevos colores específicos para el modal
        self.GRIS_TEXTO = "#4B5563"
        self.GRIS_BORDE = "#E5E7EB"

        # Propiedades del Contenedor Principal
        self.expand = True
        self.padding = 30
        self.bgcolor = self.FONDO
        self.border_radius = 30

        # ===== CONTROLES DINÁMICOS DE BÚSQUEDA =====
        self.input_busqueda = ft.TextField(
            expand=True,
            hint_text="Buscar estudiante...",
            prefix_icon=ft.Icons.SEARCH,
            color="black",
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=15),
            text_style=ft.TextStyle(size=15)
        )

        self.dropdown_estado = ft.Dropdown(
            width=140,
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Resuelto"),
            ],
            value="Todos",
            border=ft.InputBorder.NONE,
            color="black",
            content_padding=ft.padding.symmetric(horizontal=10, vertical=15),
            text_style=ft.TextStyle(size=15, weight="w500")
        )

        # =====================================================================
        # ===== NUEVA ESTRUCTURA DEL DIÁLOGO (Credencial del Estudiante) =====
        # =====================================================================
        
        # 1. Controles referenciables dentro del modal (para actualizar su contenido)
        self.modal_avatar_icon = ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=80, color=self.NARANJA)
        self.modal_nombre = ft.Text("", size=18, weight="bold", color="black")
        self.modal_matricula = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_carrera = ft.Text("", color=self.GRIS_TEXTO, size=13)
        self.modal_semestre = ft.Text("", color=self.GRIS_TEXTO, size=13, weight="bold")
        
        # QR Placeholder (Como pediste, no hay problema si no está, dejamos el espacio)
        self.modal_qr_placeholder = ft.Container(width=80, height=80, bgcolor=self.GRIS_BORDE, border_radius=5)

        self.modal_tipo = ft.Text("", color=self.NARANJA, weight="bold")
        self.modal_desc_icon = ft.Icon(ft.Icons.VOLUME_UP, size=18, color=self.GRIS_TEXTO)
        self.modal_descripcion = ft.Text("", color="black")
        self.modal_lugar = ft.Text("", color="black")
        self.modal_fecha = ft.Text("", color="black")
        
        self.modal_estado_icono = ft.Icon(ft.Icons.CIRCLE, size=12, color=self.VERDE)
        self.modal_estado_texto = ft.Text("", color=self.VERDE, weight="w500")

        self.modal_comentario = ft.TextField(
            multiline=True, 
            min_lines=3, 
            max_lines=5,
            hint_text="Escribe un comentario sobre el seguimiento...",
            border_color=self.GRIS_BORDE,
            border_radius=10,
            text_style=ft.TextStyle(color="black", size=13)
        )

        # Definición del AlertDialog rediseñado
        self.dialogo_detalles = ft.AlertDialog(
            modal=True,
            bgcolor="white", # Fondo blanco puro como la imagen 1
            shape=ft.RoundedRectangleBorder(radius=15),
            
            # TÍTULO: Fila con Texto y Botón Cerrar
            title=ft.Row([
                ft.Text("Credencial del Estudiante", size=18, weight="bold", color="black"),
                ft.IconButton(ft.Icons.CLOSE, icon_color="black", on_click=self.cerrar_dialogo)
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
                    ft.Row([ft.Text("Descripción:", width=130, color=self.GRIS_TEXTO), ft.Row([self.modal_desc_icon, self.modal_descripcion], spacing=5)]),
                    ft.Row([ft.Text("Lugar:", width=130, color=self.GRIS_TEXTO), self.modal_lugar]),
                    ft.Row([ft.Text("Fecha:", width=130, color=self.GRIS_TEXTO), self.modal_fecha]),
                    ft.Row([ft.Text("Estado Actual:", width=130, color=self.GRIS_TEXTO), ft.Row([self.modal_estado_icono, self.modal_estado_texto], spacing=5)]),
                    
                    ft.Divider(height=25),
                    
                    # SECCIÓN 3: Cambiar Estado (Selector visual)
                    ft.Row([
                        ft.Text("Cambiar Estado:", width=130, color=self.GRIS_TEXTO, weight="bold"),
                        ft.Row([
                            # Botón Resuelto (Verde activo)
                            ft.Container(content=ft.Text("Resuelto", color="white", size=12, weight="bold"), bgcolor=self.VERDE, padding=ft.padding.symmetric(horizontal=12, vertical=8), border_radius=5),
                            ft.Icon(ft.Icons.SWAP_HORIZ, color=self.GRIS_TEXTO),
                            # Botón Pendiente (Gris inactivo)
                            ft.Container(content=ft.Text("Pendiente", color="black", size=12), border=ft.border.all(1, self.GRIS_BORDE), padding=ft.padding.symmetric(horizontal=12, vertical=8), border_radius=5),
                        ], spacing=10)
                    ]),
                    ft.Text("Cambia el estado de la incidencia", color=self.GRIS_TEXTO, size=11, italic=True),
                    
                    ft.Divider(height=15, color="transparent"),
                    
                    # SECCIÓN 4: Comentario
                    ft.Text("Comentario:", weight="bold", color="black"),
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
                    on_click=self.guardar_dialogo
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Construir y ensamblar la interfaz
        self.build_ui()

    # ===== LÓGICA DEL DIÁLOGO ACTUALIZADA =====
    # Ahora acepta el evento 'e' y los datos de la incidencia
    def abrir_dialogo(self, e, nombre, matricula, carrera, semestre, tipo, razon, lugar, fecha, estado):
        
        # 1. Actualizar los controles del modal con los datos recibidos
        self.modal_nombre.value = nombre
        self.modal_matricula.value = f"Matrícula: {matricula}"
        self.modal_carrera.value = f"Carrera: {carrera}"
        self.modal_semestre.value = f"Semestre: {semestre}"
        
        self.modal_tipo.value = tipo
        # Ajustar color del tipo (Naranja para Parcial, Rojo para Definitiva)
        self.modal_tipo.color = self.ROJO if tipo == "DEFINITIVA" else self.NARANJA
        self.modal_avatar_icon.color = self.modal_tipo.color # El avatar toma el color del tipo

        # Icono de descripción dinámico
        if "Ruido" in razon: self.modal_desc_icon.icon = ft.Icons.VOLUME_UP
        elif "equipo" in razon: self.modal_desc_icon.icon = ft.Icons.COMPUTER
        else: self.modal_desc_icon.icon = ft.Icons.WARNING_AMBER_ROUNDED
        
        self.modal_descripcion.value = razon
        self.modal_lugar.value = lugar
        self.modal_fecha.value = fecha
        
        # Estado actual visual
        self.modal_estado_texto.value = estado
        self.modal_estado_texto.color = self.VERDE if estado == "Resuelto" else self.ROJO
        self.modal_estado_icono.color = self.modal_estado_texto.color
        
        # Limpiar o cargar comentario previo (puedes pasar el comentario como argumento también)
        self.modal_comentario.value = "" 

        # 2. Abrir el diálogo
        if self.dialogo_detalles not in self._page.overlay:
            self._page.overlay.append(self.dialogo_detalles)
        self.dialogo_detalles.open = True
        self._page.update()

    def cerrar_dialogo(self, e):
        self.dialogo_detalles.open = False
        self._page.update()

    def guardar_dialogo(self, e):
        # Aquí obtienes el nuevo comentario y lógica para cambiar estado
        print(f"Guardando cambios para: {self.modal_nombre.value}")
        print(f"Nuevo Comentario: {self.modal_comentario.value}")
        self.cerrar_dialogo(e)

    # ===== BOTONES REUTILIZABLES =====
    def build_btn_resuelto(self):
        return ft.ElevatedButton(
            "Resuelto", height=40, 
            style=ft.ButtonStyle(bgcolor=self.VERDE, color="white", shape=ft.RoundedRectangleBorder(radius=8))
        )

    def build_btn_pendiente(self):
        return ft.ElevatedButton(
            "Pendiente", height=40, 
            style=ft.ButtonStyle(bgcolor=self.ROJO, color="white", shape=ft.RoundedRectangleBorder(radius=8))
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
    def build_card(self, nombre, matricula, carrera, semestre, razon, lugar, fecha, tipo="PARCIAL", estado="Pendiente"):
        color_borde = self.ROJO if tipo == "DEFINITIVA" else self.NARANJA
        icono_razon = ft.Icons.WARNING_AMBER_ROUNDED
        if "Ruido" in razon: icono_razon = ft.Icons.VOLUME_UP_ROUNDED
        elif "equipo" in razon: icono_razon = ft.Icons.COMPUTER_ROUNDED
        
        return ft.Container(
            bgcolor="white", border_radius=20, shadow=ft.BoxShadow(blur_radius=25, color="black12"), 
            content=ft.Row(
                controls=[
                    ft.Container(width=8, bgcolor=color_borde, border_radius=ft.border_radius.only(top_left=20, bottom_left=20)),
                    ft.Container(
                        expand=True, padding=15, 
                        content=ft.Row([
                            ft.Row([
                                ft.Icon(ft.Icons.PERSON, size=45, color=color_borde), 
                                ft.Column([
                                    ft.Text(nombre, weight="bold", size=16, color="black"),
                                    ft.Text(f"Matrícula: {matricula}", size=13, color=self.GRIS_TEXTO),
                                    ft.Text(f"Tipo: {tipo}", size=11, weight="bold", color=color_borde),
                                    ft.Row([ft.Icon(icono_razon, size=15, color="#6B7280"), ft.Text(razon, size=13, color="black")], spacing=5),
                                    ft.Text(f"Lugar: {lugar} | Fecha: {fecha}", size=12, color="#6B7280"),
                                ], spacing=4)
                            ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Row([
                                self.build_btn_resuelto() if estado == "Pendiente" else self.build_btn_pendiente(),
                                # MODIFICADO: Pasamos una función lambda que llama a abrir_dialogo con TODOS los datos
                                self.build_btn_detalles(
                                    lambda e: self.abrir_dialogo(e, nombre, matricula, carrera, semestre, tipo, razon, lugar, fecha, estado)
                                )
                            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
                ], spacing=0
            )
        )

    # ===== LÓGICA DE NAVEGACIÓN (Se mantiene igual) =====
    def ir_a_registro(self, e):
        self.content = PantallaRegistroIncidencia(self._page, vista_anterior=self)
        self.update()

    # ===== CONSTRUCCIÓN DE LA INTERFAZ =====
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
                ft.Text("Gestión de Incidencias", size=32, weight="bold", color="black"),
                ft.Text("Busca y gestiona el catálogo de incidencias registradas en el sistema.", color=self.GRIS_TEXTO)
            ]),
            btn_nueva_incidencia
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        filtros = ft.Container(
            bgcolor="white", border_radius=35, padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="black12", offset=ft.Offset(0, 4)),
            content=ft.Row([
                self.input_busqueda,
                ft.Container(width=1, height=30, bgcolor=self.GRIS_BORDE),
                self.dropdown_estado,
                ft.ElevatedButton("Buscar", height=45, style=ft.ButtonStyle(bgcolor=self.AZUL, color="white", shape=ft.RoundedRectangleBorder(radius=25), padding=ft.padding.symmetric(horizontal=30)))
            ], spacing=5, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # MODIFICADO: Agregamos datos de Carrera y Semestre a los ejemplos de la lista
        lista = ft.Column([
            self.build_card("Carlos Daniel", "100025787", "Ingeniería en Sistemas", "4° Semestre", "Ruido excesivo", "Cubículo 1", "24/Marzo/2026 - 10:30 AM", "PARCIAL", "Pendiente"),
            self.build_card("Cruz Castillo", "100025788", "Lic. en Derecho", "6° Semestre", "Uso indebido del equipo", "Cubículo 2", "25/Marzo/2026 - 11:00 AM", "DEFINITIVA", "Resuelto"),
            self.build_card("Jose Angel", "ABCDEFGA", "Medicina", "2° Semestre", "Comportamiento inapropiado", "Cubículo 3", "26/Marzo/2026 - 09:15 AM", "PARCIAL", "Pendiente"),
            self.build_card("Figueroa Sales", "ABCDEFGA", "Contaduría", "8° Semestre", "Páginas arrancadas", "Área de lectura", "27/Marzo/2026 - 16:00 PM", "DEFINITIVA", "Resuelto"),
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

        paginacion = ft.Row([
            ft.Text("1-10 de 100 incidencias", color="black"),
            ft.Row([ft.OutlinedButton("Anterior"), ft.OutlinedButton("Siguiente")], spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.content = ft.Column([encabezado, filtros, lista, paginacion], spacing=20, expand=True)

# Código para probar la clase sola
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Prueba UNACH - Incidencias"
        page.bgcolor = "#D0DCE7" # Un fondo gris para que resalte el contenedor azul claro
        p = PantallaIncidencias(page)
        page.add(p)

    ft.app(target=main)
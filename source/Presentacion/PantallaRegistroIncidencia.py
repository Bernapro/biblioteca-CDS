import flet as ft
import datetime

class PantallaRegistroIncidencia(ft.Container):
    def __init__(self, page: ft.Page, vista_anterior=None):
        super().__init__()
        self._page = page
        self.vista_anterior = vista_anterior
        self.expand = True
        
        # Colores consistentes con tu diseño
        self.AZUL = "#3B82F6"
        self.GRIS_BORDE = "#D1D5DB"
        self.GRIS_TEXTO = "#6B7280"
        self.TEXT = "#111827"
        self.CARD = "white"

        # === CONTROLES DEL FORMULARIO ===
        self.txt_nombre = self._crear_input("Nombre del estudiante", width=350)
        self.txt_matricula = self._crear_input("Matrícula", width=350)
        
        self.drop_tipo = ft.Dropdown(
            label="Tipo de incidencia",
            width=350, border_radius=12, border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            options=[
                ft.dropdown.Option("PARCIAL"),
                ft.dropdown.Option("DEFINITIVA")
            ]
        )

        self.txt_desc = ft.TextField(
            label="Descripción de la incidencia",
            width=350, border_radius=12, border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            multiline=True, min_lines=3,
            hint_text="Describe lo sucedido..."
        )

        # Categoría
        self.drop_cat = ft.Dropdown(
            label="Categoría",
            width=165, border_radius=12, border_color=self.GRIS_BORDE,
            focused_border_color=self.AZUL,
            value="Libros", # 🔥 NUEVO: Valor inicial por defecto
            options=[
                ft.dropdown.Option("Ruido"),
                ft.dropdown.Option("Equipo"),
                ft.dropdown.Option("Comportamiento"),
                ft.dropdown.Option("Libros")
            ],
            on_select=self.actualizar_vista_previa
        )

        # Elementos de Vista Previa (Iniciados con los valores de "Libros")
        self.icono_previa = ft.Icon(ft.Icons.WARNING, color=self.AZUL, size=30)
        self.txt_previa = ft.Text("Libros", size=13, weight="bold")
        
        self.container_previa = ft.Container(
            content=ft.Row([self.icono_previa, self.txt_previa], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            width=165, height=60, bgcolor="#F3F4F6", border_radius=12,
            padding=10, 
            alignment=ft.Alignment(0, 0) 
        )

        self.row_cat_previa = ft.Row([self.drop_cat, self.container_previa], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        self.txt_lugar = self._crear_input("Lugar (Ej. Cubículo 1)", width=165)
        
        # --- CALENDARIO ---
        self.calendario = ft.DatePicker(
            on_change=self.seleccionar_fecha,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now(), 
        )
        self._page.overlay.append(self.calendario)

        self.txt_fecha = ft.TextField(
            label="Fecha",
            width=165,
            border_color=self.GRIS_BORDE,
            border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT),
            read_only=True,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.abrir_calendario
        )
        
        self.row_lugar_fecha = ft.Row([self.txt_lugar, self.txt_fecha], spacing=20, alignment=ft.MainAxisAlignment.CENTER)

        self.build_ui()

    def seleccionar_fecha(self, e):
        if self.calendario.value:
            self.txt_fecha.value = self.calendario.value.strftime("%Y-%m-%d")
            self.txt_fecha.update()

    def abrir_calendario(self, e):
        self.calendario.open = True
        self._page.update()

    # 🔥 CORRECCIÓN: Lógica mejorada para la vista previa
    def actualizar_vista_previa(self, e):
        cat = self.drop_cat.value
        if cat:
            self.txt_previa.value = cat
            if cat == "Ruido": 
                self.icono_previa.name = ft.Icons.VOLUME_UP_ROUNDED
            elif cat == "Equipo": 
                self.icono_previa.name = ft.Icons.COMPUTER_ROUNDED
            elif cat == "Comportamiento": 
                self.icono_previa.name = ft.Icons.PERSON_OFF_ROUNDED
            elif cat == "Libros": 
                self.icono_previa.name = ft.Icons.WARNING
            
            # Actualizamos la pantalla para reflejar el cambio
            self.update()

    def _crear_input(self, label, width):
        return ft.TextField(
            label=label, width=width,
            border_color=self.GRIS_BORDE, border_radius=12,
            focused_border_color=self.AZUL,
            text_style=ft.TextStyle(color=self.TEXT)
        )

    def cancelar(self, e):
        if self.vista_anterior:
            self.vista_anterior.build_ui()
            self.vista_anterior.update()

    def build_ui(self):
        formulario = ft.Column(
            [
                self.txt_nombre,
                self.txt_matricula,
                self.drop_tipo,
                self.txt_desc,
                self.row_cat_previa,
                self.row_lugar_fecha
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
                    ft.Icon(ft.Icons.ADD_ALERT_ROUNDED, size=50, color=self.AZUL),
                    ft.Text("Registro de Incidencia", size=26, weight="bold", color=self.TEXT),
                    ft.Text("Reporte detallado de irregularidades", size=14, color=self.GRIS_TEXTO),
                    ft.Divider(height=15, color="transparent"),
                    formulario,
                    ft.Divider(height=15, color="transparent"),
                    ft.Row(
                        [
                            ft.OutlinedButton("Cancelar", on_click=self.cancelar, style=ft.ButtonStyle(color="red")),
                            ft.ElevatedButton(
                                "Guardar Reporte",
                                bgcolor=self.AZUL, color="white", width=180,
                                on_click=lambda _: print("Guardado")
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
                ft.Container(
                    width=660, border_radius=40, padding=30,
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
            scroll=ft.ScrollMode.AUTO
        )
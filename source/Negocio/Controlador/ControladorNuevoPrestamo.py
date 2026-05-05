import flet as ft
from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Negocio.Modelo.Usuario import Usuario
from datetime import datetime


class ControladorNuevoPrestamo:
    def __init__(self, pantalla, endEjemplares: BibliotecaClientInterface, repositorio: RepositorioImpl, endPrestamo: BibliotecaClientInterface):
        self.__pantalla = pantalla
        self.__endEjemplares = endEjemplares
        self.__repo = repositorio
        self.__usuario = None
        self.__endPrestamo = endPrestamo




    def listener(self,e):
        id = e.control.data
        if id:
            if id == "btn_buscar":
                self.buscarLibroPorNoAdquisicion()


    def buscar_alumno(self, e):
        self.__usuario = Usuario()
        matricula_buscar = ""
        matricula_buscar = self.__pantalla.txt_matricula.value
        if len(matricula_buscar) > 6:
            usr = self.__repo.buscar_usuario_por_identificador(matricula_buscar)
            print(usr)
            if usr:
                self.__usuario.set_columns(usr)

                # Actualizamos la tarjeta dinámicamente con los datos reales
                self.__pantalla.card_alumno.bgcolor = "surfaceVariant"
                self.__pantalla.card_alumno.border_radius = 12
                self.__pantalla.card_alumno.padding = 15
                self.__pantalla.card_alumno.content = ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=self.__pantalla.AZUL),
                    ft.Column([
                        ft.Text(self.__usuario.getNombre(), weight="bold", size=16, color=self.__pantalla.TEXT),
                        ft.Text(self.__usuario.getTipo_usuario(), size=13, color=self.__pantalla.GRIS_TEXTO)
                    ], expand=True, spacing=2),
                    ft.Container(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, size=14, color=self.__pantalla.VERDE), ft.Text("Alumno encontrado", size=12, color=self.__pantalla.VERDE, weight="bold")], spacing=4),
                        bgcolor="#D1FAE5", 
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        border_radius=15
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
        else:
            # Lógica en caso de que no se encuentre el alumno o el campo esté vacío
            self.__pantalla.card_alumno.bgcolor = ft.Colors.TRANSPARENT
            self.__pantalla.card_alumno.content = ft.Text("Por favor, ingresa una matrícula válida.", color="red")
            
        self.__pantalla.update()

    def buscarLibroPorNoAdquisicion(self):
        noAdquisicion = self.__pantalla.txt_adquisicion.value
        ejem = self.__endEjemplares.get(noAdquisicion)
        if ejem:
            args = ejem.getBody()
            self.__pantalla.libros_cache = [(args["id"], args["libro"].getTitulo(), " ".join(args["libro"].getAutores()), args["noAdquisicion"], args["disponible"])]
            self.__pantalla.actualizar_lista()


    def obtener_libros_prueba(self):
        # Más adelante esto será una consulta a la Base de Datos
        return [
            ("El principito", "Antoine de Saint-Exupéry", "ADQ-001245"),
            ("1984", "George Orwell", "ADQ-001246"),
            ("Cien años de soledad", "Gabriel García Márquez", "ADQ-001247"),
            ("El alquimista", "Paulo Coelho", "ADQ-001248"),
            ("Rayuela", "Julio Cortázar", "ADQ-001249")
        ]

    def registrar_prestamo(self, e):
        if self.__usuario:
            ejemplaresIds = [tupla[0] for tupla in self.__pantalla.libros_seleccionados.values()]
            fecha_limite = self.__pantalla.txt_fecha_limite.value
            fecha_objeto = datetime.strptime(fecha_limite, "%d/%b/%Y")
            fecha_sql = fecha_objeto.strftime("%Y-%m-%d")
            args = {"usuario": self.__usuario.getIdentificador(), "fecha_limite": fecha_sql, "ejemplaresIds": ejemplaresIds}
            self.__endPrestamo.post(args)
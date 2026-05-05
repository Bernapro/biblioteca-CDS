import flet as ft
from Infraestructura.API.Interfaces.BibliotecaClientInterface import BibliotecaClientInterface
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
class ControladorNuevoPrestamo:
    def __init__(self, pantalla, endEjemplares: BibliotecaClientInterface, repositorio: RepositorioImpl):
        self.__pantalla = pantalla
        self.__endEjemplares = endEjemplares
        self.__repo = repositorio



    def listener(self,e):
        id = e.control.data
        if id:
            if id == "btn_buscar":
                self.buscarLibroPorNoAdquisicion()


    def buscar_alumno(self, e):
        matricula_buscar = ""
        matricula_buscar = self.__pantalla.txt_matricula.value
        if len(matricula_buscar) > 6:
            usr = self.__repo.buscar_usuario_por_identificador(matricula_buscar)
            print(usr)
            if usr:
                nombre = usr["nombre"]
                tipoUsuario = usr["tipo_usuario"]
                
            

                # Actualizamos la tarjeta dinámicamente con los datos reales
                self.__pantalla.card_alumno.bgcolor = "surfaceVariant"
                self.__pantalla.card_alumno.border_radius = 12
                self.__pantalla.card_alumno.padding = 15
                self.__pantalla.card_alumno.content = ft.Row([
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=self.__pantalla.AZUL),
                    ft.Column([
                        ft.Text(nombre, weight="bold", size=16, color=self.__pantalla.TEXT),
                        ft.Text(tipoUsuario, size=13, color=self.__pantalla.GRIS_TEXTO)
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
        args = ejem.getBody()
        if ejem:
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
        # Aquí irá la lógica de guardado a la base de datos a través de tu repositorio
        print(self.__pantalla.libros_seleccionados)
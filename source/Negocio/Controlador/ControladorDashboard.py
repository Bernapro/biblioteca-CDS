from datetime import datetime, date, time, timedelta
from Negocio.Modelo.RepositorioImpl import RepositorioImpl
from Persistencia.CRUD.CRUDimpl import CRUDimp
from Infraestructura.API.BibliotecaPrestamos import BibliotecaPrestamos

class ControladorDashboard:
    def __init__(self):
        self.__repo = RepositorioImpl(CRUDimp())
        self.__prestamos_api = BibliotecaPrestamos()

    def obtener_datos_dashboard(self):
        stats = self.__repo.obtener_estadisticas_dashboard() or {}
        visitas_semana = stats.get("visitas_semana", {})
        visitas_semana_normalizadas = {day: visitas_semana.get(day, 0) for day in range(1, 8)}
        estado_prestamos = self.__prestamos_api.getEstado()
        return {
            "sesiones_activas_hoy": self.__repo.contar_sesiones_activas_hoy(),
            "prestamos": estado_prestamos.getVigentes() if estado_prestamos else 0,
            "vencidos": estado_prestamos.getVencidos() if estado_prestamos else 0,
            "visitas_semana_totales": sum(visitas_semana_normalizadas.values()),
            "usuarios_registrados": stats.get("usuarios_totales", 0),
            "libros_disponibles": None,
            "incidencias_abiertas": stats.get("incidencias_abiertas", 0),
            "visitas_semana": visitas_semana_normalizadas,
            "turno": self._calcular_turno_actual()
        }

    def _calcular_turno_actual(self):
        ahora = datetime.now()

        hoy = date.today()

        inicio_matutino = datetime.combine(hoy, time(8, 0))
        fin_matutino = datetime.combine(hoy, time(14, 0))

        inicio_vespertino = datetime.combine(hoy, time(14, 0))
        fin_vespertino = datetime.combine(hoy, time(20, 0))

        duracion_turno = timedelta(hours=6)

        if inicio_matutino <= ahora < fin_matutino:

            turno = "Matutino"
            inicio = inicio_matutino
            fin = fin_matutino

            transcurrido = ahora - inicio
            restante = fin - ahora


        elif inicio_vespertino <= ahora < fin_vespertino:

            turno = "Vespertino"
            inicio = inicio_vespertino
            fin = fin_vespertino

            transcurrido = ahora - inicio
            restante = fin - ahora


        else:

            turno = "Cerrado"

            # Antes de abrir
            if ahora < inicio_matutino:

                tiempo_apertura = inicio_matutino - ahora

            # Después de cerrar
            else:

                manana = hoy + timedelta(days=1)

                proxima_apertura = datetime.combine(
                    manana,
                    time(8, 0)
                )

                tiempo_apertura = proxima_apertura - ahora

            return {

                "turno": "Biblioteca cerrada",

                "inicio": "--:--",

                "fin": "--:--",

                "duracion_horas": "Sin servicio",

                "transcurrido": "00:00:00",

                "restante_formateado":
                    self._format_timedelta(tiempo_apertura),

                "porcentaje_restante": 0
            }

        porcentaje_restante = max(
            0.0,
            min(
                1.0,
                restante.total_seconds()
                / duracion_turno.total_seconds()
            )
        )

        return {

            "turno": turno,

            "inicio": inicio.strftime("%I:%M %p"),

            "fin": fin.strftime("%I:%M %p"),

            "duracion_horas": "6 horas",

            "transcurrido":
                self._format_timedelta(transcurrido),

            "restante_formateado":
                self._format_timedelta(restante),

            "porcentaje_restante":
                porcentaje_restante
        }

    def _format_timedelta(self, value: timedelta):
        total_seconds = int(value.total_seconds())
        if total_seconds < 0:
            total_seconds = 0
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        segundos = total_seconds % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

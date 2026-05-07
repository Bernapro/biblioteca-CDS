from abc import ABC, abstractmethod


class ReporteRepository(ABC):

    @abstractmethod
    def obtener_asistencia_completa(
        self,
        fecha_inicio,
        fecha_fin,
        tipo_usuario=None
    ):
        pass

    @abstractmethod
    def obtener_usuarios_mas_activos(
        self,
        fecha_inicio,
        fecha_fin,
        tipo_usuario=None
    ):
        pass

    @abstractmethod
    def obtener_horas_pico_avanzado(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_tendencia_diaria(
        self,
        fecha_inicio,
        fecha_fin,
        tipo_usuario=None
    ):
        pass

    @abstractmethod
    def obtener_reporte_carreras(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_reporte_facultades(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_reporte_semestres(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_visitantes_externos(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_reporte_saturacion(
        self,
        fecha_inicio,
        fecha_fin
    ):
        pass

    @abstractmethod
    def obtener_reporte_crecimiento(self):
        pass
from datetime import datetime

class FormatearFecha:
    @staticmethod
    def formatear_fecha_iso(fecha_iso):
        if not fecha_iso:
            return None
        return datetime.strptime(fecha_iso, "%Y-%m-%d").strftime("%d/%b/%Y")